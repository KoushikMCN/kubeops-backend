from typing import Optional, cast

from kubernetes.client import V1Pod, V1PodList, CoreV1EventList
from kubernetes.client.rest import ApiException

from services.kubernetes.client import core_v1

from state.pod_state import PodEvent


class PodService:
    """Service for Kubernetes Pod operations."""

    def __init__(self):
        self.core_v1 = core_v1

    def create_pod(self, namespace: str, pod: V1Pod) -> V1Pod:
        """Create a pod in the specified namespace."""
        return cast(
            V1Pod,
            self.core_v1.create_namespaced_pod(
                namespace=namespace,
                body=pod,
            ),
        )

    def list_pods(
        self,
        namespace: str | None = None,
        label_selector: str | None = None,
    ) -> V1PodList:
        """
        List pods in a namespace or across all namespaces.
        """

        if namespace:
            return cast(
                V1PodList,
                self.core_v1.list_namespaced_pod(
                    namespace=namespace,
                    label_selector=label_selector,
                ),
            )

        return cast(
            V1PodList,
            self.core_v1.list_pod_for_all_namespaces(
                label_selector=label_selector,
            ),
        )

    # def get_pod(self, name: str, namespace: str) -> V1Pod:
    #     """Get a pod by name."""
    #     return cast(
    #         V1Pod,
    #         self.core_v1.read_namespaced_pod(
    #             name=name,
    #             namespace=namespace,
    #         ),
    #     )

    def describe_pod(self, name: str, namespace: str):
        """Get a pod by name."""
        return self.core_v1.read_namespaced_pod(
            name=name,
            namespace=namespace,
        )

    def get_pod_logs(
        self,
        name: str,
        namespace: str,
        tail_lines: int = 100,
    ) -> str:
        """Fetch logs from a pod."""
        return cast(
            str,
            self.core_v1.read_namespaced_pod_log(
                name=name,
                namespace=namespace,
                tail_lines=tail_lines,
            ),
        )

    def delete_pod(self, name: str, namespace: str):
        """Delete a pod."""
        self.core_v1.delete_namespaced_pod(
            name=name,
            namespace=namespace,
        )

        return f"Pod '{name}' deleted successfully."

    def pod_exists(self, name: str, namespace: str) -> bool:
        """Check whether a pod exists."""
        try:
            self.core_v1.read_namespaced_pod(
                name=name,
                namespace=namespace,
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise

    def get_pod_events(
        self,
        namespace: str,
        pod_name: str,
    ) -> list[PodEvent]:
        """Get all events associated with a pod."""

        events = cast(
            CoreV1EventList,
            self.core_v1.list_namespaced_event(
                namespace=namespace,
                field_selector=(
                    f"involvedObject.kind=Pod,"
                    f"involvedObject.name={pod_name}"
                ),
            ),
        )

        return [
            {
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "count": event.count,
                "last_timestamp": event.last_timestamp,
            }
            for event in (events.items or [])
        ]