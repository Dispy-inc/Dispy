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

from dispy.types.permissions import Overwrite
from dispy.types.user import User
from dispy.types.thread import ThreadMetadata, ThreadMember, ForumTag, DefaultReaction

class IconEmoji(DictWrapper):
    name: str
    id: Snowflake

class ChannelMention(DictWrapper):
    id: Snowflake
    guild_id: Snowflake
    type: int
    name: str

class Channel(DictWrapper):
    id: Snowflake
    type: int
    guild_id: Snowflake
    position: int
    permission_overwrites: List[Overwrite]
    name: str
    topic: str
    nsfw: bool
    last_message_id: Snowflake
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: List[User]
    theme_color: str
    icon: str
    owner_id: Snowflake
    application_id: Snowflake
    icon_emoji: IconEmoji
    managed: bool
    parent_id: Snowflake
    last_pin_timestamp: Timestamp
    rtc_region: str
    video_quality_mode: int
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: ThreadMember
    default_auto_archive_duration: int
    permissions: str
    flags: int
    total_message_sent: int
    available_tags: List[ForumTag]
    applied_tags: List[Snowflake]
    default_reaction_emoji: DefaultReaction
    default_thread_rate_limit_per_user: int
    default_sort_order: int
    default_forum_layout: int