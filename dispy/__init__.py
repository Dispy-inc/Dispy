# Dispy - Python Discord API library for discord bots.
# Copyright (C) 2025  James French
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Dispy is a light-weight discord API library.
"""
# Internal
from dispy.modules.intents import *
from dispy.modules import *
from dispy.types.t.user import User
from dispy.types.t.variable import Snowflake
from dispy.modules.rest_api import __internal__ as restapi
from dispy.modules.error import summon
from dispy.types.t.command import SlashCommandBuilder
from dispy.modules.appdirs import user_data_dir
from dispy.types.t.embed import EmbedBuilder
from dispy.modules.eventargs import _eventargs
from dispy.data import data
# External
from typing import Callable, Literal
from concurrent.futures import ThreadPoolExecutor
import aiohttp # Need to be installed (with websocket_client)
import json
import traceback
import threading
import asyncio
import os

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

# I want to add: "See related page on the [wiki](https://jamesfrench.gitbook.io/dispy)."
class Bot(restapi): # <- this shit has taken me hours
    #--------------------------------------------------------------------------------------#
    #                                      Bot Setup                                       #
    #--------------------------------------------------------------------------------------# 
    def __init__(self, token=None):
        """
        Define your bot.
        """
        # Public
        self.user: User = None
        self.status = 0
        self.token = token
        self.data_folder = user_data_dir('Dispy','Jamesfrench', "1.0") # It is not the dispy version but data folder version, I can change it when modifying how data work.

        # Dispy
        self._is_in_class = self.__class__ is not Bot
        self._registered_commands = []
        self._handlers = []
        self._user_stack = traceback.extract_stack()[:-1]
        
        # Networking
        self._heartbeat_interval = None
        self._loop = asyncio.new_event_loop() # Not the same loop as the API, so it can handle more requests.
        self._session = None # Session for websocket
        self._ws = None
        self._executor = ThreadPoolExecutor()
        self._tasks = []
        threading.Thread(target=self._run_loop, daemon=True).start()
        future = asyncio.run_coroutine_threadsafe(self._generate_session(), self._loop)
        future.result()
        
        # Internal
        self._api = restapi(self.token)
        self._data = data()
        self._eventargs = _eventargs(self._data.intents)

        # Commands
        self.commands = self._commands(self._handlers,self._eventargs,self._registered_commands)
    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever() # no_traceback
        
    async def _generate_session(self):
        self._session = aiohttp.ClientSession()

    def __getattr__(self, name):
        return getattr(self._api, name)
    
    def _create_data_folder(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def config(self,token=None):
        if self.status != 0: return None
        if token != None: self.token = token

    #--------------------------------------------------------------------------------------#
    #                                    Internal Code                                     #
    #--------------------------------------------------------------------------------------#
    # MAIN: Run the bot and get events
    async def _main(self):
        """
        🚫 Don't use it if you don't know what you're doing.
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
                        self.user = User(**data['d']['user'])
                        if len(self._registered_commands) > 0:
                            asyncio.run_coroutine_threadsafe(self._api.request('put',f'applications/{data['d']['user']['id']}/commands',payload=self._registered_commands), self._loop)
                    asyncio.create_task(self._sendevent(data['t'],data['d']))

    # Used to call functions when a event is dispatched
    async def _sendevent(self, eventname, args):
        """
        🚫 Don't use it if you don't know what you're doing.
        """
        once_remove = []
        tasks = []
    
        for key, handler in self._handlers:
            if key == eventname:
                if eventname == 'INTERACTION_CREATE' and handler['type'] == 1:
                    pass
                if eventname in self._data.intents.direct_intents_opposed:
                    if handler['is_direct'] and 'guild_id' in args:
                        continue
                    if not handler['is_direct'] and 'guild_id' not in args:
                        continue
    
                arguments = self._eventargs.set(eventname, self._api, **args)
                task = asyncio.to_thread(handler['function'], **arguments)
                tasks.append(task)
    
                if handler.get('once', False):
                    once_remove.append((key, handler))
    
        if tasks:
            await asyncio.gather(*tasks)
        for key, handler in once_remove:
            self._handlers.remove((key, handler))

    # Make the bot online
    async def _identify(self):
        """
        🚫 Don't use it if you don't know what you're doing.
        """
        payload = {
            'op': 2,
            'd': {
                'token': self.token,
                'intents': self._intents(),
                'properties': {
                    'os': 'linux',
                    'browser': 'dispy-lib',
                    'device': 'dispy-lib'
                }
            }
        }
        self.token = None
        await self._ws.send_json(payload)

    # Send heartbeat to discord to keep the bot alive
    async def _heartbeat(self):
        """
        🚫 Don't use it if you don't know what you're doing.
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
        🚫 Don't use it if you don't know what you're doing.
        """
        events = set()
        ids = []
        for key, handler in self._handlers:
            event_name = f'DIRECT_{key}' if handler['is_direct'] else key
            events.add(event_name)  # Add event name to the set

        ids = list(set([id for event in events if (intent_found := self._data.intents.get_intents(event)) for id in intent_found]))
        return sum(1 << int(id) for id in ids)
        
    # Start the bot
    async def _start(self):
        try:
            async with self._session.ws_connect('wss://gateway.discord.gg/?v=10&encoding=json') as ws:
                self._ws = ws
                await self._main()
                if ws.closed:
                    if ws.close_code in [4004]:
                        summon('close_code', False, number=ws.close_code, user_stack=self._user_stack)
                    else: 
                        message = await ws.receive()
                        reason = message.data if message.data is not None else "No data provided"
                        summon('connection_closed', True, code=str(ws.close_code), reason=reason)
        finally:
            await self._session.close()

    #--------------------------------------------------------------------------------------#
    #                                     Bot Control                                      #
    #--------------------------------------------------------------------------------------#
    def run(self) -> None:
        """
        Start your bot.
        - Will make it appear online
        - Will make it capable of receiving events and sending requests
        """
        if self.status != 0: summon('bot_is_already_running') # Stupid i know
        self.status = 1
        
        self._user_stack = traceback.extract_stack()[:-1]  
        future = asyncio.run_coroutine_threadsafe(self._start(), self._loop)
        future.result()

    def stop(self) -> None: # Experimental, i really think there is still active threads after shutdown.
        """
        Shutdown the bot.
        """
        async def _stop():
            if self._ws:
                await self._ws.close(code=1000)
            if self._session:
                await self._session.close()
            self.status = 0

        asyncio.run_coroutine_threadsafe(_stop(),loop=self._loop)

    def request(self, function, path, payload=None):
        """
        Make custom API request.
        """
        async def asynchronous():
            return await self._api.request(function=function,path=path,payload=payload)
        
        future_result = asyncio.run_coroutine_threadsafe(asynchronous(), self._loop)
        return future_result.result(timeout=7)

    class _commands:
        def __init__(self, handler, eventargs, commands):
            self.handler = handler
            self.eventargs = eventargs
            self.commands = commands
            
        def link(self, command: SlashCommandBuilder, function: Callable = None, *, guild_id: Snowflake = False):
            def decorator(fn):
                if self.eventargs.check_function(fn,'INTERACTION_CREATE'): # no_traceback
                    self.commands.append(command.get())
                    self.handler.append(('INTERACTION_CREATE',{
                        "function": fn,
                        "type": 1,
                        "context": guild_id, # False for Global and Guild_id for guild only. Help differentiete the two.
                        "name": command.args['name'],
                        "is_direct": False,
                        "once": False,
                    }))
            if function is not None: return decorator(function)
            else: return decorator

    #--------------------------------------------------------------------------------------#
    #                                    Event Handler                                     #
    #--------------------------------------------------------------------------------------#

    Events = Literal["GUILD_BAN_ADD", "MESSAGE_UPDATE", "GUILD_CREATE", "DIRECT_MESSAGE_REACTION_REMOVE_ALL", "GUILD_ROLE_CREATE", "GUILD_SCHEDULED_EVENT_CREATE", "GUILD_DELETE", "GUILD_SCHEDULED_EVENT_UPDATE", "ALL", "MESSAGE_REACTION_REMOVE_ALL", "GUILD_MEMBER_REMOVE", "INVITE_DELETE", "STAGE_INSTANCE_CREATE", "DIRECT_CHANNEL_PINS_UPDATE", "CHANNEL_DELETE", "GUILD_ROLE_UPDATE", "DIRECT_MESSAGE_CREATE", "DIRECT_MESSAGE_REACTION_REMOVE_EMOJI", "MESSAGE_DELETE_BULK", "THREAD_UPDATE", "MESSAGE_POLL_VOTE_REMOVE", "GUILD_SOUNDBOARD_SOUND_DELETE", "VOICE_STATE_UPDATE", "GUILD_INTEGRATIONS_UPDATE", "USER_UPDATE", "GUILD_ROLE_DELETE", "MESSAGE_REACTION_REMOVE", "DIRECT_MESSAGE_UPDATE", "MESSAGE_DELETE", "GUILD_SCHEDULED_EVENT_DELETE", "THREAD_MEMBER_UPDATE", "PRESENCE_UPDATE", "INTEGRATION_UPDATE", "GUILD_SOUNDBOARD_SOUND_CREATE", "WEBHOOKS_UPDATE", "GUILD_AUDIT_LOG_ENTRY_CREATE", "AUTO_MODERATION_RULE_DELETE", "READY", "AUTO_MODERATION_RULE_UPDATE", "THREAD_CREATE", "DIRECT_MESSAGE_POLL_VOTE_ADD", "RESUMED", "INTEGRATION_DELETE", "GUILD_UPDATE", "THREAD_DELETE", "GUILD_SOUNDBOARD_SOUNDS_UPDATE", "INVITE_CREATE", "MESSAGE_POLL_VOTE_ADD", "DIRECT_MESSAGE_REACTION_REMOVE", "CHANNEL_PINS_UPDATE", "MESSAGE_REACTION_REMOVE_EMOJI", "GUILD_MEMBER_UPDATE", "GUILD_MEMBER_ADD", "CHANNEL_CREATE", "VOICE_CHANNEL_EFFECT_SEND", "MESSAGE_REACTION_ADD", "GUILD_SCHEDULED_EVENT_USER_REMOVE", "GUILD_EMOJIS_UPDATE", "INTERACTION_CREATE", "DIRECT_MESSAGE_POLL_VOTE_REMOVE", "CHANNEL_UPDATE", "GUILD_BAN_REMOVE", "DIRECT_MESSAGE_DELETE", "VOICE_SERVER_UPDATE", "DIRECT_TYPING_START", "AUTO_MODERATION_RULE_CREATE", "GUILD_STICKERS_UPDATE", "MESSAGE_CREATE", "STAGE_INSTANCE_UPDATE", "THREAD_LIST_SYNC", "GUILD_SCHEDULED_EVENT_USER_ADD", "TYPING_START", "GUILD_SOUNDBOARD_SOUND_UPDATE", "INTEGRATION_CREATE", "THREAD_MEMBERS_UPDATE", "DIRECT_MESSAGE_REACTION_ADD", "AUTO_MODERATION_ACTION_EXECUTION", "STAGE_INSTANCE_DELETE"]
    def on(self, eventname: Events = None, function: Callable = None, *, once: bool = False) -> None:
        """
        Add a function to call when a specific event is dispatched.
        """
        def decorator(fn):
            if self.status != 0: summon('bot_is_running')

            if eventname is None: event_name = fn.__name__.upper()
            else: event_name = eventname.upper()
            if event_name in self._data.intents.intents:
                if self._eventargs.check_function(fn,event_name,self._is_in_class): # no_traceback
                    is_direct = event_name in self._data.intents.direct_intents
                    event_name = event_name[7:] if is_direct else event_name

                    self._handlers.append((event_name,{
                        "function": fn,
                        "type": 0,
                        "is_direct": is_direct,
                        "once": once,
                    }))
            else:
                summon("event_invalid",event=event_name.upper())
        if function is not None: return decorator(function)
        else: return decorator

    def once(self, eventname: Events = None, function: Callable = None, *, once: bool = True) -> None:
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

__all__ = ['Bot']