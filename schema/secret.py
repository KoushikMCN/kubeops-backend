from pydantic import BaseModel, Field

class SecretMetadataSchema(BaseModel):
    name: str
    namespace: str
    labels: dict[str, str] = Field(default_factory=dict)


class CreateSecretSchema(BaseModel):
    api_version: str = "v1"
    kind: str = "Secret"
    metadata: SecretMetadataSchema
    type: str = "Opaque"
    string_data: dict[str, str]