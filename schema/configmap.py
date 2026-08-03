from pydantic import BaseModel, Field


class ConfigMapMetadataSchema(BaseModel):
    name: str = Field(
        ...,
        description="Name of the ConfigMap.",
    )
    namespace: str = Field(
        ...,
        description="Namespace of the ConfigMap.",
    )
    labels: dict[str, str] = Field(
        default_factory=dict,
        description="Labels attached to the ConfigMap.",
    )


class CreateConfigMapSchema(BaseModel):
    api_version: str = Field(
        default="v1",
        description="Kubernetes API version.",
    )
    kind: str = Field(
        default="ConfigMap",
        description="Kubernetes resource kind.",
    )
    metadata: ConfigMapMetadataSchema
    data: dict[str, str] = Field(
        default_factory=dict,
        description="Key-value pairs stored in the ConfigMap.",
    )
    binary_data: dict[str, str] = Field(
        default_factory=dict,
        description="Binary data stored in the ConfigMap (base64 encoded).",
    )
