from langchain_core.tools import tool
from kubernetes.client import V1Deployment, V1ObjectMeta, V1Container, V1PodTemplateSpec, V1DeploymentSpec, V1LabelSelector, V1PodSpec, V1ContainerPort

from services.kubernetes.deployment_service import DeploymentService
from schema.deployment import CreateDeploymentSchema

deployment_service = DeploymentService()


@tool
def list_deployments(namespace: str | None = None):
    """
    List all deployments in a namespace.
    Arguments: 
    - namespace: str of the namespace. If none, will return deployments in all namespaces
    Returns:
    - List of deployments
    """
    deployments = deployment_service.list_deployments(namespace)
    return [
        {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "conditions": [
                {
                    "type": c.type,
                    "status": c.status,
                    "reason": c.reason,
                    "message": c.message
                }
                for c in (deployment.status.conditions or [])
            ]
        }
        for deployment in (deployments.items or [])
    ]


@tool
def get_deployment(namespace: str, deployment_name: str) -> V1Deployment:
    """
    Get a deployment.
    Parameters:
    - namespace: the namespace in which the deployment exists
    - deployment_name: the name of the deployment to be retrieved
    Returns:
    - Deployment details of type V1Deployment
    """
    return deployment_service.get_deployment(namespace, deployment_name)


@tool
def create_deployment(namespace: str, deployment: CreateDeploymentSchema):
    """
    Create a deployment under a given namespace.
    Parameters:
    - namespace: the namespace in which you want to create the deployment
    - deployment: The deployment specification as a CreateDeploymentSchema object.
    Returns:
    - The dictionary containing the name, namespace and the conditions of the newly created deployment
    """
    deployment_to_create = V1Deployment(
        api_version=deployment.api_version,
        kind=deployment.kind,
        metadata=V1ObjectMeta(
            name=deployment.metadata.name,
            namespace=deployment.metadata.namespace,
            labels=deployment.metadata.labels,
        ),
        spec=V1DeploymentSpec(
            replicas=deployment.spec.replicas,
            selector=V1LabelSelector(
                match_labels=deployment.metadata.labels,
            ),
            template=V1PodTemplateSpec(
                metadata=V1ObjectMeta(
                    labels=deployment.metadata.labels,
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
                        for c in deployment.spec.containers
                    ]
                ),
            ),
        ),
    )
    created_deployment = deployment_service.create_deployment(namespace, deployment_to_create)
    return {
        "name": created_deployment.metadata.name if created_deployment.metadata else None,
        "namespace": created_deployment.metadata.namespace if created_deployment.metadata else None,
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message
            }
            for c in (created_deployment.status.conditions if created_deployment.status and created_deployment.status.conditions else [])
        ]
    }


@tool
def delete_deployment(namespace: str, deployment_name: str):
    """
    Delete a deployment.
    Parameters:
    - namespace: Namespace of the deployment.
    - deployment_name: Name of the deployment.
    Returns:
    - Success message.
    """
    deployment_service.delete_deployment(namespace, deployment_name)
    return {
        "message": f"Deployment '{deployment_name}' deleted successfully.",
        "namespace": namespace,
    }


@tool
def scale_deployment(namespace: str, deployment_name: str, replicas: int):
    """
    Scale a deployment.
    Parameters:
    - namespace: Namespace of the deployment.
    - deployment_name: Name of the deployment.
    - replicas: Desired replica count.
    Returns:
    - Updated deployment summary.
    """
    deployment = deployment_service.scale_deployment(
        namespace,
        deployment_name,
        replicas,
    )

    return {
        "name": deployment.metadata.name if deployment.metadata else None,
        "namespace": deployment.metadata.namespace if deployment.metadata else None,
        "replicas": deployment.spec.replicas if deployment.spec else None,
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message,
            }
            for c in (deployment.status.conditions if deployment.status else [])
        ],
    }


@tool
def restart_deployment(namespace: str, deployment_name: str):
    """
    Restart a deployment.
    Parameters:
    - namespace: Namespace of the deployment.
    - deployment_name: Name of the deployment.
    Returns:
    - Updated deployment summary.
    """
    deployment = deployment_service.restart_deployment(
        namespace,
        deployment_name,
    )

    return {
        "name": deployment.metadata.name if deployment.metadata else None,
        "namespace": deployment.metadata.namespace if deployment.metadata else None,
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message,
            }
            for c in (deployment.status.conditions if deployment.status else [])
        ],
    }


@tool
def rollout_status(namespace: str, deployment_name: str):
    """
    Get the rollout status of a deployment.
    Parameters:
    - namespace: Namespace of the deployment.
    - deployment_name: Name of the deployment.
    Returns:
    - Rollout status summary.
    """
    deployment = deployment_service.rollout_status(
        namespace,
        deployment_name,
    )

    return {
        "name": deployment.metadata.name if deployment.metadata else None,
        "namespace": deployment.metadata.namespace if deployment.metadata else None,
        "desired_replicas": deployment.spec.replicas if deployment.spec else None,
        "updated_replicas": deployment.status.updated_replicas if deployment.status else None,
        "ready_replicas": deployment.status.ready_replicas if deployment.status else None,
        "available_replicas": deployment.status.available_replicas if deployment.status else None,
        "observed_generation": deployment.status.observed_generation if deployment.status else None,
        "conditions": [
            {
                "type": c.type,
                "status": c.status,
                "reason": c.reason,
                "message": c.message,
            }
            for c in (deployment.status.conditions if deployment.status else [])
        ],
    }