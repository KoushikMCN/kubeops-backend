from typing import List, Optional

from pydantic import BaseModel, Field

from .container import ContainerSchema
from .metadata import MetadataSchema

class DeploymentSpecSchema(BaseModel):
    replicas: int = 1
    containers: List[ContainerSchema]


class CreateDeploymentSchema(BaseModel):
    api_version: str = "apps/v1"
    kind: str = "Deployment"
    metadata: MetadataSchema
    spec: DeploymentSpecSchema