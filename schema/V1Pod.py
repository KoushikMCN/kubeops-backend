from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ContainerPortSchema(BaseModel):
    container_port: int = Field(alias="containerPort")
    protocol: Literal["TCP", "UDP", "SCTP"] = "TCP"

    model_config = {
        "populate_by_name": True,
    }


class EnvVarSchema(BaseModel):
    name: str
    value: str


class ResourceRequirementsSchema(BaseModel):
    limits: Dict[str, str] = Field(default_factory=dict)
    requests: Dict[str, str] = Field(default_factory=dict)


class ContainerSchema(BaseModel):
    name: str
    image: str

    image_pull_policy: Optional[
        Literal["Always", "IfNotPresent", "Never"]
    ] = Field(default=None, alias="imagePullPolicy")

    command: List[str] = Field(default_factory=list)
    args: List[str] = Field(default_factory=list)

    ports: List[ContainerPortSchema] = Field(default_factory=list)
    env: List[EnvVarSchema] = Field(default_factory=list)

    resources: Optional[ResourceRequirementsSchema] = None

    model_config = {
        "populate_by_name": True,
    }


class MetadataSchema(BaseModel):
    name: str
    namespace: Optional[str] = None

    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)


class PodSpecSchema(BaseModel):
    containers: List[ContainerSchema]

    restart_policy: Literal[
        "Always",
        "OnFailure",
        "Never",
    ] = Field(default="Always", alias="restartPolicy")

    service_account_name: Optional[str] = Field(
        default=None,
        alias="serviceAccountName",
    )

    node_selector: Dict[str, str] = Field(
        default_factory=dict,
        alias="nodeSelector",
    )

    image_pull_secrets: List[str] = Field(
        default_factory=list,
        alias="imagePullSecrets",
    )

    model_config = {
        "populate_by_name": True,
    }


class CreatePodSchema(BaseModel):
    api_version: str = Field(default="v1", alias="apiVersion")
    kind: str = "Pod"

    metadata: MetadataSchema
    spec: PodSpecSchema

    model_config = {
        "populate_by_name": True,
    }