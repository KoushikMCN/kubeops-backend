from kubernetes.client import V1Service

from state.schema.service_info import (
    ServiceInfo,
    ServicePortInfo,
)


def service_to_dict(
    service: V1Service,
) -> ServiceInfo:
    """
    Convert a V1Service into an LLM-friendly dictionary.
    """

    metadata = service.metadata
    spec = service.spec
    status = service.status

    assert metadata is not None
    assert spec is not None

    ports: list[ServicePortInfo] = []

    for port in spec.ports or []:
        ports.append(
            {
                "port": port.port,
                "target_port": port.target_port,
                "protocol": port.protocol,
                "node_port": port.node_port,
            }
        )

    return {
        "name": metadata.name or "",
        "namespace": metadata.namespace or "",
        "labels": metadata.labels,
        "annotations": metadata.annotations,
        "type": spec.type or "",
        "cluster_ip": spec.cluster_ip,
        "selector": spec.selector or {},
        "ports": ports,
        "external_ips": spec.external_ips,
        "load_balancer_ip": (
            status.load_balancer.ingress[0].ip
            if (
                status
                and status.load_balancer
                and status.load_balancer.ingress
                and len(status.load_balancer.ingress) > 0
            )
            else None
        ),
        "creation_timestamp": (
            metadata.creation_timestamp.isoformat()
            if metadata.creation_timestamp
            else None
        ),
    }
