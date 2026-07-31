from ctypes import cast

from langchain_core.tools import tool
from kubernetes.client import V1Container, V1ContainerPort, V1ObjectMeta, V1Pod, V1PodSpec, V1PodStatus
from schema.pod import CreatePodSchema
from services.kubernetes.pod_service import PodService

pod_service = PodService()

@tool
def list_pods(namespace: str | None = None):
    """
    List Kubernetes pods.
    Parameters:
    - namespace: The namespace to list pods from. If None, lists pods from all namespaces.
    Returns:
    - A list of dictionaries containing pod information (name, namespace, status).
    """
    pod_list = pod_service.list_pods(namespace)

    return [
        {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
        }
        for pod in (pod_list.items or [])
    ]

@tool
def get_pod_logs(
    pod_name: str,
    namespace: str,
    tail_lines: int = 100,
):
    """
    Get logs from a Kubernetes pod.
    Parameters:
    - pod_name: The name of the pod.
    - namespace: The namespace of the pod.
    - tail_lines: The number of lines to retrieve from the end of the logs.
    Returns:
    - A string containing the logs of the specified pod.
    """
    return pod_service.get_pod_logs(
        name=pod_name,
        namespace=namespace,
        tail_lines=tail_lines,
    )

@tool
def create_pod(
    pod: CreatePodSchema,
    namespace: str,
):
    """
    Create a Kubernetes pod.
    Parameters:
    - namespace: The namespace in which to create the pod.
    - pod: The pod specification as a CreatePodSchema object.
    Returns:
    - A dictionary containing the name, namespace, and status of the created pod.
    """
    pod_to_create = V1Pod(
        api_version=pod.api_version,
        kind=pod.kind,
        metadata=V1ObjectMeta(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace,
        ),
        spec=V1PodSpec(
            containers=[
                V1Container(
                    name=c.name,
                    image=c.image,
                    ports=[
                        V1ContainerPort(
                            container_port=p.container_port,
                            protocol=p.protocol,
                        )
                        for p in c.ports
                    ],
                )
                for c in pod.spec.containers
            ]
        ),
    )
    created_pod = pod_service.create_pod(namespace, pod_to_create)
    return {
        "name": created_pod.metadata.name if created_pod.metadata else None,
        "namespace": created_pod.metadata.namespace if created_pod.metadata else None,
        "status": created_pod.status.phase if created_pod.status else None,
    }

@tool
def get_pod(name:str, namespace:str):
    """
    Describe a kubernetes pod from it's name
    Parameters:
    - name: name of the pod
    - namespace: namespace the pod resides in
    Returns:
    - dictionary containing pod information
    """
    pod = pod_service.describe_pod(name, namespace)
    return pod

@tool
def delete_pod(name:str, namespace:str):
    """
    Delete a kubernetes pod using it's name & namespace
    Parameters:
    - name: name of the pod
    - namespace: namespace the pod resides in
    Returns:
    - Message saying pod is deleted successfully
    """
    delete_message = pod_service.delete_pod(name, namespace)
    return delete_message

@tool
def get_pod_events(name:str, namespace:str):
    """
    Get a kubernetes pod's events using it's name & namespace
    Parameters:
    - name: name of the pod
    - namespace: namespace the pod resides in
    Returns:
    - List of dict of events containing: type, reason, message, count, last_timestamp
    """
    pod_events = pod_service.get_pod_events(name, namespace)
    return pod_events
