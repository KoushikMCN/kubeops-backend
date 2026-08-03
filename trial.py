from agents.kubernetes_agent import build_kubernetes_agent
from rich.console import Console
from rich.markdown import Markdown

agent = build_kubernetes_agent()

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "delete the api-config in default namespace",
            }
        ]
    }
)

print("===============================================================================================================")
print(response["messages"][-1].content[0]["text"])
print("===============================================================================================================")
console = Console()
console.print(Markdown(response["messages"][-1].content[0]["text"]))