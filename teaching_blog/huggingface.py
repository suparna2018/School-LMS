import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def chat_with_bot():
    print("Start chatting with the bot (type 'quit' to stop)!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = query({"inputs": user_input})
        bot_response = response[0]['generated_text']
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    chat_with_bot()
