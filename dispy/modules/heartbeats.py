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
import threading

class Heartbeats():
    def __init__(self):
        self._ws = None
        self._interval = None
        self._running = True
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()
    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever() # no_traceback
        
    async def run(self, ws, interval):
        self._ws = ws
        self._interval = interval
        asyncio.run_coroutine_threadsafe(self._heartbeat(), self._loop)
        
    async def _heartbeat(self):
        while self._running:
            await asyncio.sleep(self._interval)
            if self._running:
                await self._ws.send_json({"op": 1, "d": 'null'})

    def stop(self):
        self._running = False
        self._loop.call_soon_threadsafe(self._loop.stop)