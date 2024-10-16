import asyncio
from asyncio import PriorityQueue
import time
import websockets
from websockets.asyncio.client import connect

from client_commands import ClientCommands
from json_endpoints import flist_endpoint, endpoints # , get_ticket
from priority import Priority
from server_commands import ServerCommands

import logging
log = logging.getLogger('main')

class Client:
    def __init__(self, config):
        self.config = config
        self.url = config['url']
        self.join_channels = config['join_channels']
        self.op_channels = config['channel_ops']
        
        self.channels = []

        self.incoming_queue = PriorityQueue()
        self.outgoing_queue = PriorityQueue()
        self.rate_limit = 10 # long for testing, set back to 1. Maybe make configurable.
        self.last_message_time = 0
        self.ticket = None
        self.ticket_expires = 0


    async def login(self):
        self.get_ticket() # sets self.ticket and self.ticket_expires

        assert(self.config['username'] in self.ticket['characters'])

        login_payload = {
            "method": "ticket",
            "account": self.config['username'],
            "ticket": self.ticket,
            "character": self.config['character'],
            "cname": self.config['bot_name'],
            "cversion": self.config['bot_version'],
        }

        identified = await ClientCommands.identify(login_payload)

        if not identified:
            raise UnableToLogInError()
        
        await self.ready() # could separate login from ready

    def get_ticket(self):
        url = endpoints['get_ticket']
        data = {
            "account": self.config['account'],
            "password": self.config['password'],
        }

        response = flist_endpoint(url, data)
        assert(response.status_code == 200)
        self.ticket = response.json()
        self.ticket_expires = time.time() + (25 * 60) # refresh ticket every 25 minutes
        log.info('ticket is good')
        return self.ticket

    def get_endpoint(self, url, data=None):
        if time.time() > self.ticket_expires:
            self.get_ticket()
        response = flist_endpoint(url, data)
        assert(response.status_code in [200, 201, 202, 203, 204]) # come back to error checking and handling
        return response.json()


    async def ready(self):
        async with connect(self.url) as websocket:
            log.info(f'connected! {websocket.remote_address}')
            await self.handle_websocket(websocket)


    async def handle_websocket(self, ws):
        async def receive_messages(in_queue):
            log.info('Beginning to read messages')
            while True:
                try:
                    message = await ws.recv()
                    await in_queue.put(message)
                except websockets.ConnectionClosedOK:
                    log.info('Connection Closed OK')
                    raise WebsocketDisconnected
                except websockets.ConnectionClosedError:
                    log.info('Connection Closed with an error: {e}')
                    raise WebsocketDisconnected

        async def process_messages(in_queue, out_queue):
            while True:
                message = await in_queue.get()
                log.info(f"processing message: {message}")
                try:
                    priority, formatted_message = ServerCommands.read_message(message)
                except Exception as e:
                    log.exception(f"Error on message {message}: {e}")
                    raise e # for dev, else just log errors and keep the bot running
                if priority == Priority.SKIP:
                    log.info(f"Skipping message: {formatted_message}")
                    continue
                if priority == Priority.ACK:
                    log.info(f"Acknowledging message: {formatted_message}")
                    # data and state handlers
                    continue
                log.info(f"p{priority} {formatted_message}")
                await out_queue.put((priority, formatted_message))
                log.info(f"size of outgoing queue: {out_queue.qsize()}")

        async def send_message(queue):
            while True:
                if time.time() > self.last_message_time + self.rate_limit:
                    try:
                        priority, message = queue.get_nowait()
                        await ws.send(message)
                        log.info(f"sent message {message}")
                        self.last_message_time = time.time()
                    except asyncio.QueueEmpty:
                        pass
                await asyncio.sleep(.1)

        read = asyncio.create_task(receive_messages(self.incoming_queue))
        process = asyncio.create_task(process_messages(self.incoming_queue, self.outgoing_queue))
        send = asyncio.create_task(send_message(self.outgoing_queue))

        await asyncio.gather(read, process, send)


    def check_channel_op_status(self, channel):
        # check config for channels we're channel op on
        return self.config["channel_ops"].get(channel, False)


class WebsocketDisconnected(Exception):
    pass

class UnableToLogInError(Exception):
    pass