from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph

from graphs.nodes.remediation_nodes import (
    create_remediation_plan_node,
    validate_remediation_plan_node,
    approval_gate_node,
    execute_action_node,
    verify_result_node
)
from state.remediation_state import RemediationState


def route_after_validation(
    state: RemediationState,
) -> str:
    """
    Route based on whether the remediation plan is valid.
    """

    if state["plan_valid"]:
        return "approval_pending"

    return "invalid_plan"


def route_after_approval(
    state: RemediationState,
) -> str:
    """
    Route based on the user's approval decision.
    """

    if state["approved"]:
        return "execute"

    return "rejected"


def build_remediation_graph():
    """
    Build the Kubernetes remediation workflow.
    """

    graph = StateGraph(RemediationState)

    graph.add_node(
        "create_remediation_plan",
        create_remediation_plan_node,
    )

    graph.add_node(
        "validate_remediation_plan",
        validate_remediation_plan_node,
    )

    graph.add_node(
        "approval_gate",
        approval_gate_node,
    )

    graph.add_node(
        "execute_action",
        execute_action_node
    )

    graph.add_node(
        "verify_result",
        verify_result_node
    )

    graph.add_edge(
        START,
        "create_remediation_plan",
    )

    graph.add_edge(
        "create_remediation_plan",
        "validate_remediation_plan",
    )

    graph.add_conditional_edges(
        "validate_remediation_plan",
        route_after_validation,
        {
            "invalid_plan": END,
            "approval_pending": "approval_gate",
        },
    )

    graph.add_conditional_edges(
        "approval_gate",
        route_after_approval,
        {
            "execute": "execute_action",
            "rejected": END,
        },
    )

    graph.add_edge(
        "execute_action",
        "verify_result",
    )

    graph.add_edge(
        "verify_result",
        END,
    )

    checkpointer = InMemorySaver()

    return graph.compile(
        checkpointer=checkpointer,
    )