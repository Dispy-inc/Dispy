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

errors = {
    "traceback": "Traceback (most recent call last):",
    "no_traceback": "No traceback available.",
    "file": "File \"{filename}\", line {line}, in {name}",
    "event_invalid": "The event {event} doesn't exist",
    "noargs": "Event {eventname} connected to {function_name}() doesn't give any arguments. Remove them!",
    "invalidtype_args": "Argument '{name}' of {function_name}() need to be of type {needed_type}. The correct way:\ndef {function_name}({arguments}): ...",
    "extra_args": "{function_name}() has '{name}' which is invalid. The correct way:\ndef {function_name}({arguments}): ...",
    "missing_args": "{function_name}() missing argument '{name}'. The correct way:\ndef {function_name}({arguments}): ...",
    "bot_is_already_running": "The bot is already running",
    "bot_is_running": "The bot is currently active and you cannot change anything",
    "request_failed": "The HTTP request code is {code} with error \"{error}\"",
    "dispy_request_error": "An error occured with dispy during HTTP request: {error}",
    "getting_invalid": "You've tried to get() an invalid result, error of the result: {error}",
    "invalid_arguments": "You didn't give the argument {arg}!",
    "invalid_emoji": "The emoji '{emoji_name}' is invalid"
}