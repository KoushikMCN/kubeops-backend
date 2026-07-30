from langchain_core.tools import tool
from services.kubernetes.pod_service import PodService

pod_service = PodService()

@tool
def list_pods(namespace: str | None = None):
    """
    List Kubernetes pods.
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
    """
    return pod_service.get_pod_logs(
        name=pod_name,
        namespace=namespace,
        tail_lines=tail_lines,
    )
