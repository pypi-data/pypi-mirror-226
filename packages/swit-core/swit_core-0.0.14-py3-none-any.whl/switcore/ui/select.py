from enum import Enum

from pydantic import BaseModel

from switcore.ui.element_components import Tag
from switcore.ui.image import Image
from switcore.ui.select_item import SelectItem


class Option(SelectItem):
    image: Image | None = None
    tag: Tag | None = None


class OptionGroup(BaseModel):
    label: str
    options: list[Option]


class SelectStyleTypes(str, Enum):
    filled = "filled"
    outlined = "outlined"
    ghost = "ghost"


class Style(BaseModel):
    variant: SelectStyleTypes = SelectStyleTypes.outlined


class Select(BaseModel):
    type: str = 'select'
    placeholder: str | None
    multiselect: bool = False
    trigger_on_input: bool = False
    value: list[str] | None
    options: list[Option] = []
    option_groups: list[OptionGroup] = []
    style: Style | None = None
    searchable: bool = True
    search_keyword: str | None = None
    search_keyword_placeholder: str | None = None
