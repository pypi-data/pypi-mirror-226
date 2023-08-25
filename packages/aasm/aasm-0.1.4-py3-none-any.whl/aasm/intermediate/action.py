from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.block import Block, Declarations

if TYPE_CHECKING:
    from aasm.intermediate.declaration import Declaration
    from aasm.intermediate.instruction import Instruction
    from aasm.intermediate.message import Message


class Action:
    def __init__(self, name: str):
        self.name: str = name
        self._block_stack: List[Block] = [Block(Declarations())]
        self._nested_blocks_count: int = 0

    @property
    def nested_blocks_count(self) -> int:
        return self._nested_blocks_count

    @property
    def main_block(self) -> Block:
        return self._block_stack[0]

    @property
    def current_block(self) -> Block:
        return self._block_stack[-1]

    def is_declaration_in_scope(self, name: str) -> bool:
        return name in self.current_block.declared_names_in_scope

    def is_declared_float(self, name: str) -> bool:
        return self.current_block.is_declared_float(name)

    def is_declared_connection(self, name: str) -> bool:
        return self.current_block.is_declared_connection(name)

    def is_declared_module_variable(self, name: str) -> bool:
        return self.current_block.is_declared_module_variable(name)

    def get_module_variable_type(self, name: str) -> str:
        return self.current_block.get_module_variable_type(name)

    def add_float_declaration(self, declaration: Declaration) -> None:
        self.current_block.add_float_declaration(declaration)

    def add_connection_declaration(self, declaration: Declaration) -> None:
        self.current_block.add_connection_declaration(declaration)

    def add_module_variable_declaration(self, declaration: Declaration) -> None:
        self.current_block.add_module_variable_declaration(declaration)

    def add_instruction(self, instruction: Instruction) -> None:
        self.current_block.add_statement(instruction)

    def start_block(self) -> None:
        new_block = Block(self.current_block.get_declarations)
        self.current_block.add_statement(new_block)
        self._block_stack.append(new_block)
        self._nested_blocks_count += 1

    def end_block(self) -> None:
        self._block_stack.pop()
        self._nested_blocks_count -= 1

    def print(self) -> None:
        print(f"Action {self.name}")
        self.main_block.print()


class ModifySelfAction(Action):
    def __init__(self, name: str):
        super().__init__(name)

    def print(self) -> None:
        print("ModifySelfAction")
        super().print()


class SendMessageAction(Action):
    def __init__(self, name: str, message: Message):
        super().__init__(name)
        self.send_message: Message = message

    def print(self) -> None:
        print("SendMessageAction")
        super().print()
        self.send_message.print()
