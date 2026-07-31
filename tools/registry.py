from .pod import *
from .deployment import *

tools = [
    # Pods
    list_pods,
    get_pod,
    create_pod,
    delete_pod,
    get_pod_logs,
    get_pod_events,

    # Deployments
    list_deployments,
    get_deployment,
    create_deployment,
    delete_deployment,
    scale_deployment,
    restart_deployment,
    rollout_status,
]