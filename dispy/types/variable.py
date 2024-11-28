from pydantic_core import core_schema

class Snowflake():
    def __init__(self, value: str):
        self._value = value
    
    def __str__(self):
        return str(self._value)
    
    def __repr__(self):
        return str(self._value)
    
    def __get_pydantic_core_schema__(self, source):
        return core_schema.no_info_plain_validator_function(
            lambda value: Snowflake(value)  # Inline logic here
        )

class Timestamp():
    def __init__(self, value: str):
        self._value = value

    def __str__(self):
        return str(self._value)
    
    def __repr__(self):
        return str(self._value)
    
    def __get_pydantic_core_schema__(self, source):
        return core_schema.no_info_plain_validator_function(
            lambda value: Timestamp(value)  # Inline logic here
        )