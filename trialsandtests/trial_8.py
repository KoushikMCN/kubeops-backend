from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from graphs.remediation import build_remediation_graph
from state.remediation_state import RemediationState

from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

console = Console()

graph = build_remediation_graph()

config: RunnableConfig = {
    "configurable": {
        "thread_id": "trial-remediation-1",
    }
}


# ==========================================
# 1. START THE REMEDIATION WORKFLOW
# ==========================================

initial_state: RemediationState = {
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

    "remediation_plan": None,

    "plan_valid": False,
    "validation_error": None,

    "approved": None,

    "execution_result": None,
    "execution_error": None,

    "verification_result": None,
    "resolved": None,
}


console.print(
    Panel.fit(
        "[bold cyan]Starting remediation workflow...[/bold cyan]",
        title="KubeOps",
    )
)


result = graph.invoke(
    initial_state,
    config=config,
)


# ==========================================
# 2. CHECK WHETHER GRAPH PAUSED
# ==========================================

console.print()

console.print(
    Panel.fit(
        Pretty(result),
        title="Graph Result After First Invoke",
    )
)


# Get the saved graph state.
snapshot = graph.get_state(config)


# ==========================================
# 3. DISPLAY APPROVAL REQUEST
# ==========================================

if snapshot.next:
    console.print()

    console.print(
        Panel.fit(
            Pretty(snapshot.values["remediation_plan"]),
            title="Remediation Approval Required",
        )
    )

    console.print()

    approval_input = input(
        "Approve this remediation? [y/n]: "
    ).strip().lower()

    approved = approval_input == "y"


    # ==========================================
    # 4. RESUME THE GRAPH
    # ==========================================

    result = graph.invoke(
        Command(
            resume={
                "approved": approved,
            }
        ),
        config=config,
    )


    # ==========================================
    # 5. SHOW FINAL STATE
    # ==========================================

    console.print()

    console.print(
        Panel.fit(
            Pretty(result),
            title="Final Remediation Workflow State",
        )
    )

else:
    console.print(
        "[bold red]The graph did not pause for approval.[/bold red]"
    )