
import asyncio
from asyncio import Queue, PriorityQueue
from collections import defaultdict

class EventQueue: # EventActionQueue?
    def __init__(self):
        self.event_queue = PriorityQueue() # change back to PriorityQueue
        self.action_queue = PriorityQueue()
        self.handlers = defaultdict(list)
        self.has_login_tasks = False # move this to state so handlers can access it

    def add_handler(self, event_type, event_handler):
        self.handlers[event_type].append(event_handler)

    def add_handlers(self, event_handlers):
        for event_type in event_handlers.keys():
            self.handlers[event_type].extend(event_handlers[event_type])

    def get_handlers(self):
        return self.handlers

    # Called by ServerCommands.read_message
    def put_event(self, event):
        self.event_queue.put(event)

    # Called by Events
    async def get_event(self):
        return await self.event_queue.get()
    
    # Called by Actions
    async def put_action(self, action):

        print(f"!!!! put_action {action}")
        await self.action_queue.put(action)

    # Called by Client
    async def get_action(self):
        return await self.action_queue.get()

    async def handle_events(self):
        async def event_watcher():
            while True:
                event = await self.event_queue.get()

                async for handler in self.handlers:
                    await handler.handle(self.action_queue, event)

                asyncio.sleep(.1)

        # async def action_sender():
        #     while True:
        #         await self.action_queue.put()

        #         # async for handler in self.handlers:
        #         #     await handler.handle(self.action_queue, event)

                asyncio.sleep(.1)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(event_watcher())
            # tg.create_task(action_sender())

    ###
    # TODO: start Task from ClientCommands, Task done by receiving matching ServerCommand(s)
    # 
    # different server messages require different actions
    # grouping them:
    # - data messages, usually replies from initial client commands request
    # - interaction messages, another user did something that might require attention
    # - confirmation messages
    # - server messages
    ###
    # - Identify - confirmation
    # - Ping - must reply to
    # - RTB, real-time bridge - notes, friend requests maybe? outside chat actions
    #     might be more than note, need to see what else it includes
    # - LIS - paginated, total chars matches CON
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
