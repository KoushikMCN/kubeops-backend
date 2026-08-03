from pydantic import BaseModel, Field


class ServiceMetadataSchema(BaseModel):
    name: str = Field(..., description="Name of the service.")
    namespace: str = Field(..., description="Namespace of the service.")
    labels: dict[str, str] = Field(
        default_factory=dict,
        description="Labels attached to the service.",
    )


class ServicePortSchema(BaseModel):
    name: str | None = Field(
        default=None,
        description="Optional name of the service port.",
    )
    port: int = Field(
        ...,
        description="Port exposed by the service.",
    )
    target_port: int = Field(
        ...,
        description="Target port on the selected pods.",
    )
    protocol: str = Field(
        default="TCP",
        description="Port protocol.",
    )


class ServiceSpecSchema(BaseModel):
    selector: dict[str, str] = Field(
        ...,
        description="Pod selector labels.",
    )
    ports: list[ServicePortSchema] = Field(
        ...,
        description="Ports exposed by the service.",
    )
    type: str = Field(
        default="ClusterIP",
        description="Service type (ClusterIP, NodePort, LoadBalancer, ExternalName).",
    )


class CreateServiceSchema(BaseModel):
    api_version: str = Field(
        default="v1",
        description="Kubernetes API version.",
    )
    kind: str = Field(
        default="Service",
        description="Kubernetes resource kind.",
    )
    metadata: ServiceMetadataSchema
    spec: ServiceSpecSchema