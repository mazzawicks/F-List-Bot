import json
from priority import Priority

from client_commands import ClientCommands

import logging
log = logging.getLogger('main')

class ServerCommands:
    @staticmethod
    def read_message(msg):
        if len(msg) < 3:
            return Priority.SKIP, f"Message too short: {msg}"
        #All commands look like this:
        # XXX {"property":"value","anotherproperty":"value"}
        command = msg[:3]
        if command not in ServerCommands.all_commands:
            return Priority.SKIP, f"Unrecognized command: {command}"

        payload = msg[3:] #Commands without a json payload should not contain a trailing space after the message type
        log.info(f'command {command}, payload {payload}, len {len(payload)}')
        if len(msg) > 4:
            try:
                payload = json.loads(msg[4:])
            except json.JSONDecodeError:
                log.warning(f'Bad JSON from server: {msg}')
                return Priority.SKIP, f"Bad JSON"

        log.info(f'servercommands read {command}, {payload}')
        priority, out_message = ServerCommands.server_commands[command](payload)
        return priority, out_message
    
    ###
    # different server commands require different actions
    # grouping them:
    # - data commands, usually replies from initial client commands request
    # - interaction commands, another user did something that might require attention
    # - room commands, confirmation of requests for joining, leaving, creating, etc
    # - confirmation for mod commands
    # - Identify and Ping, important ones to pay attention to
    # - RTB, real-time bridge - notes, friend requests maybe? outside chat actions
    #     might be more than note, need to see what else it includes
    ### 
    # other notes:
    # - some commands may be paginated, or otherwise related to other commands 
    #     being received
    # - CHA, ORS are important to map room names and IDs
    # - RLL, response to rolls
    # - VAR and SYS - apparently some more free-form datastructures that need their own parsing
    ###
    # priority:
    # - ACK will be for messages containing data that requires no immediate response.
    #     This data can be passed along to whatever form of state the bot will 
    #     maintain. For now, it's also a good way to pass something along in the 
    #     correct format to not create an exception.
    # - SKIP is for errors that should not be processed. If I find no other use for 
    #     it, maybe I'll rename it to errored. Doesn't make as much sense as a 
    #     Priority enum element though.
    # - Immediate and relax serve to separate messages that need to cut ahead and 
    #     those that should just be processed soon.
    # - Lazy, I haven't actually found a use for yet, but perhaps one will come up.


    @staticmethod
    def identified(payload):
        log.info('servercommands identified')
        return ClientCommands.identify(payload) # backwards right now, ClientCommands is called first and server responds. Should actually handle response confirmation

    @staticmethod
    def ping(payload=None):
        log.info(f'servercommands ping: {payload}')
        return ClientCommands.ping(payload)

    @staticmethod
    def private_message(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def channel_message(payload):
        # character = payload['character']
        # message = payload['message']
        # channel = payload['channel']
        log.info('servercommands msg')
        return Priority.ACK, "Method not implemented yet"
    
    @staticmethod
    def chatops_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def promoted_chatop(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def admin_broadcast(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def channel_description(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def public_channel_list(payload):
        log.info('servercommands pub channel list')

    @staticmethod
    def invited_to_channel(payload):
        log.info('servercommands invited')
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_banned(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_kicked(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def promoted_channel_op(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def channel_ops_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def connected(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def removed_channel_op(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_set_as_owner(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_timed_out(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def demoted_chatop(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def error_occurred(payload):
        log.warning('error occured')
        log.warning(payload)

    @staticmethod
    def character_kink_search_response(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def logged_out(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def hello_response(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def channel_data(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_joined(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def kinks_data(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_left_channel(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_connected(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def ignore_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def friends_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def private_rooms_list(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def profile_data(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def roleplay_ad_message(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def dice_result(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def channel_mode_changed(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def received_note(payload):
        # might be more than note, need to see what else it includes
        # probably friend requests, maybe bookmarks joining/leaving
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def admin_issue(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_status(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def system_message(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def character_typing(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def uptime(payload):
        return Priority.ACK, "Method not implemented yet"

    @staticmethod
    def server_variables(payload):
        return Priority.ACK, "Method not implemented yet"


    server_commands = {
        "ADL": chatops_list,
        "AOP": promoted_chatop,
        "BRO": admin_broadcast,
        "CDS": channel_description,
        "CHA": public_channel_list,
        "CIU": invited_to_channel,
        "CBU": character_banned,
        "CKU": character_kicked,
        "COA": promoted_channel_op,
        "COL": channel_ops_list,
        "CON": connected,
        "COR": removed_channel_op,
        "CSO": character_set_as_owner,
        "CTU": character_timed_out,
        "DOP": demoted_chatop,
        "ERR": error_occurred,
        "FKS": character_kink_search_response,
        "FLN": logged_out,
        "HLO": hello_response,
        "ICH": channel_data,
        "IDN": identified,
        "JCH": character_joined,
        "KID": kinks_data,
        "LCH": character_left_channel,
        "LIS": character_list,
        "NLN": character_connected,
        "FRL": friends_list,
        "ORS": private_rooms_list,
        "PIN": ping,
        "PRD": profile_data,
        "PRI": private_message,
        "MSG": channel_message,
        "LRP": roleplay_ad_message,
        "RLL": dice_result,
        "RMO": channel_mode_changed,
        "RTB": received_note,
        "SFC": admin_issue,
        "STA": character_status,
        "SYS": system_message,
        "TPN": character_typing,
        "UPT": uptime,
        "VAR": server_variables,
    }

    all_commands = server_commands.keys()

