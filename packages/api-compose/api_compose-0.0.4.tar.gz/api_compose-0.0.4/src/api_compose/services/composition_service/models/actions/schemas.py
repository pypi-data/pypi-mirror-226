from api_compose.services.common.field.text_field import BaseTextField, JsonLikeTextField, XmlTextField
from api_compose.services.common.models.base import BaseModel


class BaseSchemaModel(BaseModel):
    schema_: BaseTextField


class JsonSchemaModel(BaseSchemaModel):
    schema_: JsonLikeTextField


class XmlSchemaModel(BaseSchemaModel):
    schema_: XmlTextField
