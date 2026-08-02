from typing import cast

from kubernetes.client import (
    V1DeleteOptions,
    V1Namespace,
    V1NamespaceList,
)
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1


class NamespaceService:
    """Service for Kubernetes Namespace operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def create_namespace(
        self,
        namespace: V1Namespace,
    ) -> V1Namespace:
        """Create a namespace."""
        return cast(
            V1Namespace,
            self.core_v1.create_namespace(
                body=namespace,
            ),
        )

    def list_namespaces(self) -> V1NamespaceList:
        """List all namespaces."""
        return cast(
            V1NamespaceList,
            self.core_v1.list_namespace(),
        )

    def get_namespace(
        self,
        name: str,
    ) -> V1Namespace:
        """Get a namespace by name."""
        return cast(
            V1Namespace,
            self.core_v1.read_namespace(
                name=name,
            ),
        )

    def delete_namespace(
        self,
        name: str,
    ) -> str:
        """Delete a namespace."""
        self.core_v1.delete_namespace(
            name=name,
            body=V1DeleteOptions(),
        )

        return f"Namespace '{name}' deleted successfully."

    def namespace_exists(
        self,
        name: str,
    ) -> bool:
        """Check whether a namespace exists."""
        try:
            self.core_v1.read_namespace(
                name=name,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise