from graphs.deployment_diagnosis import build_deployment_diagnosis_graph

from rich.console import Console
from rich.markdown import Markdown

graph = build_deployment_diagnosis_graph()

result = graph.invoke(
    {
        "deployment_name": "crash-demo",
        "namespace": "default",
        "deployment": None,
        "pods": [],
        "pod_events": {},
        "pod_logs": {},
        "diagnosis": "",
    }
)

# print("================================================================================")
# print(result["diagnosis"])
# print("================================================================================")
print("\n\n\n")
console = Console()
console.print(Markdown(result["diagnosis"]))
print("\n\n\n")