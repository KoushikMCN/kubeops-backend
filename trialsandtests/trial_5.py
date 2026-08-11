# Service Connectivity Diagnosis Graph invoke

from rich.console import Console
from rich.markdown import Markdown

from graphs.service_connectivity import (
    build_service_connectivity_graph,
)

graph = build_service_connectivity_graph()

result = graph.invoke(
    {
        "service_name": "nginx-service",
        "namespace": "default",
        "service": None,
        "endpoints": [],
        "pods": [],
        "diagnosis": None,
        "error": None,
    }
)

console = Console()
console.print(Markdown(result["diagnosis"]))