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

from dispy.modules.dictwrapper import DictWrapper
from dispy.types.t.variable import Snowflake, Timestamp
from dispy.modules.result import result
from typing import List, Dict, Any
import asyncio

from dispy.types.t.message import Message
from dispy.types.t.guild import Member
from dispy.types.t.guild import Guild, Member
from dispy.types.t.channel import Channel
from dispy.types.t.message import ResolvedData
from dispy.types.t.emoji import Emoji
from dispy.types.t.entitlement import Entitlement
from dispy.types.t.user import User

class CommandInteractionDataOptions(DictWrapper):
    name: str
    type: int
    value: str | int | float | bool
    options: List['CommandInteractionDataOptions']
    focused: bool

class SelectOption(DictWrapper):
    label: str
    value: str
    description: str
    emoji: Emoji
    default: bool

class InteractionData(DictWrapper): # Unfortunatly, interaction data can be different so i put every possibilities in there
    id: Snowflake
    custom_id: str
    name: str
    type: int
    resolved: ResolvedData
    component_type: int
    components: Any
    values: List[SelectOption]
    options: List[CommandInteractionDataOptions]
    guild_id: Snowflake
    target_id: Snowflake

class Interaction(DictWrapper):
    id: Snowflake
    application_id: Snowflake
    version: int
    type: int
    token: str
    message: Message
    member: Member
    locale: str
    guild_locale: str
    guild_id: Snowflake
    guild: Guild
    channel_id: Snowflake
    channel: Channel
    entitlements: list
    entitlement_sku_ids: list
    data: InteractionData
    member: Member
    user: User
    entitlements: List[Entitlement]
    authorizing_integration_owners: Dict[str,Any]
    context: int
    app_permissions: str
    _api = None

    def reply(self,content=None,**kwargs) -> Message:
        """
        Reply to the message.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous(content, **kwargs):
            payload = {}
            #    "message_reference": {
            #        "channel_id": self.channel_id,
            #        "message_id": self.id,
            #        "guild_id": self.guild_id,
            #        "type": 0
            #    },
            #    "type": 19
            #}
    
            # Embed
            embeds = kwargs.get('embeds',None)
            if embeds is not None:
                if not isinstance(embeds, list):
                    embeds = [embeds]
                kwargs['embeds'] = embeds
            
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": content})
            
            result = await self._api.__request__('post', f'webhooks/{self.application_id}/{self.token}', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(content, **kwargs), self._api._loop)
        return result(future,self._api,Message)