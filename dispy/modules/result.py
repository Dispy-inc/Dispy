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
from typing import Generic, TypeVar, Type, Optional

T = TypeVar('T')

class LazyResult:
    def __init__(self, future: asyncio.Future[T], api, cls: Type[T]):
        self._future = future
        self._api = api
        self._cls = cls
        self._cached_result = None

    def _load_result(self):
        if self._cached_result is not None:
            return

        if isinstance(self._future, Invalid):
            summon("getting_invalid", stop=False, error=self._future)
            return

        try:
            async def asynchronous() -> T:
                return await self._future

            future_result = asyncio.run_coroutine_threadsafe(asynchronous(), self._api._loop)
            self._cached_result = future_result.result(timeout=7)
        except Exception as e:
            summon("getting_invalid", stop=False, error=e)
            return

        if isinstance(self._cached_result, Invalid):
            summon("getting_invalid", stop=False, error=self._cached_result)
            self._cached_result = None

        if self._cls and self._cached_result:
            self._cached_result = self._cls(**self._cached_result, _api=self._api) if hasattr(self._cls, '_api') else self._cls(**self._cached_result)

    def __getattr__(self, item):
        self._load_result()
        if self._cached_result is None:
            raise AttributeError(f"Failed to retrieve result, attribute '{item}' is unavailable.")
        return getattr(self._cached_result, item)

def result(future: asyncio.Future[T], api, cls: Type[T]) -> LazyResult:
    return LazyResult(future, api, cls)
