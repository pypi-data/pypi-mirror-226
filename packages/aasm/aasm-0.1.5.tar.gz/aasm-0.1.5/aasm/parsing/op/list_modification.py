from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import AddElement, RemoveElement

if TYPE_CHECKING:
    from aasm.parsing.state import State


def handle_list_modification(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(
        state.in_action,
        "Not inside any action.",
        "List modifications can be used inside actions.",
    )
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(
        lhs.list_modification_context(rhs),
        "Mismatched types in the list modification context.",
        f"ARG1 {lhs.explain()}, ARG2 {rhs.explain()}",
    )

    match op:
        case "ADDE":
            state.last_action.add_instruction(AddElement(lhs, rhs))

        case "REME":
            state.last_action.add_instruction(RemoveElement(lhs, rhs))

        case _:
            state.panic(f"Unexpected error: {op} {arg1} {arg2}")
