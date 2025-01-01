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
from typing import List, Dict, Any
import asyncio
from dispy.modules.rest_api import result

from dispy.types.emoji import Emoji
from dispy.types.guild import Member

class ReactionCountDetails(DictWrapper):
    burst: int
    normal: int

class Reaction(DictWrapper):
    count: int
    count_details: ReactionCountDetails
    me: bool
    me_burst: bool
    emoji: Emoji
    burst_colors: List[Any]

class ReactionAdd(DictWrapper):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Snowflake
    member: Member
    emoji: Emoji
    type: int
    message_author_id: Snowflake
    burst: bool
    burst_colors: List[Any]

    def remove(self) -> result[None]:
        """
        Remove the user reaction.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous():
            result = await self._api.__request__('delete', f'channels/{self.channel_id}/messages/{self.message_id}/reactions/{self.emoji.url_encode}/{self.user_id}', {}) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(), self._api._loop)
        return result[None](future,self._api,None)

class ReactionRemove(DictWrapper):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Snowflake
    emoji: Emoji
    type: int
    burst: bool

class ReactionRemoveAll(DictWrapper):
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Snowflake

class ReactionRemoveEmoji(DictWrapper):
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Snowflake
    emoji: Emoji