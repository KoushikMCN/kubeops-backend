# Deployment Rollout Status Graph invoke

from graphs.deployment_rollout import build_deployment_rollout_status_graph

from rich.console import Console
from rich.markdown import Markdown

graph = build_deployment_rollout_status_graph()

result = graph.invoke(
    {
        "deployment_name": "nginx-deployment",
        "namespace": "default",
        "deployment": None,
        "rollout_status": None,
        "rollout_message": None
    }
)

# print("================================================================================")
# print(result["diagnosis"])
# print("================================================================================")
print("\n\n\n")
console = Console()
console.print(Markdown(result["diagnosis"]))
print("\n\n\n")