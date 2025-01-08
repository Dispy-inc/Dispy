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
from typing import List, Dict, Any, TypedDict, Literal
import re

class EmbedField(DictWrapper):
    name: str
    value: str
    inline: bool

class EmbedAuthor(DictWrapper):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

class EmbedProvider(DictWrapper):
    name: str
    url: str

class EmbedFooter(DictWrapper):
    text: str
    icon_url: str
    proxy_icon_url: str

class Embed(DictWrapper):
    title: str
    type: str
    description: str
    url: str
    timestamp: Timestamp
    color: int
    footer: EmbedFooter
    image: Any
    thumbnail: Any
    video: Any
    provider: EmbedProvider
    author: EmbedAuthor
    fields: List[EmbedField]

class EmbedBuilder:
    """
    You can build an embed like in discord.js, template to get started:
    ```py
    embed = (EmbedBuilder()
        .setTitle('Title')
        .setDescription('Very interesting title')
        .setColor('red')
    )
    
    msg.send(embeds=embed)
    ```
    """
    def __init__(self):
        self.args = {}
        self.fields = []
    def get(self):
        content = {}
        content.update(self.args)
        if len(self.fields) > 0:
            content.update({'fields': self.fields})
        content['type'] = 'rich'
        return content
    
    def setTitle(self, title: str):
        self.args['title'] = title
        return self    
    def setDescription(self, description: str):
        self.args['description'] = description
        return self    
    
    class authorObject(TypedDict):
        name: str
        icon_url: str
        proxy_icon_url: str
        url: str
    def setAuthor(self, author: dict | authorObject):
        self.args['author'] = author
        return self
    
    def setUrl(self, url: str):
        self.args['url'] = url
        return self
    def setTimestamp(self, timestamp: Timestamp):
        """
        Take ISO8601, may support more in the future.
        """
        self.args['timestamp'] = timestamp
        return self
    
    _colors = Literal['blue','violet','pink','red','orange','yellow','green','black','brown','gray','white']
    global _color_palette
    _color_palette = {
        'blue': 0x3983F2,
        'violet': 0x9239F2,
        'pink': 0xF239D0,
        'red': 0xF23939,
        'orange': 0xF29C39,
        'yellow': 0xF2F239,
        'green': 0x39F23F,
        'black': 0x000000,
        'brown': 0xA05601,
        'gray': 0xA9A9A9,
        'white': 0xFFFFFF,
        'embed-discord': 0x2B2D31
    }
    def setColor(self, color: str | int | _colors):
        """
        Support hexcode, integer color and custom color (Red, blue, etc...)
        """
        color = color.lower()
        if isinstance(color, str) and color in list(_color_palette.keys()):
            self.args['color'] = _color_palette[color]
        elif isinstance(color, str):
            pattern = re.compile(r'^#?([0-9A-Fa-f]{6})$')
            match = pattern.match(color)
            if not match:
                raise ValueError("Invalid hex color code. Please provide a valid hex code in the format '#RRGGBB' or 'RRGGBB'.")
            self.args['color'] = int(match.group(1), 16)
            
        elif isinstance(color, int):
            if not (0x000000 <= color <= 0xFFFFFF):
                raise TypeError(f'{color} isn\'t valid. Try hexcode.')
            self.args['color'] = color
        else:
            raise TypeError('Type not compatible.')
        return self

    class FooterObject(TypedDict):
        text: str
        icon_url: str
        proxy_icon_url: str
    def setFooter(self, footer: dict | FooterObject):
        self.args['footer'] = footer
        return self
    
    class ImageObject(TypedDict):
        url: str
        proxy_url: str
        height: int
        width: int
    def setImage(self, image: dict | ImageObject):
        self.args['image'] = image
        return self
    
    class ThumbnailObject(TypedDict):
        url: str
        proxy_url: str
        height: int
        width: int
    def setThumbnail(self, thumbnail: dict | ThumbnailObject):
        self.args['thumbnail'] = thumbnail
        return self
    
    class VideoObject(TypedDict):
        url: str
        proxy_url: str
        height: int
        width: int
    def setVideo(self, video: dict | VideoObject):
        self.args['video'] = video
        return self

    class ProviderObject(TypedDict):
        name: str
        url: str
    def setProvider(self, provider: dict | ProviderObject):
        self.args['provider'] = provider
        return self
    
    # Fields
    class Field(TypedDict):
        name: str
        value: str
        inline: bool

    def setFields(self, *fields: List[Field] | Field):
        """
        Set one or multiple fields.
        ⚠️ Will remove fields defined before.
        """
        fields = [item for arg in fields for item in (arg if isinstance(arg, list) else [arg])]
        self.fields = fields
        return self
    
    def setField(self, name: str, value: str, inline: bool = None):
        """
        Set one field.
        ⚠️ Will remove fields defined before.
        """
        field = {'name': name, 'value': value}
        if inline is not None:
            field['inline'] = inline
        self.fields = [field]
        return self
    
    def addField(self, name: str, value: str, inline: bool = None):
        """
        Add a field.
        """
        field = {'name': name, 'value': value}
        if inline is not None:
            field['inline'] = inline
        self.fields.append(field)
        return self
    
    def addFields(self, *fields: List[Field] | Field):
        """
        Add one or multiple fields.
        """
        fields = [item for arg in fields for item in (arg if isinstance(arg, list) else [arg])]
        self.fields.extend(fields)
        return self