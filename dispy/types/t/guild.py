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
import traceback

from dispy.types.t.role import Role
from dispy.types.t.emoji import Emoji
from dispy.types.t.stickers import Sticker
from dispy.types.t.user import User, AvatarDecorationData

class WelcomeScreenChannel(DictWrapper):
    channel_id: Snowflake
    description: str
    emoji_id: Snowflake
    emoji_name: str


class WelcomeScreen(DictWrapper):
    description: str
    welcome_channels: List[WelcomeScreenChannel]

class Member(DictWrapper):
    user: User
    nick: str
    avatar: str
    banner: str
    roles: List[Snowflake]
    joined_at: Timestamp
    premium_since: Timestamp
    deaf: bool
    mute: bool
    flags: int
    pending: bool
    permissions: str
    communication_disabled_until: Timestamp
    avatar_decoration_data: AvatarDecorationData
    unusual_dm_activity_until: Timestamp
    guild_id: Snowflake = None
    _api = None

    def kick(self, guild_id: Snowflake = None) -> None:
        """
        Kick the member.

        In some cases, you will need to pass the argument `guild_id`.
        """
        future = self._api._loop.create_future()
        user_stack = traceback.extract_stack()[:-1]
        
        async def _asynchronous(guild_id):
            if guild_id == None:
                guild_id = self.guild_id
            result = await self._api.request('delete', f'guilds/{guild_id}/members/{self.user.id}', {}, user_stack) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(guild_id), self._api._loop)
        return result(future,self._api,None)

class Guild(DictWrapper):
    id: Snowflake
    name: str
    icon: str
    icon_hash: str
    splash: str
    discovery_splash: str
    owner: bool
    owner_id: Snowflake
    permissions: str
    region: str
    afk_channel_id: Snowflake
    afk_timeout: int
    widget_enabled: bool
    widget_channel_id: Snowflake
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: List[Role]
    emojis: List[Emoji]
    features: List[str]
    mfa_level: int
    application_id: Snowflake
    system_channel_id: Snowflake
    system_channel_flags: int
    rules_channel_id: Snowflake
    max_presences: int
    max_members: int
    vanity_url_code: str
    description: str
    banner: str
    premium_tier: int
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: Snowflake
    max_video_channel_users: int
    max_stage_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: WelcomeScreen
    nsfw_level: int
    locale: str
    stickers: List[Sticker]
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: Snowflake