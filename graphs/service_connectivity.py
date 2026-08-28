from langgraph.graph import START, END, StateGraph
from .nodes.service_nodes import (
    get_service_node,
    get_endpoints_node,
    list_matching_pods_node,
    diagnose_service_node
)
from state.service_connectivity_state import ServiceConnectivityState

def build_service_connectivity_graph():
    """
    Build the service connectivity workflow.
    """

    graph = StateGraph(ServiceConnectivityState)

    graph.add_node(
        "get_service",
        get_service_node,
    )
    graph.add_node(
        "get_endpoints",
        get_endpoints_node,
    )
    graph.add_node(
        "list_matching_pods",
        list_matching_pods_node,
    )
    graph.add_node(
        "diagnose_service_node",
        diagnose_service_node,
    )

    graph.add_edge(
        START,
        "get_service",
    )

    graph.add_edge(
        "get_service",
        "get_endpoints",
    )

    graph.add_edge(
        "get_endpoints",
        "list_matching_pods",
    )

    graph.add_edge(
        "list_matching_pods",
        "diagnose_service_node",
    )

    graph.add_edge(
        "diagnose_service_node",
        END,
    )

    return graph.compile()