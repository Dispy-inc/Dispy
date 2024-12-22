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

from dispy.types.emoji import Emoji

class PollMedia(DictWrapper):
    text: str
    emoji: Emoji

class PollAnswer(DictWrapper):
    answer_id: int
    poll_media: PollMedia

class PollAnswerCount(DictWrapper):
    id: int
    count: int
    me_voted: bool

class PollResults(DictWrapper):
    is_finalized: bool
    answer_counts: List[PollAnswerCount]

class Poll(DictWrapper):
    question: PollMedia
    answers: List[PollAnswer]
    expiry: Timestamp
    allow_multiselect: bool
    layout_type: int
    results: PollResults