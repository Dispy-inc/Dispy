"""
Dispy is a light-weight discord API library.
It is recommended to import it with `from dispy import *`
"""
# Internal
from dispy.modules.intents import *
from dispy.modules import *
import dispy.types.user as types
from dispy.modules.rest_api import __internal__ as restapi
from dispy.modules.error import error
from dispy.data import data
# External
from typing import Callable, List, Union, Literal
from concurrent.futures import ThreadPoolExecutor
import aiohttp # Need to be installed (with websocket_client)
import json
import threading
import time
import asyncio

# 888888ba  oo                               
# 88    `8b ``                               
# 88     88 dP .d8888b.    88d888b. dP    dP 
# 88     88 88 Y8ooooo.    88'  `88 88    88 
# 88    .8P 88       88 ,, 88.  .88 88.  .88 
# 8888888P  dP `88888P' 88 88Y888P' `8888P88 
#                          88            .88 
#                          dP        d8888P  

# Developed by ✯James French✯ with ❤ and hopes x)
# Licensed with GPLv3

class Bot(restapi): # <- this shit has taken me hours
    #--------------------------------------------------------------------------------------#
    #                                      Bot Setup                                       #
    #--------------------------------------------------------------------------------------# 
    def __init__(self,token=None):
        """
        Define your bot.

        See related page on the [wiki](https://jamesfrench.gitbook.io/dispy).
        """
        self.user: types.User = None
        self.status = 0

        self._token = token
        self._error = error()
        self._heartbeat_interval = None
        self._handlers = []
        self._session: aiohttp.ClientSession = None
        self._ws = None
        self._api = restapi(self._token,self._error)
        self._loop = asyncio.new_event_loop()
        self._executor = ThreadPoolExecutor()
        self._tasks = []
        self._data = data()
        threading.Thread(target=self.run_loop, daemon=True).start()
    def run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever() # no_traceback

    def __getattr__(self, name):
        return getattr(self._api, name)

    def config(self,token=None):
        if self.status != 0: return None
        if token != None: self._token = token

    #--------------------------------------------------------------------------------------#
    #                                    Internal Code                                     #
    #--------------------------------------------------------------------------------------#
    # MAIN: Run the bot and get events
    async def _main(self):
        """
        Don't use it if you don't know what you're doing.
        """
        async for msg in self._ws:
            data = json.loads(msg.data)
    
            if data['op'] == 10: # Identification and heartbeat set
                self._heartbeat_interval = data['d']['heartbeat_interval'] / 1000
                asyncio.create_task(self._heartbeat())
    
                await self._identify()
            else: # Events
                if data['t'] != None:
                    if data['t'] == "READY":
                        self.user = types.User(**data['d']['user'])
                    asyncio.create_task(self._sendevent(data['t'],data['d']))

    # Used to call functions when a event is dispatched
    async def _sendevent(self,eventname,args):
        """
        Don't use it if you don't know what you're doing.
        """
        once_remove = []
    
        for key, handler in self._handlers:
            if key == eventname:
                if eventname in self._data.intents.direct_intents_opposed:
                    if handler['is_direct'] and 'guild_id' in args: continue
                    if not handler['is_direct'] and 'guild_id' not in args: continue
    
                arguments = self._arguments_handler(args,eventname)
                thread = asyncio.to_thread(handler['function'](**arguments))
                asyncio.run_coroutine_threadsafe(thread, loop=self._loop)
    
                if handler.get('once', False):
                    once_remove.append((key,handler))
    
        for key, handler in once_remove:
            self._handlers.remove((key, handler))

    # Make the bot online
    async def _identify(self):
        """
        Don't use it if you don't know what you're doing.
        """
        payload = {
                    'op': 2,
                    'd': {
                        'token': self._token,
                        'intents': self._intents(),
                        'properties': {
                            'os': 'linux',
                            'browser': 'dispy-lib',
                            'device': 'dispy-lib'
                        }
                    }
                }
        await self._ws.send_json(payload)

    # Send heartbeat to discord to keep the bot alive
    async def _heartbeat(self):
        """
        Don't use it if you don't know what you're doing.
        """
        while self.status == 1: 
            await asyncio.sleep(self._heartbeat_interval)
            if self.status != 1:
                break
            heartbeat_payload = {
                "op": 1,
                "d": 'null'
            }
            await self._ws.send_json(heartbeat_payload)

    # Used to calculate intents
    def _intents(self):
        """
        Don't use it if you don't know what you're doing.
        """
        events = set()
        ids = []
        for key, handler in self._handlers:
            event_name = f'DIRECT_{key}' if handler['is_direct'] else key
            events.add(event_name)  # Add event name to the set
        
        ids = [id for event in events if (intent_found := self._data.intents.get_intents(event)) for id in intent_found]  # List comprehension
        return sum(1 << int(id) for id in ids)

    # Give a different amount of arguments depending on the event
    def _arguments_handler(self,arguments,eventname,check=False):
        """
        Don't use it if you don't know what you're doing.
        """
        if eventname == "READY":
            return {}
        elif eventname in self._data.intents.get_child(9)+self._data.intents.get_child(12):
            user = User(**arguments['author']) if check == False else User()
            arguments.pop('author',{})
            msg = Message(**arguments,api_=self._api)
            return {"msg": msg, "user": user}
        else:
            return {"args":dict_to_obj(arguments)} if check == False else {"args":None}
    
    # Check args on a user function
    def _check_handler(self,function,eventname):
        """
        Don't use it if you don't know what you're doing.
        """
        function_code = function.__code__
        function_arguments = list(function_code.co_varnames[:function_code.co_argcount])
        event_arguments = self._arguments_handler({},eventname,True)
        stringcode = []
        if not function_arguments == list(event_arguments.keys()):
            for name, obj in event_arguments.items():
                obj_type = type(obj).__name__
                if obj_type.startswith('Partial'):
                    obj_type = obj_type[7:]
                stringcode.append(f"{name}: {obj_type}")
            self._error.summon('function_invalid',function_name=function.__name__,arguments=", ".join(stringcode))
        else:
            return True
        
    # Start the bot
    async def _start(self):
        self._session = aiohttp.ClientSession()
        try:
            async with self._session.ws_connect('wss://gateway.discord.gg/?v=10&encoding=json') as ws:
                self._ws = ws
                await self._main()
        finally:
            await self._session.close()
        return None

    #--------------------------------------------------------------------------------------#
    #                                     Bot Control                                      #
    #--------------------------------------------------------------------------------------#
    def run(self) -> None:
        """
        Start your bot and make it online.
        Make your bot capable of receiving events and sending events.
        """
        if self.status != 0: self._error.summon('bot_is_already_running')
        self.status = 1
        
        asyncio.run(self._start()) # no_traceback
        time.sleep(2)

    def _stop(self) -> None: # (EXPERIMENTAL)
        """
        Shutdown the bot. (EXPERIMENTAL)
        """
        async def _stop():
            if self._ws:
                await self._ws.close(code=1000)
            if self._session:
                await self._session.close()

        asyncio.run_coroutine_threadsafe(_stop(),loop=self._loop)

    def _debug(self):
        pass

    #--------------------------------------------------------------------------------------#
    #                                    Event Handler                                     #
    #--------------------------------------------------------------------------------------#

    global _eventliteral
    _eventliteral = Literal["GUILD_BAN_ADD", "MESSAGE_UPDATE", "GUILD_CREATE", "DIRECT_MESSAGE_REACTION_REMOVE_ALL", "GUILD_ROLE_CREATE", "GUILD_SCHEDULED_EVENT_CREATE", "GUILD_DELETE", "GUILD_SCHEDULED_EVENT_UPDATE", "ALL", "MESSAGE_REACTION_REMOVE_ALL", "GUILD_MEMBER_REMOVE", "INVITE_DELETE", "STAGE_INSTANCE_CREATE", "DIRECT_CHANNEL_PINS_UPDATE", "CHANNEL_DELETE", "GUILD_ROLE_UPDATE", "DIRECT_MESSAGE_CREATE", "DIRECT_MESSAGE_REACTION_REMOVE_EMOJI", "MESSAGE_DELETE_BULK", "THREAD_UPDATE", "MESSAGE_POLL_VOTE_REMOVE", "GUILD_SOUNDBOARD_SOUND_DELETE", "VOICE_STATE_UPDATE", "GUILD_INTEGRATIONS_UPDATE", "USER_UPDATE", "GUILD_ROLE_DELETE", "MESSAGE_REACTION_REMOVE", "DIRECT_MESSAGE_UPDATE", "MESSAGE_DELETE", "GUILD_SCHEDULED_EVENT_DELETE", "THREAD_MEMBER_UPDATE", "PRESENCE_UPDATE", "INTEGRATION_UPDATE", "GUILD_SOUNDBOARD_SOUND_CREATE", "WEBHOOKS_UPDATE", "GUILD_AUDIT_LOG_ENTRY_CREATE", "AUTO_MODERATION_RULE_DELETE", "READY", "AUTO_MODERATION_RULE_UPDATE", "THREAD_CREATE", "DIRECT_MESSAGE_POLL_VOTE_ADD", "RESUMED", "INTEGRATION_DELETE", "GUILD_UPDATE", "THREAD_DELETE", "GUILD_SOUNDBOARD_SOUNDS_UPDATE", "INVITE_CREATE", "MESSAGE_POLL_VOTE_ADD", "DIRECT_MESSAGE_REACTION_REMOVE", "CHANNEL_PINS_UPDATE", "MESSAGE_REACTION_REMOVE_EMOJI", "GUILD_MEMBER_UPDATE", "GUILD_MEMBER_ADD", "CHANNEL_CREATE", "VOICE_CHANNEL_EFFECT_SEND", "MESSAGE_REACTION_ADD", "GUILD_SCHEDULED_EVENT_USER_REMOVE", "GUILD_EMOJIS_UPDATE", "INTERACTION_CREATE", "DIRECT_MESSAGE_POLL_VOTE_REMOVE", "CHANNEL_UPDATE", "GUILD_BAN_REMOVE", "DIRECT_MESSAGE_DELETE", "VOICE_SERVER_UPDATE", "DIRECT_TYPING_START", "AUTO_MODERATION_RULE_CREATE", "GUILD_STICKERS_UPDATE", "MESSAGE_CREATE", "STAGE_INSTANCE_UPDATE", "THREAD_LIST_SYNC", "GUILD_SCHEDULED_EVENT_USER_ADD", "TYPING_START", "GUILD_SOUNDBOARD_SOUND_UPDATE", "INTEGRATION_CREATE", "THREAD_MEMBERS_UPDATE", "DIRECT_MESSAGE_REACTION_ADD", "AUTO_MODERATION_ACTION_EXECUTION", "STAGE_INSTANCE_DELETE"]

    def on(self, eventname: _eventliteral = None, function: Callable = None, *, once: bool = False) -> None:
        """
        Add a function to call when a specific event is dispatched.
        """
        def decorator(fn):
            if self.status != 0: self._error.summon('bot_is_running')

            if eventname is None: event_name = fn.__name__.upper()
            else: event_name = eventname.upper()
            if event_name in self._data.intents.intents:
                if self._check_handler(fn,event_name): # no_traceback
                    is_direct = event_name in self._data.intents.direct_intents
                    event_name = event_name[7:] if is_direct else event_name

                    self._handlers.append((event_name,{
                        "function": fn,
                        "is_direct": is_direct,
                        "once": once,
                    }))
            else:
                self._error.summon("event_invalid",event=event_name.upper())
        if function is not None: return decorator(function)
        else: return decorator

    def once(self, eventname: _eventliteral = None, function: Callable = None, *, once: bool = True) -> None:
        """
        Add a function to call when a specific event is dispatched once.
        """
        def decorator(fn):
            self.on(eventname=eventname,function=fn,once=once)
        if function is not None: return decorator(function)
        else: return decorator
        
def Embed(**kwargs):
    content = {}
    content.update(kwargs)
    content['type'] = 'rich'
    return content

def TokenReader(filename: str) -> str:
    """
    Read the first line of any file and return it, making it useful for securing token.
    """
    try:
        with open(filename, 'r') as file:
            tokenline = file.readline()
            return tokenline
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except Exception as e:
        raise ReferenceError(f"File '{filename}' cannot be read by TokenReader() with error {e}.")

# Types
from dispy.types.message import Message
from dispy.types.user import User
typesFunc = ['Message','User']

# END
__all__ = ['Bot','Embed','TokenReader'] + typesFunc