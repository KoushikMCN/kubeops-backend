# Invoke supervisor (it chooses btw kubernetes crud and deployment diagnosis workflow)

from supervisors.kubernetes_supervisor import supervisor

from rich.console import Console
from rich.markdown import Markdown

response = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "delete nginx deployment in the default namespace",
            }
        ]
    }
)

print("\n\n\n")
console = Console()
console.print(Markdown(response["messages"][-1].content[0]["text"]))
# print(type(response["messages"][-1].content))
# print(response["messages"][-1].content)
print("\n\n\n")