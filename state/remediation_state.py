from typing import Any, TypedDict

from schema.remediation import RemediationPlan


class RemediationState(TypedDict):
    # Input from the diagnostic workflow
    namespace: str
    resource_type: str
    resource_name: str
    diagnosis: str

    # Generated remediation plan
    remediation_plan: RemediationPlan | None

    # Validation
    plan_valid: bool
    validation_error: str | None

    # Approval
    approved: bool | None

    # Execution
    execution_result: str | None
    execution_error: str | None

    # Verification
    verification_result: str | None
    resolved: bool | None