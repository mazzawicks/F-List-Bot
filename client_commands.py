
import inspect

class ClientCommands:
    def prioritize(payload):
        func_name = inspect.stack()[1].function
        priority, command = ClientCommands.client_commands[func_name]
        return priority, f"{command} {payload}"

    def identify(ticket):

        payload = {
            "method": "ticket",
            "account": "my_account",
            "ticket": ticket,
            "character": "mommy",
            "cname": "whatever this is",
            "cversion": "version cool",
        }
        # return 0, f"IDN {payload}"
        return ClientCommands.prioritize(payload)

    def ping():
        print('clientcommands ping')
        # return 0, "PIN"
        return ClientCommands.prioritize()

    def send_message():
        pass

    def join_channel():
        pass

    def create_private_channel():
        pass

    def get_channel_list():
        pass

    def channel_ops_list():
        pass

    def search_characters_by_kinks():
        pass

    def ignore():
        pass

    def request_character_kinks():
        pass

    def leave_channel():
        pass

    def send_ad():
        pass

    def get_private_rooms_list():
        pass

    def send_private_message():
        pass

    def get_character_data():
        pass

    def roll_dice():
        pass

    def alert_admin():
        pass

    def set_status():
        pass

    def typing_status():
        pass

    def request_uptime():
        pass


    ### CHANNEL OP STATUS REQUIRED COMMANDS

    def request_channel_banlist():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def ban_character_from_channel():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass


    def change_channel_description():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def invite_to_channel():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def kick_character():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def promote_channel_op():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass


    def remove_channel_op():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def set_character_as_owner():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        # only channel op? see if there are more up to date logs that distinguish between channel owner and moderator
        pass

    def timeout_character():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def unban_character():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def set_channel_mode():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def set_channel_visibility():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass

    def timeout_user():
        # Needs channel op
        # assert(.client.check_channel_op_status())
        pass


    ### UNIMPLEMENTED CHATOP AND ADMIN COMMANDS

    def request_server_ban():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request server ban")

    def promote_chatop():
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "promote chatop")

    def request_alts():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request alts")

    def admin_broadcast():
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "promote admin broadcast")

    def create_official_channel():
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "create official channel")

    def demote_chatop():
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "demote chatop")

    def delete_channel():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "delete channel")

    def request_character_server_ban():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "request character server ban")

    def reload_server_config():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "reload server config")

    def reward_character():
        raise AdminStatusRequired("Admin status is required for this command, this bot does not implement admin commands.", "reward character")

    def unban_character_from_server():
        raise ChatopStatusRequired("Chatop status is required for this command, this bot does not implement chatop commands.", "unban character from server")


    client_commands = {
        "identify": (0, "IDN"),
        "ping": (0, "PIN"),
        "send_message": (1, "MSG"),
        "join_channel": (1, "JCH"),
        "create_private_channel": (1, "CCR"),
        "get_channel_list": (1, "CHA"),
        "channel_ops_list": (1, "COL"),
        "search_characters_by_kinks": (1, "FKS"),
        "ignore": (1, "IGN"),
        "request_character_kinks": (1, "KIN"),
        "leave_channel": (1, "LCH"),
        "send_ad": (1, "LRP"),
        "get_private_rooms_list": (1, "ORS"),
        "send_private_message": (1, "PRI"),
        "get_character_data": (1, "PRO"),
        "roll_dice": (0, "RLL"),
        "alert_admin": (1, "SFC"),
        "set_status": (1, "STA"),
        "typing_status": (1, "TPN"),
        "request_uptime": (1, "UPT"),

        ### CHANNEL OP STATUS REQUIRED COMMANDS
        "request_channel_banlist": (1, "CBL"),
        "ban_character_from_channel": (0, "CBU"),
        "change_channel_description": (1, "CDS"),
        "invite_to_channel": (1, "CIU"),
        "kick_character": (0, "CKU"),
        "promote_channel_op": (1, "COA"),
        "remove_channel_op": (0, "COR"),
        "set_character_as_owner": (0, "CSO"),
        "timeout_character": (0, "CTU"),
        "unban_character": (0, "CUB"),
        "set_channel_mode": (1, "RMO"),
        "set_channel_visibility": (1, "RST"),
        "timeout_user": (0, "TMO"),
        
        ### UNIMPLEMENTED CHATOP AND ADMIN COMMANDS
        "request_server_ban": (-1, "ACB"),
        "promote_chatop": (-1, "AOP"),
        "request_alts": (-1, "AWC"),
        "admin_broadcast": (-1, "BRO"),
        "create_official_channel": (-1, "CRC"),
        "demote_chatop": (-1, "DOP"),
        "delete_channel": (-1, "KIC"), # Might have ability to delete self-created channel
        "request_character_server_ban": (-1, "KIK"),
        "reload_server_config": (-1, "RLD"),
        "reward_character": (-1, "RWD"),
        "unban_character_from_server": (-1, "UNB"),
    }

class AdminStatusRequired(Exception):
    def __init__(self, message, action=None):
        super().__init__(message)
        self.action = action

class ChatopStatusRequired(Exception):
    def __init__(self, message, action=None):
        super().__init__(message)
        self.action = action