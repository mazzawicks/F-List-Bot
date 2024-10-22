import asyncio
import time
from api import API
from event_queue import EventQueue
from state import State
from client_commands import ClientCommands as Client

class Actions:
    '''
    Thin wrapper around ClientCommands, allows grouping commands or checking DataStore, etc. more complex actions after EventHandler
    '''

    def __init__(self, action_type, *action_data):
        self.type = action_type
        self.data = action_data

    @classmethod
    def ActionQueue(cls, queue: EventQueue):
        cls.Queue = queue

    @classmethod
    async def put(cls, action):
        # print(f"!!! action {action}")
        await asyncio.create_task(cls.Queue.put_action(action)) 
    
    @staticmethod
    async def identify(login_payload):
        return await Actions.put(Client.identify(login_payload))
        # handling confirm in Handlers

    @staticmethod
    async def ping():
        return await Actions.put(Client.ping())
    
    @staticmethod
    async def get_room_lists():
        public = Actions.put(Client.get_channel_list())
        private =  Actions.put(Client.get_private_rooms_list())
        return await asyncio.gather(public, private)
    
    @staticmethod
    async def join_channel(channel):
        await Actions.put(Client.join_channel(channel))
        # confirm()

    @staticmethod
    def join_channels(channels):
        for channel in channels:
            return Actions.join_channel(channel)
        
    @staticmethod
    def send_message(channel, message):
        return Actions.put(Client.send_message(channel, message))
    
    @staticmethod
    def send_private_message(character):
        return Actions.put(Client.send_private_message(character))

    # - message all channels bot is in
    @staticmethod
    def message_all_channels(message):
        for channel in State.current_channels:
            return Actions.send_message(channel, message)

    # - roll dice
    @staticmethod
    def roll_dice(channel, dice):
        return Actions.put(Client.roll_dice(channel, dice))

    # - choose someone at random
    @staticmethod
    def bottle(channel):
        return Actions.put(Client.roll_dice(channel, "bottle"))


    # # - greet people - use "{}" if the name should appear in the greeting
    @staticmethod
    def greet(channel, character, greeting):
        return Actions.put(Client.send_message(channel, greeting.format(character)))

    # - commands - could be activated by chat message starting with !
    @staticmethod
    def bot_command(channel, character, command):
        State.command(channel, character, command)

    # - keep track of some stats or state or story or something

    # - create a new room
    @staticmethod
    def create_room(name):
        return Actions.put(Client.create_private_channel(name))
    
    # - invite someone to a room
    @staticmethod
    def invite_to_room(room, character):
        return Actions.put(Client.invite_to_channel(room, character))

    # - leave a room
    @staticmethod
    def leave_room(room):
        return Actions.put(Client.leave_channel(room))


    # - timeout/kick/ban someone from a room
    @staticmethod
    def timeout(character, room, minutes):
        return Actions.put(Client.timeout_character(room, character, minutes))

    # - send a friend request
    @staticmethod
    def send_friend_request(character): # separate queue? technically supposed to rate limit api requests too
        return API.send_friend_request(character) # also not sure what to return here, if anything

    # - accept/deny a friend request
    @staticmethod
    def accept_friend_request(request_id):
        return API.accept_friend_request(request_id) # separate queue? technically supposed to rate limit api requests too
    @staticmethod
    def deny_friend_request(request_id):
        return API.deny_friend_request(request_id) # separate queue? technically supposed to rate limit api requests too
    #