from kubernetes.client import V1Pod
from state.schema.pod_info import PodInfo


def pod_to_dict(
    pod: V1Pod,
) -> PodInfo:
    metadata = pod.metadata
    spec = pod.spec
    status = pod.status

    assert metadata is not None
    assert metadata.name is not None
    assert metadata.namespace is not None

    return {
        "name": metadata.name,
        "namespace": metadata.namespace,
        "labels": metadata.labels,
        "status": status.phase if status else None,
        "node_name": spec.node_name if spec else None,
    }