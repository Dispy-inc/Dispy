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

from typing import get_type_hints, Any, Dict, List, Union, _GenericAlias
import inspect
import json


# This variable is only On for debugging purposes and to see if there is missing args, need to be Off for normal uses.
debug = True

class DictWrapper:
    """
    DictWrapper is a tool used by Dispy made to replace TypedDict, basemodel from pydantic and dataclass. It is made to have only the pros of theses three.

    ### Functionalities
    - Take Dict as input (Pydantic & dataclass)
    - Support self-referencing (TypedDict)
    - Get by obj (Pydantic & dataclass)
    """
    #This function is needed to .dumps a text inside DictWrapper, but i removed it because it is monkey patching
    #and this is a programming crime. If you know how or want to fix this problem, contribute to dispy!
    #
    #def _jsonSupport():
    #    original_default = json.JSONEncoder.default
    #    original_decoder = json.JSONDecoder().object_hook
    #    def default(self, obj):
    #        if isinstance(obj, DictWrapper):
    #            return {'type': 'DictWrapper', 'name': obj.to_dict()}
    #        return original_default(self, obj)
    #    def object_hook(obj):
    #        if 'type' in obj and obj['type'] == 'DictWrapper':
    #            return DictWrapper.from_dict(obj['name'])
    #        return obj if original_decoder is None else original_decoder(obj)
    #    json.JSONEncoder.default = default
    #    json._default_decoder = json.JSONDecoder(object_hook=object_hook)
    #_jsonSupport()

    _dictwrapper = True
    _api = None
    _types = None

    def __init__(self, **kwargs):
        """
        This class uses DictWrapper!
        """
        self._types = get_type_hints(self.__class__)

        for key, value in kwargs.items():
            if key not in self._types and key != '_api':
                if debug:
                    raise KeyError(f"'{key}' was given but isn't defined in the DictWrapper '{self.__class__.__name__}': '{value}' of type {str(type(value)).upper()}")
                else: continue

            if '_api' in kwargs:
                self._api = kwargs['_api']

            if isinstance(value, dict):
                if not isinstance(self._types[key], _GenericAlias) and issubclass(self._types[key], DictWrapper) and self._api is not None:
                    value = self._types[key](_api=self._api, **value)
                elif inspect.isclass(self._types[key]):
                    value = self._types[key](**value)
                else:
                    value = value
            if key != '_api' and hasattr(self._types[key],'_dictwrapper_type'):
                value = self._types[key](value)
            setattr(self, key, value)

    def __getattr__(self, name):
        if name in self._types:
            return None
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __getitem__(self, item):
        if hasattr(self, item):
            value = getattr(self, item)
            if isinstance(value, DictWrapper):
                return value.to_dict()
            return value
        raise KeyError(f"'{item}' not found in '{self.__class__.__name__}'")
    
    def to_dict(self):
        result = {}
        for key in self._types:
            value = getattr(self, key, None)
            if isinstance(value, DictWrapper):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    def __iter__(self):
        return iter(self.to_dict().items())
    
    def __repr__(self):
        return repr(self.to_dict())
    
    def __str__(self):
        return str(self.to_dict())