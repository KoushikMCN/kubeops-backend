from pydantic import BaseModel, Field


class NamespaceMetadataSchema(BaseModel):
    name: str = Field(..., description="Name of the namespace.")
    labels: dict[str, str] = Field(
        default_factory=dict,
        description="Labels attached to the namespace.",
    )


class CreateNamespaceSchema(BaseModel):
    api_version: str = Field(
        default="v1",
        description="Kubernetes API version.",
    )
    kind: str = Field(
        default="Namespace",
        description="Kubernetes resource kind.",
    )
    metadata: NamespaceMetadataSchema