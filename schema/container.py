from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class EnvVarSchema(BaseModel):
    name: str
    value: str

class ResourceRequirementsSchema(BaseModel):
    limits: Dict[str, str] = Field(default_factory=dict)
    requests: Dict[str, str] = Field(default_factory=dict)

class ContainerPortSchema(BaseModel):
    container_port: int = Field(alias="containerPort")
    protocol: Literal["TCP", "UDP", "SCTP"] = "TCP"

    model_config = {
        "populate_by_name": True,
    }

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