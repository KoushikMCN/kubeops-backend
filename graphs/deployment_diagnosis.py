from langgraph.graph import START, END, StateGraph

from graphs.nodes.deployment_nodes import (
    diagnosis_node,
    get_deployment_node,
    get_events_node,
    get_logs_node,
    list_pods_node,
)
from state.deployment_state import DeploymentDiagnosisState


def build_deployment_diagnosis_graph():
    """
    Build the deployment diagnosis workflow.
    """

    graph = StateGraph(DeploymentDiagnosisState)

    graph.add_node(
        "get_deployment",
        get_deployment_node,
    )
    graph.add_node(
        "list_pods",
        list_pods_node,
    )
    graph.add_node(
        "get_events",
        get_events_node,
    )
    graph.add_node(
        "get_logs",
        get_logs_node,
    )
    graph.add_node(
        "diagnosis",
        diagnosis_node,
    )

    graph.add_edge(
        START,
        "get_deployment",
    )

    graph.add_edge(
        "get_deployment",
        "list_pods",
    )

    graph.add_edge(
        "list_pods",
        "get_events",
    )

    graph.add_edge(
        "get_events",
        "get_logs",
    )

    graph.add_edge(
        "get_logs",
        "diagnosis",
    )

    graph.add_edge(
        "diagnosis",
        END,
    )

    return graph.compile()