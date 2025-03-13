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

from dispy.types.t.emoji import Emoji
from dispy.types.t.channel import Channel


class ComponentDefaultValue(DictWrapper):
    id: Snowflake
    type: str


class ComponentOption(DictWrapper):
    label: str
    value: str
    description: str
    emoji: Emoji
    default: bool


class ComponentObject(DictWrapper):
    type: int
    style: int
    label: str
    emoji: Emoji
    custom_id: str
    sku_id: Snowflake
    url: str
    value: str
    required: bool
    disabled: bool
    options: List[ComponentOption]
    channel_types: List[Channel]
    placeholder: str
    default_values: List[ComponentDefaultValue]
    min_values: int
    max_values: int


class Component(DictWrapper):
    type: int
    components: List[ComponentObject]