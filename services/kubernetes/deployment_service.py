from typing import Optional, cast
from kubernetes.client import (
    AppsV1Api,
    V1DeleteOptions,
    V1Deployment,
    V1DeploymentList,
)

class DeploymentService:
    def __init__(self):
        self.apps_v1 = AppsV1Api()

    def list_deployments(
        self,
        namespace: Optional[str] = None,
    ) -> V1DeploymentList:
        """
        List all deployments in a namespace.
        """
        if namespace:
            return cast(V1DeploymentList, 
                self.apps_v1.list_namespaced_deployment(
                namespace=namespace
            ))
        return cast(V1DeploymentList, 
            self.apps_v1.list_deployment_for_all_namespaces(
            namespace=namespace
        ))

    def get_deployment(
        self,
        namespace: str,
        deployment_name: str,
    ) -> V1Deployment:
        """
        Get a deployment by name.
        """
        return cast(V1Deployment,
            self.apps_v1.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
        ))

    def create_deployment(
        self,
        namespace: str,
        deployment: V1Deployment,
    ) -> V1Deployment:
        """
        Create a deployment.
        """
        return cast(V1Deployment,
            self.apps_v1.create_namespaced_deployment(
            namespace=namespace,
            body=deployment,
        ))

    def delete_deployment(
        self,
        namespace: str,
        deployment_name: str,
    ):
        """
        Delete a deployment.
        """
        return self.apps_v1.delete_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=V1DeleteOptions(),
        )

    def scale_deployment(
        self,
        namespace: str,
        deployment_name: str,
        replicas: int,
    ) -> V1Deployment:
        """
        Scale a deployment.
        """
        deployment = cast(V1Deployment,
            self.apps_v1.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
        ))

        if deployment.spec is None:
            raise RuntimeError("Deployment has no spec.")

        deployment.spec.replicas = replicas

        return cast(V1Deployment,
            self.apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment,
        ))

    def restart_deployment(
        self,
        namespace: str,
        deployment_name: str,
    ) -> V1Deployment:
        """
        Trigger a rolling restart by updating the restart annotation.
        """
        from datetime import datetime, timezone

        body = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt":
                                datetime.now(timezone.utc).isoformat()
                        }
                    }
                }
            }
        }

        return cast(V1Deployment,
            self.apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=body,
        ))

    def rollout_status(
        self,
        namespace: str,
        deployment_name: str,
    ) -> V1Deployment:
        """
        Get the current rollout status.
        """
        return cast(V1Deployment,
            self.apps_v1.read_namespaced_deployment_status(
            name=deployment_name,
            namespace=namespace,
        ))

    def rollback_deployment(
        self,
        namespace: str,
        deployment_name: str,
        revision: int,
    ):
        """
        Rollback is NOT supported by the Kubernetes Python client.
        This should be implemented by invoking:
            kubectl rollout undo
        or by integrating with Helm/ArgoCD.
        """
        raise NotImplementedError(
            "Deployment rollback is not supported by the Kubernetes Python client."
        )