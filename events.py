
from client_commands import ClientCommands
from event_queue import EventQueue
from priority import Priority


class Events:
    '''
    Thin wrapper around ServerCommands. Allows grouping multiple commands into a single event, and adding custom events.
    '''
    def __init__(self, event_type, *event_data):
        self.type = event_type
        self.data = event_data

    @classmethod
    def EQueue(cls, queue: EventQueue): # name mess
        cls.Queue = queue

    @classmethod
    def put(cls, event):
        cls.Queue.put_event(event)

    @staticmethod
    def identified(payload):
        Events.put("identified")

    @staticmethod
    def ping():
        Events.put("ping")

    @staticmethod
    def channel_message(character, message, channel):
        Events.put("channel_message")

    @staticmethod
    def private_message(character, message):
        Events.put("private_message")

    @staticmethod
    def chatops(chatops):
        Events.put("chatops")

    @staticmethod
    def promoted_chatop(character):
        Events.put("promoted_chatop")

    @staticmethod
    def broadcast(message):
        Events.put("broadcast")

    @staticmethod
    def channel_description(channel, description):
        Events.put("channel_description")

    @staticmethod
    def public_channel_list(channels):
        Events.put("public_channel_list")

    @staticmethod
    def invited_to_channel(sender, title, name):
        Events.put("invited_to_channel")

    @staticmethod
    def character_banned(operator, channel, character):
        Events.put("character_banned")

    @staticmethod
    def character_kicked(operator, channel, character):
        Events.put("character_kicked")

    @staticmethod
    def promoted_channel_op(character, channel):
        Events.put("promoted_channel_op")

    @staticmethod
    def channel_ops_list(channel, oplist):
        Events.put("channel_ops_list")

    @staticmethod
    def connected(count):
        Events.put("connected")

    @staticmethod
    def removed_channel_op(character, channel):
        Events.put("removed_channel_op")

    @staticmethod
    def character_set_as_owner(character, channel):
        Events.put("character_set_as_owner")

    @staticmethod
    def character_timed_out(operator, channel, length, character):
        Events.put("character_timed_out")

    @staticmethod
    def demoted_chatop(character):
        Events.put("demoted_chatop")

    @staticmethod
    def error_occurred(number, message):
        Events.put("error_occurred")

    @staticmethod
    def character_kink_search_response(characters, kinks):
        Events.put("character_kink_search_response")

    @staticmethod
    def logged_out(character):
        Events.put("logged_out")

    @staticmethod
    def hello_response(message):
        Events.put("hello_response")

    @staticmethod
    def channel_data(users, channel, mode):
        Events.put("channel_data")

    @staticmethod
    def character_joined(character, channel, title):
        Events.put("character_joined")

    @staticmethod
    def kinks_data(type, message, key, value):
        Events.put("kinks_data")

    @staticmethod
    def character_left_channel(channel, character):
        Events.put("character_left_channel")

    @staticmethod
    def character_list(characters):
        Events.put("character_list")

    @staticmethod
    def character_connected(identity, gender, status):
        Events.put("character_connected")

    @staticmethod
    def ignore_list(action, characters, character):
        Events.put("ignore_list")

    @staticmethod
    def friends_list(characters):
        Events.put("friends_list")

    @staticmethod
    def private_rooms_list(channels):
        Events.put("private_rooms_list")

    @staticmethod
    def profile_data(type, message, key, value):
        Events.put("profile_data")

    @staticmethod
    def roleplay_ad_message(channel, message, character):
        Events.put("roleplay_ad_message")

    @staticmethod
    def dice_result(channel, message, character, results, rolls, endresult):
        Events.put("dice_result")

    @staticmethod
    def bottle_result(channel, message, character, target):
        Events.put("bottle_result")

    @staticmethod
    def channel_mode_changed(mode, channel):
        Events.put("channel_mode_changed")

    @staticmethod # gotta find out what type values can be
    def received_note(type, character):
        Events.put("received_note")

    @staticmethod
    def admin_issue(action, moderator, character, timestamp):
        Events.put("admin_issue")

    @staticmethod
    def character_status(status, character, statusmsg):
        Events.put("character_status")

    @staticmethod
    def system_message(message, channel):
        Events.put("system_message")

    @staticmethod
    def character_typing(character, status):
        Events.put("character_typing")

    @staticmethod
    def uptime(time, startime, startstring, accepted, channels, users, maxusers):
        Events.put("uptime")
        
    @staticmethod
    def server_variables(value, variable):
        Events.put("server_variables")





