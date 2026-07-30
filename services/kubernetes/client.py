"""
Kubernetes client initialization and management.
"""

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


class KubernetesClient:
    """Singleton Kubernetes client manager."""

    _initialized = False

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized:
            return

        try:
            # Local development
            config.load_kube_config()
            print("Loaded local kubeconfig.")
        except ConfigException:
            # Running inside a Kubernetes pod
            config.load_incluster_config()
            print("Loaded in-cluster configuration.")

        cls.core_v1 = client.CoreV1Api()
        cls.apps_v1 = client.AppsV1Api()
        cls.networking_v1 = client.NetworkingV1Api()

        cls._initialized = True


# Initialize once when imported
KubernetesClient.initialize()

core_v1 = KubernetesClient.core_v1
apps_v1 = KubernetesClient.apps_v1
networking_v1 = KubernetesClient.networking_v1
