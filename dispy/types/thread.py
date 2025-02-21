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
from dispy.types.variable import Snowflake, Timestamp
from typing import List, Dict, Any

from dispy.types.guild import Member

class ThreadMember(DictWrapper):
    id: Snowflake
    user_id: Snowflake
    join_timestamp: Timestamp
    flags: int
    member: Member

class ThreadMetadata(DictWrapper):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: Timestamp
    locked: bool
    invitable: bool
    create_timestamp: Timestamp

class ForumTag(DictWrapper):
    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Snowflake
    emoji_name: str

class DefaultReaction(DictWrapper):
    emoji_id: Snowflake
    emoji_name: str