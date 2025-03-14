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

import aiohttp
import asyncio
import json
import threading
from dispy.modules import dict_to_obj
from dispy.types.t.embed import EmbedBuilder
from dispy.types.t.variable import Invalid
from dispy.modules.result import result
from dispy.modules.error import summon, get as geterror
from typing import List
from dispy.types.t.embed import Embed, EmbedBuilder

# 888888ba  oo                               
# 88    `8b ``                               
# 88     88 dP .d8888b.    88d888b. dP    dP 
# 88     88 88 Y8ooooo.    88'  `88 88    88 
# 88    .8P 88       88 ,, 88.  .88 88.  .88 
# 8888888P  dP `88888P' 88 88Y888P' `8888P88 
#                          88            .88 
#                          dP        d8888P  

# Developed by ✯James French✯ with ❤
# Licensed with GPLv3

from dispy.types.t.message import Message

class __internal__():
    def  __init__(self,token) -> None:
        self.token = token
        self.__header = {
            'authorization': f'Bot {self.token}',
            'content-type': 'application/json'
        }
        self._loop = asyncio.new_event_loop()
        self._base_url = 'https://discord.com/api/v10/'
        self._api = self
        threading.Thread(target=self._run_loop, daemon=True).start()
    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever() # no_traceback

    async def __request__(self,function,path,payload=None):
        args = {}
        if payload:
            args['json'] = payload
        async with aiohttp.ClientSession() as session:
            try:
                async with getattr(session, function)(f'{self._base_url}{path}', headers=self.__header, **args) as response:
                    if response.status not in [200, 204]:
                        error = json.loads(await response.text())
                        summon("request_failed",stop=False,code=response.status,error=error["message"])
                        return Invalid(geterror("request_failed",code=response.status,error=error["message"]))
                    else:
                        if response.status != 204:
                            response_data = await response.json()
                            if isinstance(response_data, dict):
                                return dict_to_obj(response_data)
                            elif isinstance(response_data, list):
                                return [dict_to_obj(item) for item in response_data]
                        else:
                            return None
            except Exception as err:
                summon("dispy_request_error",stop=False,error=err)

    #--------------------------------------------------------------------------------------#
    #                                       Requests                                       #
    #--------------------------------------------------------------------------------------#
    def send_message(self,content=None, channel_id=None, embeds = Embed | List[Embed] | EmbedBuilder | List[EmbedBuilder], reply_to: Message = None, **kwargs) -> result[Message]:
        
        """
        Send a message in a specific channel.
        """
        future = self._api._loop.create_future()

        async def _asynchronous(embeds):
            payload = {}
    
            # Reply
            if reply_to != None:
                payload.update({
                    "message_reference": {
                        "channel_id": reply_to.channel_id,
                        "message_id": reply_to.id,
                        "guild_id": reply_to.guild_id,
                        "type": 0
                    },
                    "type": 19
                })
    
            # Embed
            if embeds:
                result_embeds = []
                if not isinstance(embeds, list): embeds = [embeds] # Convert to list
                
                for embed in embeds:
                    embed = embed.get() if isinstance(embed, EmbedBuilder) else embed # no_traceback
                    if isinstance(embed, list):
                        result_embeds.extend(embed)
                    else:
                        result_embeds.append(embed)
                    payload.update({"embeds": result_embeds})
            
            # Others
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": str(content)})
            
            result = await self._api.__request__('post', f'channels/{channel_id}/messages', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result[Message](future,self._api,Message)

    def delete_message(self,channel_id,message_id) -> result[None]:
        """
        Delete a specific message.
        """
        future = self._api._loop.create_future()

        async def _asynchronous(channel_id,message_id):
            result = await self._api.__request__('delete', f'channels/{channel_id}/messages/{message_id}') # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(channel_id, message_id), self._api._loop)
        return result[None](future,self._api,None)
    
    def edit_message(self,content=None, channel_id=None, message_id=None, embeds = Embed | List[Embed] | EmbedBuilder | List[EmbedBuilder], **kwargs) -> result[Message]:
        
        """
        Edit a specific message in a specific channel.
        You need to be the author of the message to edit it.
        """
        future = self._api._loop.create_future()
    
        async def _asynchronous(embeds):
            payload = {}

            # Embed
            if embeds:
                result_embeds = []
                if not isinstance(embeds, list): embeds = [embeds] # Convert to list
                
                for embed in embeds:
                    embed = embed.get() if isinstance(embed, EmbedBuilder) else embed # no_traceback
                    if isinstance(embed, list):
                        result_embeds.extend(embed)
                    else:
                        result_embeds.append(embed)
                    payload.update({"embeds": result_embeds})
            
            # Others
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": str(content)})
            
            result = await self._api.__request__('patch', f'channels/{channel_id}/messages/{message_id}', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result[Message](future,self._api,Message)