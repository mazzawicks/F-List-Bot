
import inspect

from priority import Priority

class ClientCommands:
    @staticmethod
    def prioritize(payload):
        func_name = inspect.stack()[1].function
        priority, command = ClientCommands.client_commands[func_name]
        if not payload: 
            return priority, command
        return priority, f"{command} {payload}"
    
    @staticmethod
    def identify(payload):
        # payload prepared upstream in login
        # return 0, f"IDN {payload}"
        return ClientCommands.prioritize(payload)

    @staticmethod
    def ping(_):
        print('clientcommands ping')
        # return 0, "PIN"
        return ClientCommands.prioritize(None)

    @staticmethod
    def send_message(channel, message):
        payload = {
            "channel": channel,
            "message": message,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def join_channel(channel):
        payload = { "channel": channel }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def create_private_channel(channel_name):
        # unique in that this is the only time the 'channel' param is a 
        # regular string, used as the name, instead of the ID
        payload = { "channel": channel_name }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def get_channel_list():
        return ClientCommands.prioritize()

    @staticmethod
    def channel_ops_list(channel):
        payload = { "channel": channel }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def search_characters_by_kinks(
        kinks,
        genders=None,
        orientations=None,
        languages=None,
        furryprefs=None,
        roles=None
    ):
        # Not sure why you'd do this with a bot
        # kinks is the only required param, everything else is an enum
        # see client commands for full list of each enum
        payload = {
            "kinks": kinks,
        }
        if genders:
            payload["genders"] = genders
        if orientations:
            payload["orientations"] = orientations
        if languages:
            payload["languages"] = languages
        if furryprefs:
            payload["furryprefs"] = furryprefs
        if roles:
            payload["roles"] = roles

        return ClientCommands.prioritize(payload)

    @staticmethod
    def ignore(action, character=None):
        # who would harass a bot? Plus this won't actually stop us from receiving messages
        # The server depends on the client to block messages on the ignore list
        # needs enum: action can be 'add', 'delete', 'notify', or 'list'
        # if action is 'list', there's no 'character' parameter
        payload = {
            "action": action,
        }
        if action != 'list':
            payload["character"] = character

        return ClientCommands.prioritize(payload)

    @staticmethod
    def request_character_kinks(character):
        payload = { "character": character }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def leave_channel(channel):
        payload = { "channel": channel }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def send_ad(channel, message):
        payload = {
            "channel": channel,
            "message": message,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def get_private_rooms_list():
        return ClientCommands.prioritize()

    @staticmethod
    def send_private_message(character, message):
        payload = {
            "recipient": character,
            "message": message
        }

    @staticmethod
    def get_character_data(character):
        payload = { "character": character }
        return ClientCommands.prioritize(payload)


    @staticmethod
    def roll_dice(channel, dice):
        payload = {
            "channel": channel,
            "dice": dice,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def alert_admin(action, report, character):
        # Not sure you'd want to do this with a bot
        # enum with single value: action can only be 'report'
        payload = {
            "action": "report",
            "report": report,
            "character": character,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def set_status(status, statusmsg):
        assert(status != 'looking')
        payload = {
            "status": status,
            "statusmsg": statusmsg,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def typing_status(character, status):
        # A bot typically doesn't need to send this,
        # unless generating a very long message
        # needs enum: status can be 'clear', 'paused', and 'typing'
        payload = {
            "character": character,
            "status": status,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def request_uptime():
        print('clientcommands uptime')
        return ClientCommands.prioritize()


    ### CHANNEL OP STATUS REQUIRED COMMANDS

    @staticmethod
    def request_channel_banlist(channel):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def ban_character_from_channel(character, channel):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def change_channel_description(channel, description):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "description": description,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def invite_to_channel(channel, character):
        # Needs channel op - why? double check
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def kick_character(channel, character):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def promote_channel_op(channel, character):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)


    @staticmethod
    def remove_channel_op(channel, character):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "character": character,
            "channel": channel,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def set_character_as_owner(character, channel):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        # only channel op? see if there are more up to date docs that distinguish between channel owner and moderator
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)
        

    @staticmethod
    def timeout_character(channel, character, minutes):
        # Needs channel op
        # minutes is a number from 1 to 90
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
            "length": minutes,
        }
        return ClientCommands.prioritize(payload)


    @staticmethod
    def unban_character(channel, character):
        # Needs channel op
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "character": character,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def set_channel_mode(channel, mode):
        # Needs channel op
        # Needs enum: mode can be 'chat', 'ads', or 'both'
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "mode": mode,
        }
        return ClientCommands.prioritize(payload)

    @staticmethod
    def set_channel_visibility(channel, status):
        # Needs channel op
        # Needs enum: status can be 'public' or 'private'
        # assert(.client.check_channel_op_status())
        payload = {
            "channel": channel,
            "status": status,
        }
        return ClientCommands.prioritize(payload)



    ### UNIMPLEMENTED CHATOP AND ADMIN COMMANDS

    @staticmethod
    def request_server_ban(character):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request server ban")

    @staticmethod
    def promote_chatop(character):
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "promote chatop")

    @staticmethod
    def request_alts(charater):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request alts")

    @staticmethod
    def admin_broadcast(message):
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "promote admin broadcast")

    @staticmethod
    def create_official_channel(channel):
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "create official channel")

    @staticmethod
    def demote_chatop(character):
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "demote chatop")

    @staticmethod
    def delete_channel(channel):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "delete channel")

    @staticmethod
    def request_character_server_ban(character):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request character server ban")

    @staticmethod
    def reload_server_config(save):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "reload server config")

    @staticmethod
    def reward_character(character):
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "reward character")

    @staticmethod
    def timeout_user(character, time, reason):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "timeout user from server")
    
    @staticmethod
    def unban_character_from_server(character):
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "unban character from server")


    client_commands = {
        "identify": (Priority.IMMEDIATE, "IDN"),
        "ping": (Priority.IMMEDIATE, "PIN"),
        "send_message": (Priority.RELAX, "MSG"),
        "join_channel": (Priority.RELAX, "JCH"),
        "create_private_channel": (Priority.RELAX, "CCR"),
        "get_channel_list": (Priority.RELAX, "CHA"),
        "channel_ops_list": (Priority.RELAX, "COL"),
        "search_characters_by_kinks": (Priority.RELAX, "FKS"),
        "ignore": (Priority.RELAX, "IGN"),
        "request_character_kinks": (Priority.RELAX, "KIN"),
        "leave_channel": (Priority.LAZY, "LCH"),
        "send_ad": (Priority.LAZY, "LRP"),
        "get_private_rooms_list": (Priority.RELAX, "ORS"),
        "send_private_message": (Priority.RELAX, "PRI"),
        "get_character_data": (Priority.RELAX, "PRO"),
        "roll_dice": (Priority.IMMEDIATE, "RLL"),
        "alert_admin": (Priority.RELAX, "SFC"),
        "set_status": (Priority.RELAX, "STA"),
        "typing_status": (Priority.RELAX, "TPN"),
        "request_uptime": (Priority.RELAX, "UPT"),

        ### CHANNEL OP STATUS REQUIRED COMMANDS
        "request_channel_banlist": (Priority.RELAX, "CBL"),
        "ban_character_from_channel": (Priority.IMMEDIATE, "CBU"),
        "change_channel_description": (Priority.RELAX, "CDS"),
        "invite_to_channel": (Priority.RELAX, "CIU"),
        "kick_character": (Priority.IMMEDIATE, "CKU"),
        "promote_channel_op": (Priority.RELAX, "COA"),
        "remove_channel_op": (Priority.IMMEDIATE, "COR"),
        "set_character_as_owner": (Priority.IMMEDIATE, "CSO"),
        "timeout_character": (Priority.IMMEDIATE, "CTU"),
        "unban_character": (Priority.IMMEDIATE, "CUB"),
        "set_channel_mode": (Priority.RELAX, "RMO"),
        "set_channel_visibility": (Priority.RELAX, "RST"),
        
        ### UNIMPLEMENTED CHATOP AND ADMIN COMMANDS
        "request_server_ban": (Priority.SKIP, "ACB"),
        "promote_chatop": (Priority.SKIP, "AOP"),
        "request_alts": (Priority.SKIP, "AWC"),
        "admin_broadcast": (Priority.SKIP, "BRO"),
        "create_official_channel": (Priority.SKIP, "CRC"),
        "demote_chatop": (Priority.SKIP, "DOP"),
        "delete_channel": (Priority.SKIP, "KIC"), # Might have ability to delete self-created channel
        "request_character_server_ban": (Priority.SKIP, "KIK"),
        "reload_server_config": (Priority.SKIP, "RLD"),
        "reward_character": (Priority.SKIP, "RWD"),
        "timeout_user": (Priority.SKIP, "TMO"),
        "unban_character_from_server": (Priority.SKIP, "UNB"),
    }

class AdminStatusRequired(Exception):
    def __init__(self, message, action=None):
        super().__init__(message)
        self.action = action

class ChatopStatusRequired(Exception):
    def __init__(self, message, action=None):
        super().__init__(message)
        self.action = action

