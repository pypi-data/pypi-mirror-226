from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.graph import (
    MatrixGraph,
    StatisticalGraph,
    BarabasiGraph,
    InhomogenousRandomGraph,
)

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_GRAPH(state: State, category: str) -> None:
    state.require(
        not state.in_graph,
        "Already inside a graph.",
        "First end current graph using EGRAPH.",
    )
    state.require(
        not state.in_agent,
        "Cannot define graphs inside agents.",
        "First end current message using EAGENT.",
    )
    state.require(
        not state.in_message,
        "Cannot define graphs inside messages.",
        "First end current message using EMESSAGE.",
    )
    state.require(
        not state.graph_exists(), "Graph already exists in the current environment."
    )

    match category:
        case "statistical":
            state.add_graph(StatisticalGraph())
        case "matrix":
            state.add_graph(MatrixGraph())
        case "barabasi-albert":
            state.add_graph(BarabasiGraph())
        case "irg":
            state.add_graph(InhomogenousRandomGraph())
        case _:
            state.panic(f"Incorrect operation: GRAPH {category}")

    state.in_graph = True


def op_EGRAPH(state: State) -> None:
    state.require(
        state.in_graph, "Not inside any graph.", "Try defining new graphs using GRAPH."
    )
    if (
        isinstance(state.last_graph, StatisticalGraph)
        or isinstance(state.last_graph, InhomogenousRandomGraph)
    ) and state.last_graph.is_agent_percent_amount_used():
        state.require(
            state.last_graph.is_size_defined(),
            "Graph size is not defined.",
            "Graph size must be defined to use agent percent amount.",
        )
    elif isinstance(state.last_graph, BarabasiGraph):
        state.require(
            state.last_graph.is_m_defined(),
            "Graph MParameters is not defined.",
            "Graph MParameters must be defined to use barabasi graph.",
        )
        if state.last_graph.is_agent_percent_amount_used():
            state.require(
                state.last_graph.is_size_defined(),
                "Graph size is not defined.",
                "Graph size must be defined to use agent percent amount.",
            )

    state.in_graph = False
