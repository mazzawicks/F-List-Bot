import logging
log = logging.getLogger('main')

class State:
    def __init__(self, config):
        self.current_channels = []
        self.config = config
        self.op_channels = self.config['channel_op']
        # self.players
        # self.messages

    def join_channel(self, channel):
        self.current_channels.add(channel)

    def leave_channel(self, channel):
        try:
            self.current_channels.remove(channel)
        except ValueError:
            log.warning(f"Tried to leave channel we're not in: {channel}")

    def is_channel_op(self, channel):
        return channel in self.op_channels
    
class BotState(State):
    def __init__(self, config):
        super().__init__(config)

    @classmethod
    def is_channel_op(cls, channel):
        return channel in cls.op_channels