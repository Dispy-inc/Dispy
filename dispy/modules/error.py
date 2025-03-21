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

import traceback
import sys
import re
import os
import asyncio
import threading
from dispy.data.errors import errors

asyncio_path = os.path.dirname(asyncio.__file__)
threading_path = os.path.dirname(threading.__file__)

# Custom error handling for dispy
def summon(error_name,stop=True,*,number=None,user_stack=None,**kwargs):
    """
    Custom error handling, do not use if you don't know what your doing.
    """
    # Print the traceback
    stack = traceback.extract_stack()[:-2]
    user_stack = [frame for frame in user_stack if not frame.filename.startswith(threading_path)]
    filtered_stack = [frame for frame in stack if not re.compile(r'#\s*no_traceback\s*$').search(frame.line.replace(' ',''))]
    filtered_stack = [frame for frame in filtered_stack if not frame.filename.startswith(asyncio_path)]
    filtered_stack = [frame for frame in filtered_stack if not frame.filename.startswith(threading_path)]

    if len(filtered_stack) > 0 or user_stack:
        print('\033[93m' + errors['traceback'] + '\033[0m')
        for frame in user_stack:
            print(f"  {errors['file'].format(filename=frame.filename, line=frame.lineno, name=frame.name)}")
            print(f"    {frame.line}")
        for frame in filtered_stack:
            print(f"  {errors['file'].format(filename=frame.filename,line=frame.lineno,name=frame.name)}")
            print(f"    {frame.line}")
    else:
        print('\033[93m' + errors['no_traceback'] + '\033[0m')

    error = errors[error_name][number] if number else errors[error_name]
    error = error.format(**kwargs)
    print(f'\033[31m{error}\033[0m')    

    # Exit the program
    if stop: sys.exit()
    else: return error
    
def get(error_name,**kwargs):
    return errors[error_name].format(**kwargs)