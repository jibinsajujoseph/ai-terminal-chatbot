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
        try:
            chat_data = json.load(file)
            selected_role = chat_data.get("role", "General Assistant")
            selected_style = chat_data.get("style", "Friendly")
            conversation_history = chat_data.get("messages", [])
            print("\nChat loaded successfully. Continue with your chat...")
        except json.JSONDecodeError:
            print("\nChat history is corrupted. Starting a new chat..")
            choice = "2"
else:
    print("\nStarting a new chat...")

if choice == "2":
    print("\nChoose a role:")
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

session_input_tokens = 0
session_output_tokens = 0

def save_chat():
    chat_data = {
        "role": selected_role,
        "style": selected_style,
        "messages": conversation_history
    }

    os.makedirs("conversations", exist_ok=True)

    with open(chat_file, "w") as file:
        json.dump(chat_data, file, indent=4)

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

    try:
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
        response = stream.get_final_response()

        session_input_tokens += response.usage.input_tokens
        session_output_tokens += response.usage.output_tokens

        print(
            f"\nTokens: "
            f"in={response.usage.input_tokens}, "
            f"out={response.usage.output_tokens}, "
            f"session={session_input_tokens + session_output_tokens}"
        )

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        continue

    conversation_history.append({
        "role": "assistant",
        "content": full_response
    })

    save_chat()