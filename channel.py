
from enum import Enum
from client_commands import ClientCommands


class Channel:
    def __init__(self, command, channel_data):
        # self.id = channel_data['channel']
        # self.title = channel_data['title']
        # self.users =  channel_data['users']
        # self.description = channel_data['description']
        # self.channel_ops = []

        # self.mode = channel_data['mode']
        # self.visibility = visibility

        # self.messages = []


# channel_description CDS
# "CDS {\"description\":\"This is a room dedicated to the kinkiest, most \\\"out there\\\" kinds of transformation there are.\",\"channel\":\"ADH-44e91ecfb4116365ad80\"}"
        self.description

# public_channel_list CHA
# "CHA {\"channels\":[{\"name\":\"Gamers\",\"mode\":\"chat\",\"characters\":143},
        self.name
        self.mode
        self.characters
        self.visibility = Visibility.PUBLIC


# private_rooms_list ORS
# "ORS {\"channels\":[{\"name\":\"ADH-6a58888a85642950e263\",\"title\":\"Loose Canons\",\"characters\":28},
        self.name
        self.title
        self.characters
        self.visibility = Visibility.OPEN_PRIVATE

# channel_data ICH
# "ICH {\"channel\":\"ADH-9a88bd5138c97acf6983\",\"mode\":\"chat\",\"users\":[{\"identity\":\"Jasper the Kobold\"},
        self.channel
        self.mode
        self.users

# character_left_channel LCH

# channel_message MSG

# invited_to_channel CIU

        # self.visibility = ?

# promoted_channel_op COA

# removed_channel_op COR

    def message(self, character, message):
        if self.should_save(character, message):
            self.messages.append(message)
            self.character_messages[character].append(message)

    def should_save(self, character, message):
        return True
    
# channel_ops_list COL
    
# "COL {\"oplist\":[\"Domenique Hunter\",\"Officer Taylor\",\"Troya Williams\",\"Hiira\",\"H-Milk\",\"Miriam Stallion\"],\"channel\":\"ADH-3c2b46e569b842f2e75f\"}"

    async def get_channel_ops(self):
        # As with all commands that refer to a specific channel, official/public channels use the name, but unofficial/private/open private rooms use the channel ID, which can be gotten from ORS.
        ops = await ClientCommands.channel_ops_list(self.name_or_id())
        self.op_list = ops['oplist']

    
# channel_mode_changed RMO

    def name_or_id(self):
        self.name if self.visibility == Visibility.PUBLIC else self.id



class Visibility(Enum):
    PUBLIC = 0
    OPEN_PRIVATE = 1
    CLOSED_PRIVATE = 2