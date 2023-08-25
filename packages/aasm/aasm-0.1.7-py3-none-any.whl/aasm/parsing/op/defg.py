from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.graph import (
    AgentConstantAmount,
    AgentPercentAmount,
    ConnectionConstantAmount,
    ConnectionDistExpAmount,
    ConnectionDistNormalAmount,
    ConnectionDistUniformAmount,
    StatisticalAgent,
    StatisticalGraph,
    BarabasiAgent,
    BarabasiGraph,
)
from aasm.utils.validation import is_float, is_int

if TYPE_CHECKING:
    from parsing.state import State

    from aasm.intermediate.graph import AgentAmount, ConnectionAmount


def op_DEFG(state: State, agent_name: str, amount: str, args: List[str]) -> None:
    state.require(
        state.in_graph,
        "Cannot define agent graph amount outside graph scope.",
        "Try defining new graphs using GRAPH.",
    )
    is_statistical = isinstance(state.last_graph, StatisticalGraph)
    is_barabsi = isinstance(state.last_graph, BarabasiGraph)
    state.require(
        is_statistical ^ is_barabsi,
        "DEFG can be used with statistical and barabasi graphs.",
        "Define statistical graphs with GRAPH statistical|GRAPH barabasi-albert.",
    )
    state.require(state.agent_exists(agent_name), f"Agent {agent_name} is not defined.")

    agent_amount: AgentAmount | None = None
    if amount.endswith("%"):
        percent_value = amount[:-1]
        state.require(is_float(percent_value), f"{amount} is not a valid float.")
        state.require(
            float(percent_value) >= 0 and float(percent_value) <= 100,
            f"{amount} is not a valid agent amount.",
            "Amount must be non-negative.",
        )

        agent_amount = AgentPercentAmount(percent_value)

    else:
        state.require(is_int(amount), f"{amount} is not a valid integer.")
        state.require(
            int(amount) >= 0,
            f"{amount} is not a valid agent amount.",
            "Amount must be non-negative.",
        )

        agent_amount = AgentConstantAmount(amount)

    if is_statistical:
        connection_amount: ConnectionAmount | None = None
        match args:
            case [value]:
                state.require(is_int(value), f"{value} is not a valid integer.")
                state.require(
                    int(value) >= 0,
                    f"{value} is not a valid connection amount.",
                    "Amount must be non-negative.",
                )

                connection_amount = ConnectionConstantAmount(value)

            case ["dist_normal", mean, std_dev]:
                state.require(is_float(mean), f"{mean} is not a valid float.")
                state.require(is_float(std_dev), f"{std_dev} is not a valid float.")
                state.require(
                    float(std_dev) >= 0,
                    f"{std_dev} is not a valid standard deviation parameter.",
                    "Standard deviation must be non-negative.",
                )

                connection_amount = ConnectionDistNormalAmount(mean, std_dev)

            case ["dist_exp", lambda_]:
                state.require(is_float(lambda_), f"{lambda_} is not a valid float.")
                state.require(
                    float(lambda_) > 0,
                    f"{lambda_} is not a valid lambda parameter.",
                    "Lambda must be positive.",
                )

                connection_amount = ConnectionDistExpAmount(lambda_)

            case ["dist_uniform", a, b]:
                state.require(is_float(a), f"{a} is not a valid float.")
                state.require(is_float(b), f"{b} is not a valid float.")

                connection_amount = ConnectionDistUniformAmount(a, b)

            case _:
                state.panic(f"Incorrect operation: DEFG {agent_name} {amount} {args}")

        state.last_graph.add_agent(
            StatisticalAgent(agent_name, agent_amount, connection_amount)
        )
    else:
        state.last_graph.add_agent(BarabasiAgent(agent_name, agent_amount))
