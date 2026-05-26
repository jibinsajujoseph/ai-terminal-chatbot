from openai import OpenAI
from dotenv import load_dotenv
from rich.panel import Panel
from rich.console import Console

load_dotenv()

client = OpenAI()

console = Console()

messages = []

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.responses.create(
        model="gpt-5-mini",
        input=messages
    )

    console.print(
    Panel(
        response.output_text,
        title="Bot"
        )
    )
    
    messages.append({
        "role": "assistant",
        "content": response.output_text
    })