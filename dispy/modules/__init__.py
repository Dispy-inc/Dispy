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

class dict_to_obj(dict):
    def __getattr__(self, attr):
        value = self.get(attr)
        if isinstance(value, dict):
            return dict_to_obj(value)
        return value
    
def format_list(elements):
    if not elements:
        return ""
    elif len(elements) == 1:
        return elements[0]
    elif len(elements) == 2:
        return " and ".join(elements)
    else:
        return ", ".join(elements[:-1]) + " and " + elements[-1]