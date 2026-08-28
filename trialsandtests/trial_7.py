from rich.console import Console
from rich.markdown import Markdown

from supervisors.kubernetes_supervisor import supervisor


response = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Investigate why my nginx-service is not working and find the underlying cause.",
            }
        ]
    }
)

console = Console()

final_message = response["messages"][-1].content[0]['text']

console.print("\n")
console.print(Markdown(final_message))
console.print("\n")