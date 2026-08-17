from langgraph.graph import START, END, StateGraph

from state.cluster_health_state import ClusterHealthState

from .nodes.cluster_health_nodes import (
    get_deployments_node,
    get_pods_node,
    get_services_node,
    get_events_node,
    diagnose_cluster_node,
)


def build_cluster_health_graph():
    """
    Build the cluster health workflow.
    """

    graph = StateGraph(ClusterHealthState)

    graph.add_node(
        "get_deployments",
        get_deployments_node,
    )

    graph.add_node(
        "get_pods",
        get_pods_node,
    )

    graph.add_node(
        "get_services",
        get_services_node,
    )

    graph.add_node(
        "get_events",
        get_events_node,
    )

    graph.add_node(
        "diagnose_cluster",
        diagnose_cluster_node,
    )

    graph.add_edge(
        START,
        "get_deployments",
    )

    graph.add_edge(
        "get_deployments",
        "get_pods",
    )

    graph.add_edge(
        "get_pods",
        "get_services",
    )

    graph.add_edge(
        "get_services",
        "get_events",
    )

    graph.add_edge(
        "get_events",
        "diagnose_cluster",
    )

    graph.add_edge(
        "diagnose_cluster",
        END,
    )

    return graph.compile()