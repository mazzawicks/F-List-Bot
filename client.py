import asyncio
from asyncio import PriorityQueue
import time
import websockets
from websockets.asyncio.client import connect

from client_commands import ClientCommands
from api import API
from priority import Priority
from server_commands import ServerCommands

import logging
log = logging.getLogger('main')

class Client:
    def __init__(self, config):
        self.config = config
        self.api = API(config)
        self.url = config['url']
        self.join_channels = config['join_channels']
        self.op_channels = config['channel_ops']
        
        self.channels = []

        self.incoming_queue = PriorityQueue()
        self.outgoing_queue = PriorityQueue()
        self.rate_limit = config['rate_limit']
        self.last_message_time = 0
        self.ticket = None
        self.ticket_expires = 0

        # turn these into a dict, or even a stat class
        self._msg_received = 0
        self._msg_skipped = 0
        self._msg_processed = 0
        self._msg_sent = 0


    async def login(self):
        self.api.refresh_ticket()

        assert(self.config['character'] in self.ticket['characters'])

        login_payload = {
            "method": "ticket",
            "account": self.config['account'],
            "ticket": self.ticket,
            "character": self.config['character'],
            "cname": self.config['bot_name'],
            "cversion": self.config['bot_version'],
        }

        identified = await ClientCommands.identify(login_payload)

        if not identified:
            raise UnableToLogInError()
        
        await self.ready() # could separate login from ready


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
                    self._msg_received += 1
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
                    self._msg_skipped += 1
                    continue
                if priority == Priority.ACK:
                    log.info(f"Acknowledging message: {formatted_message}")
                    # data and state handlers
                    self._msg_skipped += 1
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
                        self._msg_sent += 1
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