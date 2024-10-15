from client_commands import ClientCommands

import logging
log = logging.getLogger('main')

class ServerCommands:
    def read(command, payload=None):
        print(f'servercommands read {command}, {payload}')
        return ServerCommands.server_commands[command](payload)

    def get_commands():
        return ServerCommands.server_commands.keys()

    def identified(payload):
        print('servercommands identified')
        return ClientCommands.identify(payload) # backwards right now, ClientCommands is called first

    def ping(payload=None):
        print('servercommands ping')
        return ClientCommands.ping()

    def chatops_list(payload):
        pass

    def promoted_chatop(payload):
        pass

    def admin_broadcast(payload):
        pass

    def channel_description(payload):
        pass

    def public_channel_list(payload):
        pass

    def invited_to_channel(payload):
        pass

    def character_banned(payload):
        pass

    def character_kicked(payload):
        pass

    def promoted_channel_op(payload):
        pass

    def channel_ops_list(payload):
        pass

    def connected(payload):
        pass

    def removed_channel_op(payload):
        pass

    def character_set_as_owner(payload):
        pass

    def character_timed_out(payload):
        pass

    def demoted_chatop(payload):
        pass

    def error_occurred(payload):
        pass

    def character_kink_search_response(payload):
        pass

    def logged_out(payload):
        pass

    def hello_response(payload):
        pass

    def channel_data(payload):
        pass

    def character_joined(payload):
        pass

    def kinks_data(payload):
        pass

    def character_left_channel(payload):
        pass

    def character_list(payload):
        pass

    def character_connected(payload):
        pass

    def ignore_list(payload):
        pass

    def friends_list(payload):
        pass

    def private_rooms_list(payload):
        pass

    def profile_data(payload):
        pass

    def private_message(payload):
        pass

    def channel_message(payload):
        pass

    def roleplay_ad_message(payload):
        pass

    def dice_result(payload):
        pass

    def channel_mode_changed(payload):
        pass

    def received_note(payload):
        pass

    def admin_issue(payload):
        pass

    def character_status(payload):
        pass

    def system_message(payload):
        pass

    def character_typing(payload):
        pass

    def uptime(payload):
        pass

    def server_variables(payload):
        pass


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
