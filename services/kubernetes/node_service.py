from typing import Any, cast

from kubernetes.client import (
    V1DeleteOptions,
    V1Node,
    V1NodeList,
    V1PodList,
)
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1


class NodeService:
    """Service for Kubernetes Node operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def list_nodes(self) -> V1NodeList:
        """List all nodes."""
        return cast(
            V1NodeList,
            self.core_v1.list_node(),
        )

    def get_node(
        self,
        name: str,
    ) -> V1Node:
        """Get a node by name."""
        return cast(
            V1Node,
            self.core_v1.read_node(
                name=name,
            ),
        )

    def cordon_node(
        self,
        name: str,
    ) -> V1Node:
        """Mark a node as unschedulable."""
        return cast(
            V1Node,
            self.core_v1.patch_node(
                name=name,
                body={
                    "spec": {
                        "unschedulable": True,
                    }
                },
            ),
        )

    def uncordon_node(
        self,
        name: str,
    ) -> V1Node:
        """Mark a node as schedulable."""
        return cast(
            V1Node,
            self.core_v1.patch_node(
                name=name,
                body={
                    "spec": {
                        "unschedulable": False,
                    }
                },
            ),
        )

    def drain_node(
        self,
        name: str,
        ignore_daemonsets: bool = True,
        delete_emptydir_data: bool = True,
        grace_period_seconds: int = 30,
    ) -> str:
        """
        Drain a node by evicting all evictable pods.

        Assumes the node has already been cordoned.
        """

        field_selector = f"spec.nodeName={name}"
        pods = cast(
            V1PodList,
            self.core_v1.list_pod_for_all_namespaces(
                field_selector=field_selector,
            ),
        )

        for pod in pods.items or []:
            metadata = pod.metadata
            spec = pod.spec

            if metadata is None or spec is None:
                continue

            namespace = metadata.namespace
            pod_name = metadata.name

            if namespace is None or pod_name is None:
                continue

            # Skip mirror/static pods
            annotations = metadata.annotations or {}
            if "kubernetes.io/config.mirror" in annotations:
                continue

            # Skip DaemonSet pods if requested
            owner_refs = metadata.owner_references or []
            if ignore_daemonsets and any(
                owner.kind == "DaemonSet"
                for owner in owner_refs
            ):
                continue

            self.core_v1.create_namespaced_pod_eviction(
                name=pod_name,
                namespace=namespace,
                body=V1DeleteOptions(
                    grace_period_seconds=grace_period_seconds,
                ),
            )

        return f"Node '{name}' drained successfully."

    def taint_node(
        self,
        name: str,
        key: str,
        value: str,
        effect: str,
    ) -> V1Node:
        """Add a taint to a node."""

        node = self.get_node(name)

        spec = node.spec
        assert spec is not None

        taints = list(spec.taints or [])

        taints.append(
            {
                "key": key,
                "value": value,
                "effect": effect,
            }
        )

        return cast(
            V1Node,
            self.core_v1.patch_node(
                name=name,
                body={
                    "spec": {
                        "taints": taints,
                    }
                },
            ),
        )

    def remove_taint_node(
        self,
        name: str,
        key: str,
    ) -> V1Node:
        """Remove a taint from a node by key."""

        node = self.get_node(name)

        spec = node.spec
        assert spec is not None

        taints = [
            {
                "key": t.key,
                "value": t.value,
                "effect": t.effect,
            }
            for t in (spec.taints or [])
            if t.key != key
        ]

        return cast(
            V1Node,
            self.core_v1.patch_node(
                name=name,
                body={
                    "spec": {
                        "taints": taints,
                    }
                },
            ),
        )

    def patch_node(
        self,
        name: str,
        patch: dict[str, Any],
    ) -> V1Node:
        """Patch an existing node."""

        return cast(
            V1Node,
            self.core_v1.patch_node(
                name=name,
                body=patch,
            ),
        )

    def node_exists(
        self,
        name: str,
    ) -> bool:
        """Check whether a node exists."""
        try:
            self.core_v1.read_node(
                name=name,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise