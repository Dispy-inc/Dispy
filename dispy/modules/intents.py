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

#"-1": [
#   "READY",
#   "RESUMED",
#   "VOICE_SERVER_UPDATE",
#   "USER_UPDATE",
#   "INTERACTION_CREATE",
#   "ALL"
#],

class intents_variable:
    def __init__(self,intents) -> None:
        intents_list = intents.copy()
        del intents_list['-1']
        self.__intents_list__ = intents_list

        self.intents = {key for nested_dict in intents.values() for key in nested_dict}
        self.direct_intents = intents["12"] + intents["13"] + intents["14"] + intents["25"]
        self.direct_intents_opposed = [intents["0"][9]] + intents["9"][:3] + intents["10"] + intents["11"] + intents["24"]
    def get_intents(self,eventname) -> list:
        parents = []
        for parent_id, events in self.__intents_list__.items():
            if eventname in events:
                parents.append(parent_id)
        return parents
    def get_child(self,id):
        return list(self.__intents_list__.values())[id]