import json
from priority import Priority

# from client_commands import ClientCommands
from events import Events

import logging
log = logging.getLogger('main')

class ServerCommands:
    @staticmethod
    def read_message(msg):
        if len(msg) < 3:
            return Priority.SKIP, f"Message too short: {msg}"
        # All commands look like this:
        # XXX {"property":"value","anotherproperty":"value"}
        command = msg[:3]
        if command not in ServerCommands.all_commands:
            log.warning(f"Unrecognized command: {command}")
            return
            # return Priority.SKIP, f"Unrecognized command: {command}"

        payload = msg[3:] #Commands without a json payload should not contain a trailing space after the message type
        log.info(f'command {command}, payload {payload[:20]}, len {len(payload)}')
        if len(msg) > 4:
            try:
                payload = json.loads(msg[4:])
            except json.JSONDecodeError:
                log.warning(f'Bad JSON from server: {msg}')
                return
                # return Priority.SKIP, f"Bad JSON"

        log.info(f'servercommands read {command}, {payload[:20]}')
        # ServerCommands.server_commands[command](payload)
        ServerCommands.create_event(command, payload)
        return 
        # priority, out_message = ServerCommands.server_commands[command](payload)
        # return priority, out_message

    @staticmethod
    def create_event(command, payload):
        command_name = ServerCommands.server_commands[command]
        getattr(Events, command_name)(*payload)

    server_commands = {
        "ADL": "chatops_list",
        "AOP": "promoted_chatop",
        "BRO": "admin_broadcast",
        "CDS": "channel_description",
        "CHA": "public_channel_list",
        "CIU": "invited_to_channel",
        "CBU": "character_banned",
        "CKU": "character_kicked",
        "COA": "promoted_channel_op",
        "COL": "channel_ops_list",
        "CON": "connected",
        "COR": "removed_channel_op",
        "CSO": "character_set_as_owner",
        "CTU": "character_timed_out",
        "DOP": "demoted_chatop",
        "ERR": "error_occurred",
        "FKS": "character_kink_search_response",
        "FLN": "logged_out",
        "HLO": "hello_response",
        "ICH": "channel_data",
        "IDN": "identified",
        "JCH": "character_joined",
        "KID": "kinks_data",
        "LCH": "character_left_channel",
        "LIS": "character_list",
        "NLN": "character_connected",
        "IGN": "ignore_list",
        "FRL": "friends_list",
        "ORS": "private_rooms_list",
        "PIN": "ping",
        "PRD": "profile_data",
        "PRI": "private_message",
        "MSG": "channel_message",
        "LRP": "roleplay_ad_message",
        "RLL": "dice_result",
        "RMO": "channel_mode_changed",
        "RTB": "received_note",
        "SFC": "admin_issue",
        "STA": "character_status",
        "SYS": "system_message",
        "TPN": "character_typing",
        "UPT": "uptime",
        "VAR": "server_variables",
    }

    all_commands = server_commands.keys()




    # @staticmethod
    # def identified(payload):
    #     log.info('servercommands identified')
    #     Events.identified(payload)

    # @staticmethod
    # def ping(payload=None):
    #     Events.ping()

    # @staticmethod
    # def channel_message(payload):
    #     character = payload['character']
    #     message = payload['message']
    #     channel = payload['channel']
    #     log.info('servercommands msg')
    #     Events.channel_message(character, message, channel)

    # @staticmethod
    # def private_message(payload):
    #     character, message, recipient = payload
    #     Events.private_message(character, message)
    
    # @staticmethod
    # def chatops_list(payload):
    #     chatops = payload['ops']
    #     Events.chatops(chatops)

    # @staticmethod
    # def promoted_chatop(payload):
    #     character = payload['character']
    #     Events.promoted_chatop(character)

    # @staticmethod
    # def admin_broadcast(payload):
    #     message = payload['message']
    #     Events.broadcast(message)

    # @staticmethod
    # def channel_description(payload):
    #     channel, description = payload
    #     Events.channel_description(channel, description)

    # @staticmethod
    # def public_channel_list(payload):
    #     channels = payload['channels']
    #     Events.public_channel_list(channels)
    #     log.info('servercommands pub channel list')

    # @staticmethod
    # def invited_to_channel(payload):
    #     sender, title, name = payload
    #     log.info('servercommands invited')
    #     Events.invited_to_channel(sender, title, name)

    # @staticmethod
    # def character_banned(payload):
    #     operator, channel, character = payload
    #     Events.character_banned(operator, channel, character)

    # @staticmethod
    # def character_kicked(payload):
    #     operator, channel, character = payload
    #     Events.character_kicked(operator, channel, character)

    # @staticmethod
    # def promoted_channel_op(payload):
    #     character, channel = payload
    #     Events.promoted_channel_op(character, channel)

    # @staticmethod
    # def channel_ops_list(payload):
    #     channel, oplist = payload
    #     Events.channel_ops_list(channel, oplist)

    # @staticmethod
    # def connected(payload):
    #     count = payload['count']
    #     Events.connected(count)

    # @staticmethod
    # def removed_channel_op(payload):
    #     character, channel = payload
    #     Events.removed_channel_op(character, channel)

    # @staticmethod
    # def character_set_as_owner(payload):
    #     character, channel = payload
    #     Events.character_set_as_owner(character, channel)

    # @staticmethod
    # def character_timed_out(payload):
    #     operator, channel, length, character = payload
    #     Events.character_timed_out(operator, channel, length, character)

    # @staticmethod
    # def demoted_chatop(payload):
    #     character = payload['character']
    #     Events.demoted_chatop(character)

    # @staticmethod
    # def error_occurred(payload):
    #     number, message = payload
    #     log.warning('F-list error #{number} occured: {message}')
    #     Events.error_occurred(number, message)
    #     log.warning(payload)

    # @staticmethod
    # def character_kink_search_response(payload):
    #     characters, kinks = payload
    #     Events.character_kink_search_response(characters, kinks)

    # @staticmethod
    # def logged_out(payload):
    #     character = payload["character"]
    #     Events.logged_out(character)

    # @staticmethod
    # def hello_response(payload):
    #     message = payload["message"]
    #     Events.hello_response(message)

    # @staticmethod
    # def channel_data(payload):
    #     users, channel, mode = payload
    #     Events.channel_data(users, channel, mode)

    # @staticmethod
    # def character_joined(payload):
    #     channel, character, title = payload
    #     Events.character_joined(character, channel, title)

    # @staticmethod
    # def kinks_data(payload):
    #     type = payload["type"]
    #     message = payload.get("message") 
    #     key = payload.get("key") 
    #     value = payload.get("value")
    #     Events.kinks_data(type, message, key, value)

    # @staticmethod
    # def character_left_channel(payload):
    #     channel, character = payload
    #     Events.character_left_channel(channel, character)

    # @staticmethod
    # def character_list(payload):
    #     characters = payload["characters"]
    #     Events.character_list(characters)

    # @staticmethod
    # def character_connected(payload):
    #     identity, gender, status = payload
    #     Events.character_connected(identity, gender, status)

    # @staticmethod
    # def ignore_list(payload):
    #     action = payload["action"]
    #     characters = payload.get("characters")
    #     character = payload.get("character")
    #     Events.ignore_list(action, characters, character)

    # @staticmethod
    # def friends_list(payload):
    #     characters = payload["characters"]
    #     Events.friends_list(characters)

    # @staticmethod
    # def private_rooms_list(payload):
    #     channels = payload["channels"]
    #     Events.private_rooms_list(channels)

    # @staticmethod
    # def profile_data(payload):
    #     type = payload["type"]
    #     message = payload.get("message") 
    #     key = payload.get("key") 
    #     value = payload.get("value")
    #     Events.profile_data(type, message, key, value)

    # @staticmethod
    # def roleplay_ad_message(payload):
    #     channel, message, character = payload
    #     Events.roleplay_ad_message(channel, message, character)

    # @staticmethod
    # def dice_result(payload):
    #     channel, type, message, character = payload
    #     if type == "dice":
    #         results, rolls, endresult = payload
    #         Events.dice_result(channel, message, character, results, rolls, endresult)
    #     if type == "bottle":
    #         target = payload['target']
    #         Events.bottle_result(channel, message, character, target)

    # @staticmethod
    # def channel_mode_changed(payload):
    #     mode, channel = payload
    #     Events.channel_mode_changed(mode, channel)

    # @staticmethod
    # def received_note(payload):
    #     type, character = payload
    #     # might be more than note, need to see what else it includes
    #     # probably friend requests
    #     Events.received_note(type, character)

    # @staticmethod
    # def admin_issue(payload):
    #     action, moderator, character, timestamp = payload
    #     Events.admin_issue(action, moderator, character, timestamp)

    # @staticmethod
    # def character_status(payload):
    #     status, character, statusmsg = payload
    #     Events.character_status(status, character, statusmsg)

    # @staticmethod
    # def system_message(payload):
    #     message = payload['message']
    #     channel = payload.get('channel')
    #     Events.system_message(message, channel)

    # @staticmethod
    # def character_typing(payload):
    #     character, status = payload
    #     Events.character_typing(character, status)

    # @staticmethod
    # def uptime(payload):
    #     time, startime, startstring, accepted, channels, users, maxusers = payload
    #     Events.uptime(time, startime, startstring, accepted, channels, users, maxusers)

    # @staticmethod
    # def server_variables(payload):
    #     value, variable = payload
    #     Events.server_variables(value, variable)


    # server_commands = {
        # "ADL": chatops_list,
        # "AOP": promoted_chatop,
        # "BRO": admin_broadcast,
        # "CDS": channel_description,
        # "CHA": public_channel_list,
        # "CIU": invited_to_channel,
        # "CBU": character_banned,
        # "CKU": character_kicked,
        # "COA": promoted_channel_op,
        # "COL": channel_ops_list,
        # "CON": connected,
        # "COR": removed_channel_op,
        # "CSO": character_set_as_owner,
        # "CTU": character_timed_out,
        # "DOP": demoted_chatop,
        # "ERR": error_occurred,
        # "FKS": character_kink_search_response,
        # "FLN": logged_out,
        # "HLO": hello_response,
        # "ICH": channel_data,
        # "IDN": identified,
        # "JCH": character_joined,
        # "KID": kinks_data,
        # "LCH": character_left_channel,
        # "LIS": character_list,
        # "NLN": character_connected,
        # "IGN": ignore_list,
        # "FRL": friends_list,
        # "ORS": private_rooms_list,
        # "PIN": ping,
        # "PRD": profile_data,
        # "PRI": private_message,
        # "MSG": channel_message,
        # "LRP": roleplay_ad_message,
        # "RLL": dice_result,
        # "RMO": channel_mode_changed,
        # "RTB": received_note,
        # "SFC": admin_issue,
        # "STA": character_status,
        # "SYS": system_message,
        # "TPN": character_typing,
        # "UPT": uptime,
        # "VAR": server_variables,
    # }

    # all_commands = server_commands.keys()

