from kubernetes.client import V1Deployment
from state.deployment_state import DeploymentInfo


def deployment_to_dict(
    deployment: V1Deployment,
) -> DeploymentInfo:
    """
    Convert a V1Deployment into an LLM-friendly dictionary.
    """

    metadata = deployment.metadata
    spec = deployment.spec
    status = deployment.status

    assert metadata is not None
    assert metadata.name is not None
    assert metadata.namespace is not None

    assert spec is not None
    assert spec.selector is not None

    assert status is not None
    return {
        "name": metadata.name,
        "namespace": metadata.namespace,
        "labels": metadata.labels,
        "selector": spec.selector.match_labels or {},
        "annotations": metadata.annotations,
        "replicas": spec.replicas,
        "ready_replicas": status.ready_replicas,
        "available_replicas": status.available_replicas,
        "updated_replicas": status.updated_replicas,
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message,
            }
            for c in (status.conditions or [])
        ],
    }