# Kubernetes Agent Test ( create_agent() from langchain )

from agents.kubernetes_agent import build_kubernetes_agent
from rich.console import Console
from rich.markdown import Markdown

agent = build_kubernetes_agent()

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Create a deployment named crash-demo in the default namespace with one replica using the busybox image. Configure it to run the command [\"false\"].",
                # "content": "Create an nginx deployment with multiple replicas, default namespace, wrong image name to simulate an image pull back off error",
            }
        ]
    }
)

# print("===============================================================================================================")
# print(response["messages"][-1].content[0]["text"])
# print("===============================================================================================================")
print("\n\n\n")
console = Console()
console.print(Markdown(response["messages"][-1].content[0]["text"]))
print("\n\n\n")