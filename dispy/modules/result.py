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

import asyncio
from dispy.modules.error import summon
from dispy.types.t.variable import Invalid
from typing import Generic, TypeVar, Type

T = TypeVar('T')

class result(Generic[T]):
    """
    Represent the response of the request you've done.
    Use .get() to get variables, this will pause the execution of your code until the response is given.
    """
    def __init__(self, future: asyncio.Future[T], api, cls: Type[T] = None):
        self.future = future
        self.api = api
        self.loop = self.api._loop
        self._cls = cls
    
    def get(self) -> T:
        """
        Will block the code execution until response is given.
        """
        if not isinstance(self.future,Invalid):
            async def asynchronous() -> T:
                return await self.future
            
            future_result = asyncio.run_coroutine_threadsafe(asynchronous(), self.loop)
            result = future_result.result(timeout=7)
        else:
            summon("getting_invalid",stop=False,error=self.future)
            return None
        
        if isinstance(result,Invalid):
            summon("getting_invalid",stop=False,error=result)
            return None
        else:
            return self._cls(**result, _api=self.api) if hasattr(self._cls,'_api') else self._cls(**result)