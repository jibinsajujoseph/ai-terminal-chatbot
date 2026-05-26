from openai import OpenAI
from dotenv import load_dotenv
from rich.panel import Panel
from rich.console import Console

load_dotenv()

client = OpenAI()

console = Console()

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break

    response = client.responses.create(
        model="gpt-5-mini",
        input=user_input
    )

    console.print(
    Panel(
        response.output_text,
        title="Bot"
    )
)
    