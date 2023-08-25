from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.agent import DistExpFloatParam as AgentDistExpFloatParam
from aasm.intermediate.agent import DistNormalFloatParam as AgentDistNormalFloatParam
from aasm.intermediate.agent import DistUniformFloatParam as AgentDistUniformFloatParam
from aasm.intermediate.agent import EnumParam as AgentEnumParam
from aasm.intermediate.agent import InitFloatParam as AgentInitFloatParam
from aasm.intermediate.agent import ModuleVariableParam as AgentModuleVariableParam
from aasm.intermediate.message import ConnectionParam as MessageConnectionParam
from aasm.intermediate.message import FloatParam as MessageFloatParam
from aasm.intermediate.message import ModuleVariableParam as MessageModuleVariableParam
from aasm.utils.validation import (
    is_float,
    is_valid_enum_list,
    is_valid_name,
    print_invalid_names,
)

if TYPE_CHECKING:
    from parsing.state import State


def op_agent_PRM(state: State, name: str, category: str, args: List[str]) -> None:
    state.require(
        state.in_agent,
        "Cannot define agent parameters outside agent scope.",
        "Try defining new agents using AGENT.",
    )
    state.require(
        not state.in_behaviour,
        "Cannot define agent parameters inside a behaviour.",
        "Parameters must appear after AGENT.",
    )
    state.require(
        not state.last_agent.name_exists(name),
        f"{name} already exists inside current agent.",
    )
    state.require(
        is_valid_name(name),
        f"{name} is not a correct name.",
        f"Names can only contain alphanumeric characters, underscores and cannot be: {print_invalid_names()}.",
    )

    match category, args:
        case "float", ["init", value]:
            state.require(is_float(value), f"{value} is not a valid float.")

            state.last_agent.add_init_float(AgentInitFloatParam(name, value))

        case "float", ["dist", "normal", mean, std_dev]:
            state.require(is_float(mean), f"{mean} is not a valid float.")
            state.require(is_float(std_dev), f"{std_dev} is not a valid float.")
            state.require(
                float(std_dev) >= 0,
                f"{std_dev} is not a valid standard deviation parameter.",
                "Standard deviation must be non-negative.",
            )

            state.last_agent.add_dist_normal_float(
                AgentDistNormalFloatParam(name, mean, std_dev)
            )

        case "float", ["dist", "exp", lambda_]:
            state.require(is_float(lambda_), f"{lambda_} is not a valid float.")
            state.require(
                float(lambda_) > 0,
                f"{lambda_} is not a valid lambda parameter.",
                "Lambda must be positive.",
            )

            state.last_agent.add_dist_exp_float(AgentDistExpFloatParam(name, lambda_))

        case "float", ["dist", "uniform", a, b]:
            state.require(is_float(a), f"{a} is not a valid float.")
            state.require(is_float(b), f"{b} is not a valid float.")

            state.last_agent.add_dist_uniform_float(
                AgentDistUniformFloatParam(name, a, b)
            )

        case "list", ["conn"]:
            state.last_agent.add_connection_list(name)

        case "list", ["msg"]:
            state.last_agent.add_message_list(name)

        case "list", ["float"]:
            state.last_agent.add_float_list(name)

        case "enum", enums:
            state.require(
                is_valid_enum_list(enums),
                f"{enums} is not a valid enum list.",
                "The correct pattern is [name, percent, ...], where percent(s) sum up to 100 (+/- 1).",
            )

            state.last_agent.add_enum(AgentEnumParam(name, enums))

        case _:
            if category in state.get_module_types():
                init_func = state.get_init_function(category)
                if init_func is "":
                    state.panic(
                        f"Cannot find init function for module type {category}.",
                    )
                state.last_agent.add_module_variable(
                    AgentModuleVariableParam(name, category, init_func)
                )
            else:
                state.panic(
                    f"Incorrect operation: (agent) PRM {name} {category} {args}"
                )


def op_message_PRM(state: State, name: str, category: str) -> None:
    state.require(
        state.in_message,
        "Cannot define message parameters outside message scope.",
        "Try defining new messages using MESSAGE.",
    )
    state.require(
        not state.last_message.param_exists(name),
        f"Parameter {name} already exists inside current message.",
    )
    state.require(
        is_valid_name(name),
        f"{name} is not a correct name.",
        f"Names can only contain alphanumeric characters, underscores and cannot be: {print_invalid_names()}.",
    )

    match category:
        case "float":
            state.last_message.add_float(MessageFloatParam(name))

        case "conn":
            state.last_message.add_connection(MessageConnectionParam(name))

        case _:
            if category in state.get_module_types():
                init_func = state.get_init_function(category)
                if init_func is "":
                    state.panic(
                        f"Cannot find init function for module type {category}.",
                    )
                state.last_message.add_module_variable(
                    MessageModuleVariableParam(name, category, init_func)
                )
            else:
                state.panic(f"Incorrect operation: (message) PRM {name} {category}")
