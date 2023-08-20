from typing import Union, Optional, Literal

from pydantic import Field

from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.jinja.exceptions import FailedToRenderTemplateException
from api_compose.core.logging import get_logger
from api_compose.core.serde.integer import IntegerSerde
from api_compose.core.serde.json import JsonSerde
from api_compose.core.serde.str import StringSerde
from api_compose.core.serde.xml import XmlSerde
from api_compose.core.serde.yaml import YamlSerde
from api_compose.services.common.events.templated_field import TemplatedFieldEvent
from api_compose.services.common.field.text_field import TextFieldFormat, BaseTextField, StringTextField, \
    IntegerTextField, YamlTextField, JsonTextField, XmlTextField

logger = get_logger(__name__)


class BaseTemplatedTextField(BaseTextField):
    template: str = ""

    # Setters
    def render_to_text(self, jinja_engine: JinjaEngine, jinja_context: BaseJinjaContext):
        # Step 1: render string

        rendered, is_success, exec = jinja_engine.set_template_by_string(self.template).render_to_str(
            jinja_context)

        if not is_success:
            # raise instead?
            logger.error(f"{self.template=}", TemplatedFieldEvent())
            logger.error(f"{is_success=}", TemplatedFieldEvent())
            logger.error(f"Exception Message={str(exec)}", TemplatedFieldEvent())

            logger.error(f"Available Globals {jinja_engine._custom_global_keys=}", TemplatedFieldEvent())
            raise FailedToRenderTemplateException(
                template=self.template,
                exec=exec,
                custom_global_keys=jinja_engine._custom_global_keys)

        self.text = rendered
        return self


class StringTemplatedTextField(StringTextField, BaseTemplatedTextField):
    pass


class IntegerTemplatedTextField(IntegerTextField, BaseTemplatedTextField):
    pass


class YamlTemplatedTextField(YamlTextField, BaseTemplatedTextField):
    pass


class JsonTemplatedTextField(JsonTextField, BaseTemplatedTextField):
    pass


class XmlTemplatedTextField(XmlTextField, BaseTemplatedTextField):
    pass

JsonLikeTemplatedTextField = Union[JsonTemplatedTextField, YamlTemplatedTextField]
