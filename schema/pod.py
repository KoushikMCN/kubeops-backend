from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .container import ContainerSchema
from .metadata import MetadataSchema

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