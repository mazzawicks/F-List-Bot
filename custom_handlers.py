


from events import Handler

from actions import Actions


class ReplyFive(Handler):
    def handle(self, event):
        if event.type == "message" and event.payload[0] == "!":
            # ClientCommands.send_message
            Actions.send_message(f"High five {event.character}!")

high_five = ReplyFive()

def high_five(message, character, channel):
    if message[0] == "!":
        Actions.send_message(channel, f"High five {character}!")

custom_handlers = {
    "on_message": [high_five]
}