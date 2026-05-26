from openai import OpenAI
from dotenv import load_dotenv
from rich.panel import Panel
from rich.console import Console

load_dotenv()

client = OpenAI()

console = Console()

messages = []

while True:
    user_input = input("Ask anything: ")

    if user_input == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    full_response = ""

    console.print("\n[bold green]Bot:[/bold green] ", end="")

    with client.responses.stream(
        model="gpt-5-mini",
        input=messages
    ) as stream:

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                full_response += event.delta

    print("\n")

    messages.append({
        "role": "assistant",
        "content": full_response
    })