from typing import Protocol

from .Chroma_6310 import Chroma_6310
from .Chroma_63206A import Chroma_63206A
from .Chroma_63210A import Chroma_63210A
from .Chroma_63600 import Chroma_63600
from .Kikusui_PLZ1004WH import Kikusui_PLZ1004WH


class ElectronicLoad(Protocol):
    """
    A protocol defining the minimum functionality of an electronic load. Can be
    used for type-hinting, intellisense, or other code-completion tools in more
    complicated automation applications.
    """

    def set_current(self, current: float) -> None:
        """sets output level of the electronic load"""

    def get_current(self) -> float:
        """returns the output level of the electronic load"""

    def set_state(self, state: bool) -> None:
        """sets the state of the electronic load's output"""

    def get_state(self) -> bool:
        """returns the state of the electronic load's output"""

    def on(self) -> None:
        """sets the state of the electronic load's output to active"""

    def off(self) -> None:
        """sets the state of the electronic load's output to inactive"""

    def toggle(self) -> None:
        """reverses the state of the electronic load's output"""


__all__ = [
    "Chroma_6310",
    "Chroma_63206A",
    "Chroma_63210A",
    "Chroma_63600",
    "ElectronicLoad",
    "Kikusui_PLZ1004WH",
]
