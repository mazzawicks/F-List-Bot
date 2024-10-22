import asyncio
import time
import websockets
from websockets.asyncio.client import connect as _connect

from api import API
from events import Events
from event_queue import EventQueue
from handlers import _default_handlers
# from priority import Priority
from server_commands import ServerCommands
from actions import Actions

import logging
log = logging.getLogger('main')

class Client:
    def __init__(self, config):
        if not config:
            raise NoConfigError("No config detected. It should be in the root of your project. Did you forget to create your .env file? You can run generate_env.py to help create one.")

        self.config = config
        self.api = API(config)
        self.url = config['url']
        self.join_channels = config['join_channels']
        self.op_channels = config['channel_ops']
        
        self.channels = []

        self.rate_limit = config['rate_limit']
        self.last_message_time = 0
        self.ticket = None
        self.ticket_expires = 0

        self.event_queue = EventQueue()
        Events.EQueue(self.event_queue) # bleh
        Actions.ActionQueue(self.event_queue)
        self.event_queue.add_handlers(_default_handlers)
        # self.event_queue.add_handlers(custom_handlers)

        # turn these into a dict, or even a stat class
        self._msg_received = 0
        self._msg_skipped = 0
        self._msg_processed = 0
        self._msg_sent = 0


    async def login(self):
        # self.ticket = self.api.refresh_ticket()
        self.ticket = "nice" # dev test
        # assert(self.config['character'] in self.ticket['characters'])

        login_payload = {
            "method": "ticket",
            "account": self.config['account'],
            "ticket": self.ticket,
            "character": self.config['character'],
            "cname": self.config['bot_name'],
            "cversion": self.config['bot_version'],
        }

        identify = asyncio.create_task(Actions.identify(login_payload))
        room_lists = asyncio.create_task(Actions.get_room_lists())
        await asyncio.gather(identify, room_lists)

        join_tasks = []
        for channel in self.join_channels:
            join_tasks.append(asyncio.create_task(Actions.join_channel(channel)))
        return await asyncio.gather(*join_tasks)
        
    async def connect(self):
        while True:
            if not self.event_queue.has_login_tasks:
                await self.login()
            async with _connect(self.url) as websocket:
                log.info(f'Connected! {websocket.remote_address}')
                await self.handle_websocket(websocket)
            
            log.info(f"Disconnected! Trying again in 15 seconds")

            asyncio.sleep(15)
        

    async def handle_websocket(self, ws):
        await self.login() # dev test
        async def receive_messages():
            log.info('Beginning to read messages')
            while True:
                try:
                    message = await ws.recv()
                    log.info(message[:20])
                    self._msg_received += 1
                    # await self.event_queue.put_event(message)
                    ServerCommands.read_message(message)
                # except websockets.ConnectionClosedOK: # Not sure these belong here
                #     log.info('Connection Closed OK')
                #     raise WebsocketDisconnected
                # except websockets.ConnectionClosedError:
                #     log.info('Connection Closed with an error: {e}')
                #     raise WebsocketDisconnected
                except Exception as e:
                    log.exception(f"Error on message {message}: {e}")
                    raise e # for dev test, else just log errors and keep the bot running

        async def send_message():
            while True:
                # still need separate queue/timer for messages, ads, status
                # get VAR flood variables
                if time.time() > self.last_message_time + self.rate_limit:
                    try:
                        priority, message = await self.event_queue.get_action()
                        await ws.send(message)
                        self._msg_sent += 1
                        log.info(f"sent message {message}")
                        self.last_message_time = time.time()
                    except asyncio.QueueEmpty:
                        pass
                await asyncio.sleep(.1)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(receive_messages())
            # tg.create_task(process_messages())
            tg.create_task(send_message())

        # await asyncio.gather(read, process, send)


    def check_channel_op_status(self, channel):
        # check config for channels we're channel op on
        return self.config["channel_ops"].get(channel, False)

class NoConfigError(Exception):
    pass

class UnableToLogInError(Exception):
    pass

class WebsocketDisconnected(Exception):
    pass

