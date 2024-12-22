# Dispy - Python Discord API library for discord bots.
# Copyright (C) 2024  James French
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
from dispy.types.variable import Snowflake, Timestamp
from dispy.modules.rest_api import result
import asyncio
from typing import List, Dict, Any

from dispy.types.user import User
from dispy.types.role import Role, RoleSubscriptionData
from dispy.types.embed import Embed, EmbedBuilder
from dispy.types.channel import ChannelMention, Channel
from dispy.types.attachment import Attachment
from dispy.types.reaction import Reaction
from dispy.types.application import Application
from dispy.types.guild import Member
from dispy.types.component import Component
from dispy.types.stickers import StickerItem, Sticker
from dispy.types.poll import Poll

class MessageActivity(DictWrapper):
    type: int
    party_id: str

class MessageReference(DictWrapper):
    type: int
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    fail_if_not_exists: bool

class MessageSnapshot(DictWrapper):
    message: 'Message'

class MessageInteractionMetadata(DictWrapper):
    id: Snowflake
    type: int
    name: str
    user: User
    authorizing_integration_owners: Dict[Any,Any]
    original_response_message_id: Snowflake
    target_user: User
    target_message_id: Snowflake
    command_type: int

class MessageInteraction(DictWrapper):
    id: Snowflake
    type: int
    name: str
    user: User
    member: Member

class ResolvedData(DictWrapper):
    users: List[User]
    members: List[Member]
    roles: List[Role]
    channels: List[Channel]
    messages: List["Message"]
    attachments: List[Attachment]

class MessageCall(DictWrapper):
    participants: List[Snowflake]
    ended_timestamp: Timestamp

class Message(DictWrapper):
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: Timestamp
    edited_timestamp: Timestamp
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Role]
    mention_channels: List[ChannelMention]
    attachments: List[Attachment]
    embeds: List[Embed]
    reactions: List[Reaction]
    nonce: bool | int
    pinned: bool
    webhook_id: Snowflake
    type: int
    activity: MessageActivity
    application: Application
    application_id: Snowflake
    channel_type: int
    member: Member
    guild_id: Snowflake
    flags: int
    message_reference: MessageReference
    message_snapshots: List[MessageSnapshot]
    referenced_message: 'Message'
    interaction_metadata: MessageInteractionMetadata
    interaction: MessageInteraction
    thread: Channel
    components: List[Component]
    sticker_items: List[StickerItem]
    stickers: List[Sticker] # Useless lol, this shit is deprecated
    position: int
    role_subscription_data: RoleSubscriptionData
    resolved: ResolvedData
    poll: Poll
    call: MessageCall
    _api = None

    # Message
    def reply(self,content=None, embeds=None, **kwargs) -> result["Message"]:
        """
        Reply to the message.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous(embeds):
            payload = {
                "message_reference": {
                    "channel_id": self.channel_id,
                    "message_id": self.id,
                    "guild_id": self.guild_id,
                    "type": 0
                },
                "type": 19
            }

            # Embed
            if isinstance(embeds, list):
                embeds = [embed.get() if isinstance(embed, EmbedBuilder) else embed for embed in embeds]
            else:
                if isinstance(embeds, EmbedBuilder):
                    embeds = embeds.get()
            if embeds is not None:
                if not isinstance(embeds, list):
                    embeds = [embeds]
                payload.update({"embeds": embeds})
            
            # Reste
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": content})
            
            result = await self._api.__request__('post', f'channels/{self.channel_id}/messages', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result[Message](future,self._api,Message)
    
    def send(self,content=None, embeds=None, reply_to: 'Message' = None, **kwargs) -> result["Message"]:
        """
        Send a message in the same channel as the message.
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
            if isinstance(embeds, list):
                embeds = [embed.get() if isinstance(embed, EmbedBuilder) else embed for embed in embeds]
            else:
                if isinstance(embeds, EmbedBuilder):
                    embeds = embeds.get()
            if embeds is not None:
                if not isinstance(embeds, list):
                    embeds = [embeds]
                payload.update({"embeds": embeds})
            
            # Reste
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": content})
            
            result = await self._api.__request__('post', f'channels/{self.channel_id}/messages', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result[Message](future,self._api,Message)
    
    def delete(self) -> result[None]:
        """
        Delete the message.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous(channel_id,message_id):
            result = await self._api.__request__('delete', f'channels/{channel_id}/messages/{message_id}') # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(self.channel_id, self.id), self._api._loop)
        return result[None](future,self._api,None)
    
    def edit(self,content=None, embeds=None, **kwargs):
        """
        Edit the message.
        You need to be the author of it to edit it.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous(embeds):
            payload = {}
        
            # Embed
            if isinstance(embeds, list):
                embeds = [embed.get() if isinstance(embed, EmbedBuilder) else embed for embed in embeds]
            else:
                if isinstance(embeds, EmbedBuilder):
                    embeds = embeds.get()
            if embeds is not None:
                if not isinstance(embeds, list):
                    embeds = [embeds]
                payload.update({"embeds": embeds})
            
            # Reste
            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": content})
            
            result = await self._api.__request__('patch', f'channels/{self.channel_id}/messages/{self.id}', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result[Message](future,self._api,Message)