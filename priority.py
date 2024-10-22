from enum import Enum

class Priority(Enum):
    ACK = -2        # Message Acknowledged, no response necessary
    SKIP = -1       # Do not process message
    IMMEDIATE = 0   # Process immediately - Reserved for Identify
    PING = 1        # Process before everything except Identify
    RELAX = 20      # Process when nothing more important in queue
    LAZY = 30       # Process last

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value