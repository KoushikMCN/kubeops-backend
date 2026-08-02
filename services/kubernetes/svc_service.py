from typing import Any, Optional, cast

from kubernetes.client import (
    V1DeleteOptions,
    V1Service,
    V1ServiceList,
)
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1


class ServiceService:
    """Service for Kubernetes Service operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def create_service(
        self,
        namespace: str,
        service: V1Service,
    ) -> V1Service:
        """Create a service in the specified namespace."""
        return cast(
            V1Service,
            self.core_v1.create_namespaced_service(
                namespace=namespace,
                body=service,
            ),
        )

    def list_services(
        self,
        namespace: Optional[str] = None,
    ) -> V1ServiceList:
        """List all services in a namespace or across all namespaces."""
        if namespace:
            return cast(
                V1ServiceList,
                self.core_v1.list_namespaced_service(namespace),
            )

        return cast(
            V1ServiceList,
            self.core_v1.list_service_for_all_namespaces(),
        )

    def describe_service(
        self,
        name: str,
        namespace: str,
    ) -> V1Service:
        """Get a service by name."""
        return cast(
            V1Service,
            self.core_v1.read_namespaced_service(
                name=name,
                namespace=namespace,
            ),
        )

    def delete_service(
        self,
        name: str,
        namespace: str,
    ) -> str:
        """Delete a service."""
        self.core_v1.delete_namespaced_service(
            name=name,
            namespace=namespace,
            body=V1DeleteOptions(),
        )

        return f"Service '{name}' deleted successfully."

    def service_exists(
        self,
        name: str,
        namespace: str,
    ) -> bool:
        """Check whether a service exists."""
        try:
            self.core_v1.read_namespaced_service(
                name=name,
                namespace=namespace,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise

    def patch_service(
        self,
        name: str,
        namespace: str,
        patch: dict[str, Any],
    ) -> V1Service:
        """
        Patch an existing service.

        Parameters:
        - name: Name of the service.
        - namespace: Namespace of the service.
        - patch: Partial service manifest to apply.

        Returns:
        - Updated V1Service object.
        """
        return cast(
            V1Service,
            self.core_v1.patch_namespaced_service(
                name=name,
                namespace=namespace,
                body=patch,
            ),
        )