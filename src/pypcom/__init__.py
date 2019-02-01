from __future__ import absolute_import

from pypcom.__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __copyright__,
    __author_email__,
    __license__,
)

from pypcom.page import Page
from pypcom.component import PageComponent
PC = PageComponent
from pypcom.state import State


__all__ = [
    "Page",
    "PageComponent",
    "PC",
    "State",
]
