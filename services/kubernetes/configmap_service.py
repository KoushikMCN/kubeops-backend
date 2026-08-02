from typing import Any, Optional, cast

from kubernetes.client import (
    V1ConfigMap,
    V1ConfigMapList,
    V1DeleteOptions,
)
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1


class ConfigMapService:
    """Service for Kubernetes ConfigMap operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def create_configmap(
        self,
        namespace: str,
        configmap: V1ConfigMap,
    ) -> V1ConfigMap:
        """Create a ConfigMap in the specified namespace."""
        return cast(
            V1ConfigMap,
            self.core_v1.create_namespaced_config_map(
                namespace=namespace,
                body=configmap,
            ),
        )

    def list_configmaps(
        self,
        namespace: Optional[str] = None,
    ) -> V1ConfigMapList:
        """List ConfigMaps in a namespace or across all namespaces."""
        if namespace:
            return cast(
                V1ConfigMapList,
                self.core_v1.list_namespaced_config_map(
                    namespace=namespace,
                ),
            )

        return cast(
            V1ConfigMapList,
            self.core_v1.list_config_map_for_all_namespaces(),
        )

    def get_configmap(
        self,
        name: str,
        namespace: str,
    ) -> V1ConfigMap:
        """Get a ConfigMap by name."""
        return cast(
            V1ConfigMap,
            self.core_v1.read_namespaced_config_map(
                name=name,
                namespace=namespace,
            ),
        )

    def patch_configmap(
        self,
        name: str,
        namespace: str,
        patch: dict[str, Any],
    ) -> V1ConfigMap:
        """Patch an existing ConfigMap."""
        return cast(
            V1ConfigMap,
            self.core_v1.patch_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=patch,
            ),
        )

    def delete_configmap(
        self,
        name: str,
        namespace: str,
    ) -> str:
        """Delete a ConfigMap."""
        self.core_v1.delete_namespaced_config_map(
            name=name,
            namespace=namespace,
            body=V1DeleteOptions(),
        )

        return f"ConfigMap '{name}' deleted successfully."

    def configmap_exists(
        self,
        name: str,
        namespace: str,
    ) -> bool:
        """Check whether a ConfigMap exists."""
        try:
            self.core_v1.read_namespaced_config_map(
                name=name,
                namespace=namespace,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise