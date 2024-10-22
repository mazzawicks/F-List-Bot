import asyncio
import logging
import os

from client import Client

from dotenv import load_dotenv
load_dotenv()

config = {
    "url": "wss://chat.f-list.net/chat2",
    "chatop": False,
    "account": os.getenv('account'),
    "password": os.getenv('password'),
    "character": os.getenv('character'),
    "join_channels": os.getenv('channels', []),
    "channel_ops": os.getenv('channel_ops', []),
    "bot_name": "Mommybot",
    "bot_version": "0.1.0",
    "rate_limit": .2
}

logging.basicConfig()
log = logging.getLogger('main')
log.setLevel(logging.DEBUG) # bring to Info later

# async def begin(config):

def parse_config(config):
    channel_ops = config['channel_ops']
    if channel_ops:
        channel_ops = [el.strip() for el in channel_ops]
        channel_ops = list(filter(lambda x: bool(x), channel_ops))
    else:
        channel_ops = []
    config['channel_ops'] = channel_ops

    channels = config['join_channels']
    if channels:
        channels = [el.strip() for el in channels]
        channels = list(filter(lambda x: bool(x), channels))
    else:
        channels = []
    config['join_channels'] = channels



async def main():
    parse_config(config)
    # begin()

    log.info("Beginning Client")
    client = Client(config)

    await client.login()
    await client.join_channels(config['join_channels'])
    # client = Client(config)
    # client.login()

    
if __name__ == '__main__':
    asyncio.run(main())