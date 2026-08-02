from typing import Any, Optional, cast

from kubernetes.client import (
    V1DeleteOptions,
    V1Secret,
    V1SecretList,
)
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1


class SecretService:
    """Service for Kubernetes Secret operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def create_secret(
        self,
        namespace: str,
        secret: V1Secret,
    ) -> V1Secret:
        """Create a Secret in the specified namespace."""
        return cast(
            V1Secret,
            self.core_v1.create_namespaced_secret(
                namespace=namespace,
                body=secret,
            ),
        )

    def list_secrets(
        self,
        namespace: Optional[str] = None,
    ) -> V1SecretList:
        """List Secrets in a namespace or across all namespaces."""
        if namespace:
            return cast(
                V1SecretList,
                self.core_v1.list_namespaced_secret(
                    namespace=namespace,
                ),
            )

        return cast(
            V1SecretList,
            self.core_v1.list_secret_for_all_namespaces(),
        )

    def get_secret_metadata(
        self,
        name: str,
        namespace: str,
    ) -> dict[str, Any]:
        """
        Get Secret metadata only.

        Secret data is intentionally omitted.
        """

        secret = cast(
            V1Secret,
            self.core_v1.read_namespaced_secret(
                name=name,
                namespace=namespace,
            ),
        )

        metadata = secret.metadata
        if metadata is None:
            raise RuntimeError("Secret metadata is missing.")

        return {
            "name": metadata.name,
            "namespace": metadata.namespace,
            "labels": metadata.labels,
            "annotations": metadata.annotations,
            "type": secret.type,
            "creation_timestamp": metadata.creation_timestamp,
        }

    def patch_secret(
        self,
        name: str,
        namespace: str,
        patch: dict[str, Any],
    ) -> V1Secret:
        """Update an existing Secret."""
        return cast(
            V1Secret,
            self.core_v1.patch_namespaced_secret(
                name=name,
                namespace=namespace,
                body=patch,
            ),
        )

    def delete_secret(
        self,
        name: str,
        namespace: str,
    ) -> str:
        """Delete a Secret."""
        self.core_v1.delete_namespaced_secret(
            name=name,
            namespace=namespace,
            body=V1DeleteOptions(),
        )

        return f"Secret '{name}' deleted successfully."

    def secret_exists(
        self,
        name: str,
        namespace: str,
    ) -> bool:
        """Check whether a Secret exists."""
        try:
            self.core_v1.read_namespaced_secret(
                name=name,
                namespace=namespace,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise