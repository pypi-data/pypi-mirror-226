from enum import Enum
from typing import Any, Union, Optional, Literal

from pydantic import BaseModel as _BaseModel, Field
from pydantic import field_serializer

from api_compose.core.logging import get_logger
from api_compose.core.serde.base import BaseSerde
from api_compose.core.serde.integer import IntegerSerde
from api_compose.core.serde.json import JsonSerde
from api_compose.core.serde.str import StringSerde
from api_compose.core.serde.xml import XmlSerde
from api_compose.core.serde.yaml import YamlSerde
from api_compose.services.common.events.text_field import TextFieldEvent

logger = get_logger(__name__)


class TextFieldFormat(str, Enum):
    STRING = 'string'
    INTEGER = 'integer'
    YAML = 'yaml'
    JSON = 'json'
    XML = 'xml'


class BaseTextField(_BaseModel):
    format: TextFieldFormat
    serde: BaseSerde = Field(exclude=True)

    @field_serializer('serde')
    def serialize_serde(self, serde: BaseSerde, _info):
        return serde.__str__()

    # Other properties
    text: Optional[str] = Field(None)
    obj: Optional[Any] = Field(None)

    # Setters

    def deserialise_to_obj(self):
        try:
            self.obj = self.serde.deserialise(self.text)
        except Exception as e:
            logger.error(f"Error deserising text to {self.format=} \n"
                         f"{self.text=}", TextFieldEvent())
            raise
        return self


class StringTextField(BaseTextField):
    format: Literal[TextFieldFormat.STRING] = TextFieldFormat.STRING

    serde: StringSerde = Field(
        StringSerde(),
        exclude=True
    )


class IntegerTextField(BaseTextField):
    format: Literal[TextFieldFormat.INTEGER] = TextFieldFormat.INTEGER

    serde: IntegerSerde = Field(
        IntegerSerde(),
        exclude=True
    )


class YamlTextField(BaseTextField):
    format: Literal[TextFieldFormat.YAML] = TextFieldFormat.YAML

    serde: YamlSerde = Field(
        YamlSerde(),
        exclude=True
    )


class JsonTextField(BaseTextField):
    format: Literal[TextFieldFormat.JSON] = TextFieldFormat.JSON

    serde: JsonSerde = Field(
        JsonSerde(),
        exclude=True
    )


class XmlTextField(BaseTextField):
    format: Literal[TextFieldFormat.XML] = TextFieldFormat.XML
    serde: XmlSerde = Field(
        XmlSerde(),
        exclude=True,
    )


JsonLikeTextField = Union[JsonTextField, YamlTextField]
