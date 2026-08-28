from graphs.remediation import build_remediation_graph

from rich import print
from rich.console import Console
from rich.panel import Panel


graph = build_remediation_graph()


result = graph.invoke(
    {
        # Input from the diagnostic workflow
        "namespace": "default",
        "resource_type": "deployment",
        "resource_name": "crash-demo",
        "diagnosis": """
The container crash-demo is repeatedly crashing and restarting,
causing the pod to enter a CrashLoopBackOff state.

The container likely exits immediately after startup because its
entrypoint command is short-lived or fails.

Suggested fix: Review and modify the container command and args.
Ensure the container runs a long-lived process. For a busybox image,
a possible command is: sh -c "sleep infinity".
""",

        # Remediation plan
        "remediation_plan": None,

        # Validation
        "plan_valid": False,
        "validation_error": None,

        # Approval
        "approved": None,

        # Execution
        "execution_result": None,
        "execution_error": None,

        # Verification
        "verification_result": None,
        "resolved": None,
    }
)


console = Console()

console.print(
    Panel.fit(
        str(result["remediation_plan"]),
        title="Generated Remediation Plan",
    )
)

console.print()

console.print(
    f"[bold]Plan Valid:[/bold] {result['plan_valid']}"
)

if result["validation_error"]:
    console.print(
        f"[bold red]Validation Error:[/bold red] "
        f"{result['validation_error']}"
    )