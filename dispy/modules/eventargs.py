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

# This file is used to attribute arguments to a eventname
# For example, when a message is send, we give the message and the author object separatly.

from dispy.types.message import Message
from dispy.types.interaction import Interaction
from dispy.types.user import User
from dispy.types.reaction import ReactionAdd, ReactionRemove, ReactionRemoveAll, ReactionRemoveEmoji
from dispy.types.variable import Null
from typing import Any, get_type_hints

from dispy.modules import dict_to_obj
class _eventargs:
    """
    🚫 Don't use it if you don't know what you're doing.
    """
    def __init__(self,intents,error):
        self.intents = intents
        self.error = error
        
    def set(self,eventname,api, **kwargs):
        if eventname == 'READY':
            return {}
        
        # Messages
        elif eventname in ['MESSAGE_CREATE','MESSAGE_UPDATE','DIRECT_MESSAGE_CREATE','DIRECT_MESSAGE_UPDATE']:
            msg = Message(**kwargs, _api=api)
            user = msg.author
            return {'msg': msg,'user': user}
        
        # Reactions
        elif eventname in ['MESSAGE_REACTION_ADD','DIRECT_MESSAGE_REACTION_ADD']:
            return {'reaction': ReactionAdd(**kwargs, _api=api)}
        elif eventname in ['MESSAGE_REACTION_REMOVE','DIRECT_MESSAGE_REACTION_REMOVE']:
            return {'reaction': ReactionRemove(**kwargs, _api=api)}
        elif eventname in ['MESSAGE_REACTION_REMOVE_ALL','DIRECT_MESSAGE_REACTION_REMOVE_ALL']:
            return {'reaction': ReactionRemoveAll(**kwargs, _api=api)}
        elif eventname in ['MESSAGE_REACTION_REMOVE_EMOJI','DIRECT_MESSAGE_REACTION_REMOVE_EMOJI']:
            return {'reaction': ReactionRemoveEmoji(**kwargs, _api=api)}
        
        # Interactions
        elif eventname == 'INTERACTION_CREATE':
            return {'int': Interaction(**kwargs, _api=api)}
        else:
            return {'args': dict_to_obj(kwargs)}
        
    def get(self,eventname):
        if eventname == 'READY':
            return {}
        
        # Messages
        elif eventname in ['MESSAGE_CREATE','MESSAGE_UPDATE','DIRECT_MESSAGE_CREATE','DIRECT_MESSAGE_UPDATE']:
            return {'msg': Message, 'user': User}
        
        # Reactions
        elif eventname in ['MESSAGE_REACTION_ADD','DIRECT_MESSAGE_REACTION_ADD']:
            return {'reaction': ReactionAdd}
        elif eventname in ['MESSAGE_REACTION_REMOVE','DIRECT_MESSAGE_REACTION_REMOVE']:
            return {'reaction': ReactionRemove}
        elif eventname in ['MESSAGE_REACTION_REMOVE_ALL','DIRECT_MESSAGE_REACTION_REMOVE_ALL']:
            return {'reaction': ReactionRemoveAll}
        elif eventname in ['MESSAGE_REACTION_REMOVE_EMOJI','DIRECT_MESSAGE_REACTION_REMOVE_EMOJI']:
            return {'reaction': ReactionRemoveEmoji}
        
        # Interactions
        elif eventname == 'INTERACTION_CREATE':
            return {'int': Interaction}
        else:
            return {'args': Any}

    def check_function(self,function,eventname):
        code = function.__code__
        function_arguments = list(code.co_varnames[:code.co_argcount])
        type_hints = get_type_hints(function)
        current_types = {arg: type_hints.get(arg,Null) for arg in function_arguments}
        needed_type = self.get(eventname)
        stringcode = ", ".join([f"{key}: {value.__name__}" for key, value in needed_type.items()])

        if len(needed_type) == 0:
            if not len(current_types) == 0:
                self.error.summon('noargs',eventname=eventname,function_name=function.__name__)
        else:
            for name, ntypes in needed_type.items():
                # Check for missing arguments
                if name not in current_types:
                    self.error.summon('missing_args', function_name=function.__name__, name=name, arguments=stringcode)

                # Check for extra arguments (we don't want those shit)
                for key in current_types:
                    if key not in needed_type:
                        self.error.summon('extra_args', function_name=function.__name__, name=key, arguments=stringcode)

                # Check for types
                input_type = current_types[name]
                if ntypes is not Any and not issubclass(input_type,ntypes):
                    self.error.summon('invalidtype_args', name=name, needed_type=ntypes.__name__, function_name=function.__name__, arguments=stringcode)
        return True