from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from personas import roles, styles
import os
import json

load_dotenv()
client = OpenAI()

console = Console()

print("Choose a role:")
for key, value in roles.items():
    print(f"{key}. {value}")

role_choice = input("Role: ")

print("\nChoose a style:")
for key, value in styles.items():
    print(f"{key}. {value}")

style_choice = input("Style: ")

selected_role = roles.get(role_choice, "General Assistant")
selected_style = styles.get(style_choice, "Friendly")

instructions = f"""
You are a {selected_role}.
Your communication style is {selected_style}.
"""

conversation_history = []

while True:
    user_input = input("\nAsk anything: ")

    if user_input == "exit":
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    full_response = ""

    console.print(f"\n[bold green]{selected_role}:[/bold green] ", end="")

    with client.responses.stream(
        model="gpt-5-mini",
        instructions=instructions,
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

os.makedirs("conversations", exist_ok=True)

with open("conversations/chat_history.json", "w") as file:
    json.dump(conversation_history, file, indent=4)