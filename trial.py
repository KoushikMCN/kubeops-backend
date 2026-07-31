from agents.kubernetes_agent import build_kubernetes_agent
from rich.console import Console
from rich.markdown import Markdown

agent = build_kubernetes_agent()

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "there must be an nginx deployment in default namespace. scale it to 5 replicas",
            }
        ]
    }
)

# print(response["messages"][-1].content[0]["text"])
console = Console()
console.print(Markdown(response["messages"][-1].content[0]["text"]))