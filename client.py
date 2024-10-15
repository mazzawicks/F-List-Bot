import asyncio
from asyncio import PriorityQueue
import json
import logging
import time
import websockets
from websockets.asyncio.client import connect

from client_commands import ClientCommands
from json_endpoints import flist_endpoint, endpoints
from server_commands import ServerCommands

log = logging.getLogger('main')

class Client:
    def __init__(self, config):
        self.config = config
        self.url = config['url']
        self.incoming_queue = PriorityQueue()
        self.outgoing_queue = PriorityQueue()
        self.rate_limit = 1
        self.last_message_time = 0
        self.ticket = None
        self.ticket_expiry = None

        self.join_channels = config['join_channels']
        self.op_channels = config['channel_ops']
        # self.current_channel = None

        self.server_command_list = ServerCommands.get_commands()

    async def login(self):
        ticket = self.get_ticket()
        # {'characters': ['THEYSTUD SIMP'],
        # 'default_character': '',
        # 'ticket': 'fct_8db994568a7589337b144767c64c64e327ab8f99613d56f5266f893d58f280af',
        # 'friends': [],
        # 'bookmarks': [],
        # 'error': ''}
        assert(self.config['username'] in ticket['characters'])

        login_payload = {
            "method": "ticket",
            "account": self.config['username'],
            "ticket": ticket,
            "character": self.config['character'],
            "cname": self.config['bot_name'],
            "cversion": self.config['bot_version'],
        }

        identified = await ClientCommands.identify(login_payload)

        if identified:
            await self.ready()
        else:
            raise UnableToLoginError()

    def get_ticket(self):
        url = endpoints['get_ticket']
        data = {
            "account": self.config['account'],
            "password": self.config['password'],
        }

        response = flist_endpoint(url, data)
        assert(response.status_code == 200)
        return response.json()

    async def ready(self):
        async with connect(self.url) as websocket:
            log.info(f'connected! {websocket.remote_address}')
            await self.handle_websocket(websocket)

    def read_message(self, msg):
        #All commands look like this:
        # XXX {"property":"value","anotherproperty":"value"}
        command = msg[:3]
        if command not in self.server_command_list:
            return -1, f"Unrecognized command: {command}"

        payload = msg[3:] #Commands without a json payload should not contain a trailing space after the message type
        log.info(f'command {command}, payload {payload}, len {len(payload)}')
        if len(msg) > 4:
            payload = json.loads(msg[4:])

        priority, out_message = ServerCommands.read(command, payload) # is this ever awaitable?
        return priority, out_message

    async def handle_websocket(self, ws):
        async def read_messages(in_queue):
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
                priority, formatted_message = self.read_message(message)
                if priority == -1:
                    log.info(f"Skipping message: {formatted_message}")
                    continue
                log.info(f"p{priority} {formatted_message}")
                await out_queue.put((priority, formatted_message))

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

        read = asyncio.create_task(read_messages(self.incoming_queue))
        process = asyncio.create_task(process_messages(self.incoming_queue, self.outgoing_queue))
        send = asyncio.create_task(send_message(self.outgoing_queue))

        await asyncio.gather(read, process, send)


    def check_channel_op_status(self, channel):
        # check config for channels we're channel op on
        return self.config["channel_op"].get(channel, False)


class WebsocketDisconnected(Exception):
    pass

class UnableToLoginError(Exception):
    pass