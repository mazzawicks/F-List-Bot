
import os


greeting = '''
*******************************************************

Hello! This interactive script will ask you a series of questions and then create what's called an environment file. You can exit at any time by pressing Ctrl+C. The file generated will contain all the environment variables you'll need to use this bot. If you are familiar with these, there is an example .env in the repo so you can make your own instead of using this script if you desire.

You should also be aware that F-List has several rules that must be followed to avoid action against your bot, and even your account. The full rules can be found here: https://wiki.f-list.net/index.php?title=F-Chat_Protocol, or in the `docs` folder of this repo. Here's a summary of important ones to point out though:

- Your bot must not enter rooms to which it has not been explicitly allowed by the channel owner.*

- Your bot must not send PMs, friend requests, or channel invites to a user unless requested by the user through some user-initiated contact with the bot. (Like PMing the bot or using trigger commands in a channel.)*

- The character your bot operates on must contain a notice that the character is a chat bot, a brief summary of its intended purpose/functionality, and a name/link to the character who operates the bot on the profile page for the character.

- Your bot must not use the looking status.

- The character your bot operates on must only contain custom kinks so that it will not show in the chat search system.
 
- Your bot must not post advertisements in public channels without the consent of site staff or private channels without the consent of the private channel owner.*

- Misuse of user data, including spying on inter-character interactions without consent, will be subject to disciplinary action and may lead to suspension of bot privileges.

- Your bot must conform to the site's Privacy Policy regarding third-party bots. Found here: https://www.f-list.net/doc/privacy.php


* Some caveats and exceptions - Read the rules in full!
Press enter to continue.
'''

username_q = '''
*******************************************************

Now then, first question: 
What is your account's username? This is not the name of a character, it is the username the bot will use to log in to f-list.

'''

password_q = '''
*******************************************************

Next, what is the password to that account? Unfortunately this is required to log in. As far as I know you may use a separate f-list account so long as the bot's profile links back to its owner. The code in this repo will send the password only to f-list and nowhere else, and store it only in the file generated at the end of this script. You're welcome to encrypt the file for storage, but unfortunately f-list's API requires a plaintext password.

'''

character_q = '''
*******************************************************

What is the name of the character this bot will run on? As mentioned earlier, it should be a character used soley for this purpose, ideally a fresh one.

'''

join_channels_q = '''
*******************************************************

What channels would you like the bot to join immediately once it logs in? Do keep in mind the rules about what rooms bots are allowed in. You can enter the names of the rooms as a comma-separated list, or leave this blank. You can also have the bot join rooms at any time by inviting it through f-list's /invite command.

'''

channel_op_q = '''
*******************************************************

Are there any channels your bot is a channel op in? You can customize how the bot uses moderator powers. Enter the name or names of these channels as a comma-separated list, or leave this blank.

'''

# filepath_q = '''
# *******************************************************
# 
# Finally, where would you like your environment file to be created? It's recommended to keep it at the root of your project folder.
# '''

class QA:
    def __init__(self, name, answer):
        self.name = name
        self.answer = answer

    def config_str(self):
        return f"{self.name}=\"{self.answer}\"\n"

_ = input(greeting)

qas = [
    QA("username", input(username_q)),
    QA("password", input(password_q)),
    QA("character", input(character_q)),
    QA("join_channels", input(join_channels_q)),
    QA("channel_op", input(channel_op_q)),
]

# filepath = input(filepath_q)
filepath = os.getcwd()

with open(f"{filepath}/.env", 'w') as f:
    for qa in qas:
        f.write(qa.config_str())

