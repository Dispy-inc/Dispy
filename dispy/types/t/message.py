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
from dispy.modules.error import summon
from dispy.modules.result import result
import asyncio
import re
import traceback
from urllib.parse import quote
from typing import List, Dict, Any

from dispy.types.t.user import User
from dispy.types.t.role import Role, RoleSubscriptionData
from dispy.types.t.embed import Embed, EmbedBuilder
from dispy.types.t.channel import ChannelMention, Channel
from dispy.types.t.attachment import Attachment
from dispy.types.t.reaction import Reaction
from dispy.types.t.application import Application
from dispy.types.t.guild import Member
from dispy.types.t.component import Component
from dispy.types.t.stickers import StickerItem, Sticker
from dispy.types.t.poll import Poll

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.member and self.guild_id:
            self.member.guild_id = self.guild_id
        if self.author and self.guild_id:
            self.author.guild_id = self.guild_id
        if self.author.id and self.member:
            self.member.user = User(id = self.author.id)

    # Message
    def reply(self,content: str = None, embeds: Embed | List[Embed] | EmbedBuilder | List[EmbedBuilder] = None, **kwargs) -> "Message":
        """
        Reply to the message.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
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
            
            result = await self._api.request('post', f'channels/{self.channel_id}/messages', payload, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result(future,self._api,Message)
    
    def send(self,content=None, embeds:Embed | List[Embed] | EmbedBuilder | List[EmbedBuilder] = None, reply_to: 'Message' = None, **kwargs) -> "Message":
        """
        Send a message in the same channel as the message.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
        async def _asynchronous(embeds):
            payload = {}

            # Reply
            if reply_to:
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
            
            result = await self._api.request('post', f'channels/{self.channel_id}/messages', payload, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result(future,self._api,Message)
    
    def delete(self) -> None:
        """
        Delete the message.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
        async def _asynchronous(channel_id,message_id):
            result = await self._api.request('delete', f'channels/{channel_id}/messages/{message_id}', {}, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(self.channel_id, self.id), self._api._loop)
        return result(future,self._api,None)
    
    def edit(self,content=None, embeds: Embed | List[Embed] | EmbedBuilder | List[EmbedBuilder] = None, **kwargs) -> "Message":
        """
        Edit the message.
        You need to be the author of it to edit it.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
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
            
            result = await self._api.request('patch', f'channels/{self.channel_id}/messages/{self.id}', payload, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(embeds), self._api._loop)
        return result(future,self._api,Message)
    
    def react(self,emoji: str, id: int | str = None) -> None:
        """
        Add a reaction to the message.

        You can use unicode emoji like `❤️`, Use `Windows + .` on windows to open the emoji selection menu.

        For custom emoji, you need to put `name:id`, e.g. `blobreach:123456789012345678`. Or you can separate these two by attributing the argument id separatly.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
        async def _asynchronous(emoji):
            # For custom emojis
            if ':' in emoji or id:
                if id: emoji = f'{emoji}:{str(id)}'
                else:
                    pattern = r"([a-zA-Z]+):(\d+)" # No, i totally didn't use chatgpt
                    match = re.search(pattern, emoji)
                    if match: emoji = match.group(0)
                    else: summon('invalid_emoji',emoji_name=str(emoji),stop=False)
            else:
                emoji = emoji[0]
            
            result = await self._api.request('put', f'channels/{self.channel_id}/messages/{self.id}/reactions/{quote(emoji)}/@me', {}, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(emoji), self._api._loop)
        return result(future,self._api,None)