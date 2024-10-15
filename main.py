import asyncio
import logging
import os

from client import Client

from dotenv import load_dotenv
load_dotenv()

config = {
    "url": "wss://chat.f-list.net/chat2",
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
log.setLevel(logging.DEBUG) # bring to Info later

async def begin(config):

    # parse config
    channel_ops = config['channel_op']
    if channel_ops:
        channel_ops = [el.strip() for el in channel_ops]
        channel_ops = list(filter(lambda x: bool(x), channel_ops))
    else:
        channel_ops = []
    config['channel_op'] = channel_ops

    channels = config['join_channels']
    if channels:
        channels = [el.strip() for el in channels]
        channels = list(filter(lambda x: bool(x), channels))
    else:
        channels = []
    config['join_channels'] = channels


    client = Client(config)

    ws = await client.login()
    await client.join_channels(config['join_channels'])


async def main():
    
    log.info("Beginning Client")
    begin()
    # client = Client(config)
    # client.login()

    
# Test
if __name__ == '__main__':
    asyncio.run(main())