from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
client = OpenAI()
console = Console()

conversation_history = []

while True:
    user_input = input("Ask anything: ")

    if user_input == "exit":
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    full_response = ""

    console.print("\n[bold green]Bot:[/bold green] ", end="")

    with client.responses.stream(
        model="gpt-5-mini",
        instructions="You are a sarcastic assistant who speaks in a sassy manner.",
        input=conversation_history
    ) as stream:

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                full_response += event.delta

    print("\n")

    conversation_history.append({
        "role": "assistant",
        "content": full_response
    })