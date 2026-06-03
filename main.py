import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

from personas import roles, styles

load_dotenv()
client = OpenAI()

console = Console()

conversation_history = []

chat_file = "conversations/chat_history.json"

if os.path.exists(chat_file):
    print("\n1. Load chat")
    print("2. New chat")
    choice = input("Choice: ")
else:
    choice = "2"

if choice == "1":
    with open(chat_file, "r") as file:
        chat_data = json.load(file)
    selected_role = chat_data.get("role", "General Assistant")
    selected_style = chat_data.get("style", "Friendly")
    conversation_history = chat_data.get("messages", [])
    print("Chat loaded successfully.")
else:
    print("\nStarting a new chat...")

if choice == "2":
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

while True:
    user_input = input("\nAsk anything: ")

    if user_input.strip().lower() == "exit":
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

chat_data = {
    "role": selected_role,
    "style": selected_style,
    "messages": conversation_history
}

os.makedirs("conversations", exist_ok=True)

with open(chat_file, "w") as file:
    json.dump(chat_data, file, indent=4)

print(f"Chat history saved to {chat_file}")