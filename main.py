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
    "join_channels": os.getenv('channels', []),
    "username": os.getenv('username'),
    "password": os.getenv('password'),
}

log = logging.getLogger()

async def begin(config):
    client = Client()

    ws = await client.login()
    await client.join_channels(config['join_channels'])


    # connect to f-list
    # - get ticket from json endpoint
    # - connect to ws
    # - identify
    # - join channels
    # - respond to pings
    # - respond to messages
    # - scan message for triggers
    #  - perform triggers


async def main():
    
    log.info("Beginning Client")
    client = Client(config)
    # client.login()

    
# Test
if __name__ == '__main__':
    asyncio.run(main())