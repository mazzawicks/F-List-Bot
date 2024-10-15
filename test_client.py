import asyncio
import logging
import json
import os
import websockets

from client import Client

from dotenv import load_dotenv
load_dotenv()

config = {
    "url": "wss://chat.f-list.net/chat2",
    "chatop": False,
    "channel_op": {}, # channel_op['my_channel'] = True
    "character_name": "",
    "join_channels": os.getenv('channels'),
    "username": os.getenv('username'),
    "password": os.getenv('password'),
}

logging.basicConfig()
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)

# async def begin(config):
#     client = Client()

#     ws = await client.login()
#     await client.join_channels(config['join_channels'])


async def test_main():
    from websockets.asyncio.server import serve
    
    log.info("Beginning Client Test")
    client = Client(config)

    async with serve(client.handle_websocket, "localhost", 8111):
        await asyncio.get_running_loop().create_future()

# Test
if __name__ == '__main__':
    asyncio.run(test_main())