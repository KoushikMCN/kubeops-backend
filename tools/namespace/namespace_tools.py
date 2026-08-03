from langchain_core.tools import tool
from kubernetes.client import (
    V1Namespace,
    V1ObjectMeta,
)

from schema.namespace import CreateNamespaceSchema
from services.kubernetes.namespace_service import NamespaceService

namespace_service = NamespaceService()


@tool
def list_namespaces():
    """
    List Kubernetes namespaces.

    Returns:
    - A list of dictionaries containing namespace information.
    """
    namespace_list = namespace_service.list_namespaces()

    return [
        {
            "name": ns.metadata.name,
            "status": ns.status.phase if ns.status else None,
        }
        for ns in (namespace_list.items or [])
    ]


@tool
def get_namespace(
    name: str,
):
    """
    Get information about a Kubernetes namespace.

    Parameters:
    - name: Name of the namespace.

    Returns:
    - Dictionary containing namespace information.
    """
    namespace = namespace_service.get_namespace(name)

    metadata = namespace.metadata
    status = namespace.status

    return {
        "name": metadata.name if metadata else None,
        "labels": metadata.labels if metadata else None,
        "annotations": metadata.annotations if metadata else None,
        "status": status.phase if status else None,
    }


@tool
def create_namespace(
    namespace: CreateNamespaceSchema,
):
    """
    Create a Kubernetes namespace.

    Parameters:
    - namespace: Namespace specification.

    Returns:
    - Dictionary containing created namespace information.
    """

    namespace_to_create = V1Namespace(
        api_version=namespace.api_version,
        kind=namespace.kind,
        metadata=V1ObjectMeta(
            name=namespace.metadata.name,
            labels=namespace.metadata.labels,
        ),
    )

    created_namespace = namespace_service.create_namespace(
        namespace_to_create,
    )

    return {
        "name": created_namespace.metadata.name
        if created_namespace.metadata
        else None,
        "status": created_namespace.status.phase
        if created_namespace.status
        else None,
    }


@tool
def delete_namespace(
    name: str,
):
    """
    Delete a Kubernetes namespace.

    Parameters:
    - name: Name of the namespace.

    Returns:
    - Message indicating successful deletion.
    """
    return namespace_service.delete_namespace(
        name=name,
    )

@tool
def namespace_exists(
    name: str,
):
    """
    Check whether a Kubernetes namespace exists.

    Parameters:
    - name: Name of the namespace.

    Returns:
    - True if the namespace exists, otherwise False.
    """
    return namespace_service.namespace_exists(
        name=name,
    )