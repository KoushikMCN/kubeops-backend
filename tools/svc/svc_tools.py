from langchain_core.tools import tool
from kubernetes.client import (
    V1ObjectMeta,
    V1Service,
    V1ServicePort,
    V1ServiceSpec,
)

from schema.svc import CreateServiceSchema
from services.kubernetes.svc_service import SvcService

service_service = SvcService()


@tool
def list_services(namespace: str | None = None):
    """
    List Kubernetes services.

    Parameters:
    - namespace: The namespace to list services from. If None, lists services from all namespaces.

    Returns:
    - A list of dictionaries containing service information.
    """
    service_list = service_service.list_services(namespace)

    return [
        {
            "name": svc.metadata.name,
            "namespace": svc.metadata.namespace,
            "type": svc.spec.type,
            "cluster_ip": svc.spec.cluster_ip,
        }
        for svc in (service_list.items or [])
    ]


@tool
def get_service(
    name: str,
    namespace: str,
):
    """
    Describe a Kubernetes service.

    Parameters:
    - name: Name of the service.
    - namespace: Namespace the service resides in.

    Returns:
    - Dictionary containing service information.
    """
    service = service_service.describe_service(
        name=name,
        namespace=namespace,
    )

    metadata = service.metadata
    spec = service.spec

    return {
        "name": metadata.name if metadata else None,
        "namespace": metadata.namespace if metadata else None,
        "labels": metadata.labels if metadata else None,
        "annotations": metadata.annotations if metadata else None,
        "type": spec.type if spec else None,
        "cluster_ip": spec.cluster_ip if spec else None,
        "selector": spec.selector if spec else None,
        "ports": [
            {
                "name": p.name,
                "port": p.port,
                "target_port": p.target_port,
                "protocol": p.protocol,
            }
            for p in (spec.ports or [])
        ]
        if spec
        else [],
    }


@tool
def create_service(
    service: CreateServiceSchema,
    namespace: str,
):
    """
    Create a Kubernetes service.

    Parameters:
    - namespace: Namespace in which to create the service.
    - service: Service specification.

    Returns:
    - Dictionary containing created service information.
    """

    service_to_create = V1Service(
        api_version=service.api_version,
        kind=service.kind,
        metadata=V1ObjectMeta(
            name=service.metadata.name,
            namespace=service.metadata.namespace,
            labels=service.metadata.labels,
        ),
        spec=V1ServiceSpec(
            type=service.spec.type,
            selector=service.spec.selector,
            ports=[
                V1ServicePort(
                    port=p.port,
                    target_port=p.target_port,
                    protocol=p.protocol,
                    name=p.name,
                )
                for p in service.spec.ports
            ],
        ),
    )

    created_service = service_service.create_service(
        namespace=namespace,
        service=service_to_create,
    )

    return {
        "name": created_service.metadata.name if created_service.metadata else None,
        "namespace": created_service.metadata.namespace if created_service.metadata else None,
        "type": created_service.spec.type if created_service.spec else None,
        "cluster_ip": created_service.spec.cluster_ip if created_service.spec else None,
    }


@tool
def delete_service(
    name: str,
    namespace: str,
):
    """
    Delete a Kubernetes service.

    Parameters:
    - name: Name of the service.
    - namespace: Namespace the service resides in.

    Returns:
    - Message indicating successful deletion.
    """
    return service_service.delete_service(
        name=name,
        namespace=namespace,
    )


@tool
def patch_service(
    name: str,
    namespace: str,
    patch: dict,
):
    """
    Patch a Kubernetes service.

    Parameters:
    - name: Name of the service.
    - namespace: Namespace the service resides in.
    - patch: Partial service manifest.

    Returns:
    - Dictionary containing updated service information.
    """

    updated_service = service_service.patch_service(
        name=name,
        namespace=namespace,
        patch=patch,
    )

    return {
        "name": updated_service.metadata.name if updated_service.metadata else None,
        "namespace": updated_service.metadata.namespace if updated_service.metadata else None,
        "type": updated_service.spec.type if updated_service.spec else None,
        "cluster_ip": updated_service.spec.cluster_ip if updated_service.spec else None,
    }