from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

class MetadataSchema(BaseModel):
    name: str
    namespace: Optional[str] = None

    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)