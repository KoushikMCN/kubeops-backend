from langchain_core.tools import tool
from kubernetes.client import (
    V1ConfigMap,
    V1ObjectMeta,
)

from schema.configmap import CreateConfigMapSchema
from services.kubernetes.configmap_service import ConfigMapService

configmap_service = ConfigMapService()


@tool
def list_configmaps(
    namespace: str | None = None,
):
    """
    List Kubernetes ConfigMaps.

    Parameters:
    - namespace: Namespace to list ConfigMaps from. If None, lists ConfigMaps from all namespaces.

    Returns:
    - List of dictionaries containing ConfigMap information.
    """
    configmaps = configmap_service.list_configmaps(namespace)

    return [
        {
            "name": cm.metadata.name,
            "namespace": cm.metadata.namespace,
        }
        for cm in (configmaps.items or [])
    ]


@tool
def get_configmap(
    name: str,
    namespace: str,
):
    """
    Get a Kubernetes ConfigMap.

    Parameters:
    - name: Name of the ConfigMap.
    - namespace: Namespace the ConfigMap resides in.

    Returns:
    - Dictionary containing ConfigMap information.
    """
    configmap = configmap_service.get_configmap(
        name=name,
        namespace=namespace,
    )

    metadata = configmap.metadata

    return {
        "name": metadata.name if metadata else None,
        "namespace": metadata.namespace if metadata else None,
        "labels": metadata.labels if metadata else None,
        "annotations": metadata.annotations if metadata else None,
        "data": configmap.data,
        "binary_data": configmap.binary_data,
    }


@tool
def create_configmap(
    configmap: CreateConfigMapSchema,
    namespace: str,
):
    """
    Create a Kubernetes ConfigMap.

    Parameters:
    - namespace: Namespace in which to create the ConfigMap.
    - configmap: ConfigMap specification.

    Returns:
    - Dictionary containing created ConfigMap information.
    """

    configmap_to_create = V1ConfigMap(
        api_version=configmap.api_version,
        kind=configmap.kind,
        metadata=V1ObjectMeta(
            name=configmap.metadata.name,
            namespace=configmap.metadata.namespace,
            labels=configmap.metadata.labels,
        ),
        data=configmap.data,
        binary_data=configmap.binary_data,
    )

    created_configmap = configmap_service.create_configmap(
        namespace=namespace,
        configmap=configmap_to_create,
    )

    return {
        "name": created_configmap.metadata.name
        if created_configmap.metadata
        else None,
        "namespace": created_configmap.metadata.namespace
        if created_configmap.metadata
        else None,
    }


@tool
def patch_configmap(
    name: str,
    namespace: str,
    patch: dict,
):
    """
    Patch a Kubernetes ConfigMap.

    Parameters:
    - name: Name of the ConfigMap.
    - namespace: Namespace the ConfigMap resides in.
    - patch: Partial ConfigMap manifest.

    Returns:
    - Dictionary containing updated ConfigMap information.
    """
    updated = configmap_service.patch_configmap(
        name=name,
        namespace=namespace,
        patch=patch,
    )

    return {
        "name": updated.metadata.name
        if updated.metadata
        else None,
        "namespace": updated.metadata.namespace
        if updated.metadata
        else None,
        "data": updated.data,
        "binary_data": updated.binary_data,
    }


@tool
def delete_configmap(
    name: str,
    namespace: str,
):
    """
    Delete a Kubernetes ConfigMap.

    Parameters:
    - name: Name of the ConfigMap.
    - namespace: Namespace the ConfigMap resides in.

    Returns:
    - Success message.
    """
    return configmap_service.delete_configmap(
        name=name,
        namespace=namespace,
    )


@tool
def configmap_exists(
    name: str,
    namespace: str,
):
    """
    Check whether a Kubernetes ConfigMap exists.

    Parameters:
    - name: Name of the ConfigMap.
    - namespace: Namespace the ConfigMap resides in.

    Returns:
    - True if the ConfigMap exists, otherwise False.
    """
    return configmap_service.configmap_exists(
        name=name,
        namespace=namespace,
    )