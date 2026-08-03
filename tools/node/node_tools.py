from langchain_core.tools import tool

from services.kubernetes.node_service import NodeService

node_service = NodeService()


@tool
def list_nodes():
    """
    List Kubernetes nodes.

    Returns:
    - A list of dictionaries containing node information.
    """
    node_list = node_service.list_nodes()

    return [
        {
            "name": node.metadata.name,
            "status": next(
                (
                    condition.type
                    for condition in (node.status.conditions or [])
                    if condition.status == "True"
                ),
                "Unknown",
            ),
            "unschedulable": node.spec.unschedulable
            if node.spec
            else None,
        }
        for node in (node_list.items or [])
    ]


@tool
def get_node(name: str):
    """
    Get information about a Kubernetes node.

    Parameters:
    - name: Name of the node.

    Returns:
    - Dictionary containing node information.
    """
    node = node_service.get_node(name)

    metadata = node.metadata
    spec = node.spec
    status = node.status

    return {
        "name": metadata.name if metadata else None,
        "labels": metadata.labels if metadata else None,
        "annotations": metadata.annotations if metadata else None,
        "unschedulable": spec.unschedulable if spec else None,
        "taints": [
            {
                "key": t.key,
                "value": t.value,
                "effect": t.effect,
            }
            for t in (spec.taints or [])
        ]
        if spec
        else [],
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message,
            }
            for c in (status.conditions or [])
        ]
        if status
        else [],
    }


@tool
def cordon_node(name: str):
    """
    Mark a Kubernetes node as unschedulable.

    Parameters:
    - name: Name of the node.

    Returns:
    - Dictionary containing updated node information.
    """
    node = node_service.cordon_node(name)

    return {
        "name": node.metadata.name if node.metadata else None,
        "unschedulable": node.spec.unschedulable if node.spec else None,
    }


@tool
def uncordon_node(name: str):
    """
    Mark a Kubernetes node as schedulable.

    Parameters:
    - name: Name of the node.

    Returns:
    - Dictionary containing updated node information.
    """
    node = node_service.uncordon_node(name)

    return {
        "name": node.metadata.name if node.metadata else None,
        "unschedulable": node.spec.unschedulable if node.spec else None,
    }


@tool
def drain_node(
    name: str,
    ignore_daemonsets: bool = True,
    delete_emptydir_data: bool = True,
    grace_period_seconds: int = 30,
):
    """
    Drain a Kubernetes node by evicting evictable pods.

    Parameters:
    - name: Name of the node.
    - ignore_daemonsets: Ignore DaemonSet-managed pods.
    - delete_emptydir_data: Allow deletion of pods using emptyDir volumes.
    - grace_period_seconds: Grace period before pod termination.

    Returns:
    - Dictionary containing the node name, evicted pods, and eviction count.
    """
    return node_service.drain_node(
        name=name,
        ignore_daemonsets=ignore_daemonsets,
        grace_period_seconds=grace_period_seconds,
    )


@tool
def taint_node(
    name: str,
    key: str,
    value: str,
    effect: str,
):
    """
    Add a taint to a Kubernetes node.

    Parameters:
    - name: Name of the node.
    - key: Taint key.
    - value: Taint value.
    - effect: Taint effect.

    Returns:
    - Dictionary containing updated node information.
    """
    node = node_service.taint_node(
        name=name,
        key=key,
        value=value,
        effect=effect,
    )

    return {
        "name": node.metadata.name if node.metadata else None,
        "taints": [
            {
                "key": t.key,
                "value": t.value,
                "effect": t.effect,
            }
            for t in (node.spec.taints or [])
        ]
        if node.spec
        else [],
    }


@tool
def remove_taint_node(
    name: str,
    key: str,
):
    """
    Remove a taint from a Kubernetes node.

    Parameters:
    - name: Name of the node.
    - key: Taint key to remove.

    Returns:
    - Dictionary containing updated node information.
    """
    node = node_service.remove_taint_node(
        name=name,
        key=key,
    )

    return {
        "name": node.metadata.name if node.metadata else None,
        "taints": [
            {
                "key": t.key,
                "value": t.value,
                "effect": t.effect,
            }
            for t in (node.spec.taints or [])
        ]
        if node.spec
        else [],
    }

@tool
def patch_node(
    name: str,
    patch: dict,
):
    """
    Patch a Kubernetes node.

    Parameters:
    - name: Name of the node.
    - patch: Partial node manifest.

    Returns:
    - Dictionary containing updated node information.
    """
    node = node_service.patch_node(
        name=name,
        patch=patch,
    )

    return {
        "name": node.metadata.name if node.metadata else None,
        "unschedulable": node.spec.unschedulable if node.spec else None,
        "taints": [
            {
                "key": t.key,
                "value": t.value,
                "effect": t.effect,
            }
            for t in (node.spec.taints or [])
        ]
        if node.spec
        else [],
    }

@tool
def node_exists(
    name: str,
):
    """
    Check whether a Kubernetes node exists.

    Parameters:
    - name: Name of the node.

    Returns:
    - True if the node exists, otherwise False.
    """
    return node_service.node_exists(name)