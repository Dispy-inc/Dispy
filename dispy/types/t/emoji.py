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
from urllib.parse import quote

from dispy.types.t.role import Role
from dispy.types.t.user import User

class Emoji(DictWrapper):
    id: Snowflake
    name: str
    roles: List[Role]
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool
    url_encode: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url_encode = quote(f'{self.name}:{self.id}') if self.id else quote(self.name)