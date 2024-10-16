from enum import Enum

class Priority(Enum):
    ACK = -2        # Message Acknowledged, no response necessary
    SKIP = -1       # Do not process message
    IMMEDIATE = 0   # Process immediately
    RELAX = 1       # Process when nothing IMMEDIATE in queue
    LAZY = 2        # Process last
