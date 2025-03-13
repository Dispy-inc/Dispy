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
from typing import List, Dict, Any
from dispy.modules.result import result
import asyncio

class AvatarDecorationData(DictWrapper):
    asset: str
    sku_id: Snowflake
    expires_at: int

class User(DictWrapper):
    id: Snowflake
    username: str
    discriminator: str
    display_name: str
    global_name: str
    avatar: str
    clan: Any
    bot: bool
    system: bool # This is useless x)
    mfa_enabled: bool
    verified: bool
    email: str
    locale: str
    flags: int
    banner: str
    banner_color: int
    accent_color: int
    premium_type: int
    public_flags: int
    primary_guild: str
    avatar_decoration_data: AvatarDecorationData
    whole_name: str = None
    guild_id: Snowflake = None
    _api = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.username and self.discriminator:
            self.whole_name = f'{self.username}{f'#{self.discriminator}' if self.discriminator != '0' else ''}'

    def kick(self, guild_id: Snowflake = None) -> result[None]:
        """
        Kick the user.
    
        In some cases, you will need to pass the argument `guild_id`.
        """
        future = self._api._loop.create_future()
        
        async def _asynchronous(guild_id):
            if guild_id == None:
                if self.guild_id != None:
                    guild_id = self.guild_id
                else:
                    raise TypeError('You need to pass the guild_id argument to kick()')
            result = await self._api.__request__('delete', f'guilds/{guild_id}/members/{self.id}') # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(guild_id), self._api._loop)
        return result[None](future,self._api,None)
    
__all__ = ["User"]