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

class RoleSubscriptionData(DictWrapper):
    role_subscription_listing_id: Snowflake
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool

# This function is shit, see the discord wiki to see it: https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
# I will need to change bool to True if null is present, else to False, who is the dumbass at discord that coded that api shit.
# \/ \/ \/ \/

class RoleTags(DictWrapper):
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: Any # Will not work
    subscription_listing_id: Snowflake
    available_for_purchase: Any # Will not work
    guild_connections: Any # Will not work

class Role(DictWrapper):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: str
    unicode_emoji: str
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: RoleTags
    flags: int