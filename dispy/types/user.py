from dispy.types.variable import Snowflake
from pydantic import BaseModel, create_model, ConfigDict
from typing import Optional, Type, Any, Tuple
from copy import deepcopy
from pydantic.fields import FieldInfo

def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )

@partial_model
class Avatar_decoration(BaseModel):
    asset: str
    sku_id: Snowflake

@partial_model
class User(BaseModel):
    id: Snowflake
    username: str
    discriminator: str
    global_name: str
    avatar: str
    bot: bool
    system: bool # This is useless x)
    mfa_enabled: bool
    verified: bool
    email: str
    locale: str
    flags: int
    banner: str
    accent_color: int
    premium_type: int
    public_flags: int
    avatar_decoration_data: Avatar_decoration