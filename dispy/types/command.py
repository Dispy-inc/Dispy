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
from typing import List, Dict, Any, Callable

class CommandOptionChoice(DictWrapper):
    name: str
    name_localizations: Dict[str, Any]
    value: str | int | float

class CommandOption(DictWrapper):
    type: int
    name: str
    name_localizations: Dict[str, Any]
    description_localizations: Dict[str, Any]
    description: str
    required: bool
    choices: List[CommandOptionChoice]
    options: List["CommandOption"]
    channel_types: List[int]
    min_value: int | float
    max_value: int | float
    min_length: int
    max_length: int
    autocomplete: bool

class Command(DictWrapper):
    id: Snowflake
    type: int
    application_id: Snowflake
    guild_id: Snowflake
    name: str
    name_localizations: Dict[str, Any]
    description_localizations: Dict[str, Any]
    description: str
    options: List[CommandOption]
    default_member_permissions: str
    dm_permission: bool
    default_permission: bool
    nsfw: bool
    integration_types: List[int]
    contexts: List[int]
    version: Snowflake
    handler: int

class SlashCommandBuilder:
    """
    You can build a command like an EmbedBuilder, template to get started:
    ```py
    command = (CommandBuilder()
        .setTitle('command')
        .setDescription('Very interesting description')
    )
    ```
    """
    def __init__(self):
        self.args = {}
    def get(self):
        content = {}
        content.update(self.args)
        content['type'] = 1
        return content
    
    def setName(self, name: str):
        self.args['name'] = name
        return self  
    def setDescription(self, description: str):
        self.args['description'] = description
        return self  