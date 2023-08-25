from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aasm.intermediate.argument import Argument


class Declaration:
    def __init__(self, name: Argument, value: Argument):
        self.name: str = name.expr
        self.value: Argument = value

    def print(self) -> None:
        print(f"Declaration: {self.name}")
        self.value.print()


class FloatDeclaration(Declaration):
    def __init__(self, name: Argument, value: Argument):
        super().__init__(name=name, value=value)

    def print(self) -> None:
        print(f"FloatDeclaration: {self.name}")
        super().print()


class ConnectionDeclaration(Declaration):
    def __init__(self, name: Argument, value: Argument):
        super().__init__(name=name, value=value)

    def print(self) -> None:
        print(f"ConnectionDeclaration: {self.name}")
        super().print()


class ModuleVariableDeclaration(Declaration):
    def __init__(
        self, name: Argument, value: Argument, subtype: str, init_function: str
    ):
        super().__init__(name=name, value=value)
        self.subtype: str = subtype
        self.init_function: str = init_function

    def print(self) -> None:
        print(f"ModuleVariableDeclaration: {self.name}: {self.subtype}")
        super().print()
