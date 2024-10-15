
class Channel:
    def __init__(self, channel_data):
        self.name = channel_data['channel']
        self.users =  channel_data['users']
        self.mode = channel_data['mode']

        self.visibility = "public" # ?