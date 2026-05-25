from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break

    response = client.responses.create(
        model="gpt-5-mini",
        input=user_input
    )

    print("Bot: ", response.output_text)
    