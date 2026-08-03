from .pod import *
from .deployment import *
from .svc import *
from .node import *
from .namespace import *
from .configmap import *
from .secret import *

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

    # Services
    list_services,
    get_service,
    create_service,
    delete_service,
    patch_service,

    # Nodes
    list_nodes,
    get_node,
    cordon_node,
    uncordon_node,
    taint_node,
    remove_taint_node,
    drain_node,
    node_exists,

    # Namespaces
    list_namespaces,
    get_namespace,
    create_namespace,
    delete_namespace,
    namespace_exists,

    # ConfigMaps
    list_configmaps,
    get_configmap,
    create_configmap,
    patch_configmap,
    delete_configmap,
    configmap_exists,

    # Secrets
    list_secrets,
    get_secret_metadata,
    create_secret,
    patch_secret,
    delete_secret,
    secret_exists,
]