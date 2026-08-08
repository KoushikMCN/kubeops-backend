from langgraph.graph import START, END, StateGraph
from .nodes.rollout_nodes import (
    get_deployment_node, 
    get_rollout_status_node, 
    rollout_result_node
)
from state.rollout_state import RolloutState

def build_deployment_rollout_status_graph():
    """
    Build the deployment rollout status workflow.
    """

    graph = StateGraph(RolloutState)

    graph.add_node(
        "get_deployment",
        get_deployment_node,
    )
    graph.add_node(
        "get_rollout_status",
        get_rollout_status_node,
    )
    graph.add_node(
        "rollout_result",
        rollout_result_node,
    )

    graph.add_edge(
        START,
        "get_deployment",
    )

    graph.add_edge(
        "get_deployment",
        "get_rollout_status",
    )

    graph.add_edge(
        "get_rollout_status",
        "rollout_result",
    )

    graph.add_edge(
        "rollout_result",
        END,
    )

    return graph.compile()