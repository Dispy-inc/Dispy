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
from datetime import datetime

class Snowflake(str):
    def __new__(cls, value):
        return str.__new__(cls, value)

class Timestamp(str):
    _dictwrapper_type = True
    def __new__(cls, value):
        if value: result = datetime.fromisoformat(str(value)).timestamp()
        else: result = None
        return super().__new__(cls, result)
    
class Invalid(str):
    def __new__(cls, value):
        return str.__new__(cls, value)
    
class Null(str):
    def __init__(self):
        pass