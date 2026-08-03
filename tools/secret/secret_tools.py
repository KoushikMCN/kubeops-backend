from langchain_core.tools import tool
from kubernetes.client import (
    V1ObjectMeta,
    V1Secret,
)

from schema.secret import CreateSecretSchema
from services.kubernetes.secret_service import SecretService

secret_service = SecretService()


@tool
def list_secrets(
    namespace: str | None = None,
):
    """
    List Kubernetes Secrets.

    Parameters:
    - namespace: Namespace to list Secrets from. If None, lists Secrets from all namespaces.

    Returns:
    - List of dictionaries containing Secret metadata.
    """
    secret_list = secret_service.list_secrets(namespace)

    return [
        {
            "name": secret.metadata.name,
            "namespace": secret.metadata.namespace,
            "type": secret.type,
        }
        for secret in (secret_list.items or [])
    ]


@tool
def get_secret_metadata(
    name: str,
    namespace: str,
):
    """
    Get metadata of a Kubernetes Secret.

    Parameters:
    - name: Name of the Secret.
    - namespace: Namespace the Secret resides in.

    Returns:
    - Dictionary containing Secret metadata only.
    """
    return secret_service.get_secret_metadata(
        name=name,
        namespace=namespace,
    )


@tool
def create_secret(
    secret: CreateSecretSchema,
    namespace: str,
):
    """
    Create a Kubernetes Secret.

    Parameters:
    - namespace: Namespace in which to create the Secret.
    - secret: Secret specification.

    Returns:
    - Dictionary containing created Secret information.
    """

    secret_to_create = V1Secret(
        api_version=secret.api_version,
        kind=secret.kind,
        metadata=V1ObjectMeta(
            name=secret.metadata.name,
            namespace=secret.metadata.namespace,
            labels=secret.metadata.labels,
        ),
        type=secret.type,
        string_data=secret.string_data,
    )

    created_secret = secret_service.create_secret(
        namespace=namespace,
        secret=secret_to_create,
    )

    return {
        "name": created_secret.metadata.name
        if created_secret.metadata
        else None,
        "namespace": created_secret.metadata.namespace
        if created_secret.metadata
        else None,
        "type": created_secret.type,
    }


@tool
def patch_secret(
    name: str,
    namespace: str,
    patch: dict,
):
    """
    Update a Kubernetes Secret.

    Parameters:
    - name: Name of the Secret.
    - namespace: Namespace the Secret resides in.
    - patch: Partial Secret manifest.

    Returns:
    - Dictionary containing updated Secret information.
    """
    updated_secret = secret_service.patch_secret(
        name=name,
        namespace=namespace,
        patch=patch,
    )

    return {
        "name": updated_secret.metadata.name
        if updated_secret.metadata
        else None,
        "namespace": updated_secret.metadata.namespace
        if updated_secret.metadata
        else None,
        "type": updated_secret.type,
    }


@tool
def delete_secret(
    name: str,
    namespace: str,
):
    """
    Delete a Kubernetes Secret.

    Parameters:
    - name: Name of the Secret.
    - namespace: Namespace the Secret resides in.

    Returns:
    - Success message.
    """
    return secret_service.delete_secret(
        name=name,
        namespace=namespace,
    )


@tool
def secret_exists(
    name: str,
    namespace: str,
):
    """
    Check whether a Kubernetes Secret exists.

    Parameters:
    - name: Name of the Secret.
    - namespace: Namespace the Secret resides in.

    Returns:
    - True if the Secret exists, otherwise False.
    """
    return secret_service.secret_exists(
        name=name,
        namespace=namespace,
    )