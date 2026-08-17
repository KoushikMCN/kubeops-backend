# Cluster Health Graph invoke

from rich.console import Console
from rich.markdown import Markdown

from graphs.cluster_health import build_cluster_health_graph


graph = build_cluster_health_graph()

result = graph.invoke(
    {
        "namespace": "default",
        "deployments": [],
        "pods": [],
        "services": [],
        "events": [],
        "diagnosis": None,
    }
)

console = Console()

console.print("\n\n")
console.print(Markdown(result["diagnosis"]))
console.print("\n\n")