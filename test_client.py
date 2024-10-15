import asyncio
import logging
import os

from client import Client

from dotenv import load_dotenv
load_dotenv()

config = {
    "url": "ws://localhost:8110",
    "chatop": False,
    "username": os.getenv('username'),
    "password": os.getenv('password'),
    "character_name": os.getenv('character'),
    "join_channels": os.getenv('channels', []),
    "channel_op": os.getenv('channel_op', []),
    "bot_name": "Mommybot",
    "bot_version": "0.1.0",
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