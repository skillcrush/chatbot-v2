from openai import OpenAI
import tiktoken
import logging
import datetime

log = logging.getLogger("chatbot_token_count")

logging.basicConfig(filename = "chatbot_token_count.log", level = logging.INFO)

client = OpenAI()

# accepts a preferred model and a list of messages
# makes chat completions API call
# returns the response message content
def get_api_chat_response_message(model, messages):
    # make the API call
    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    # return the response
    return api_response

# extract and return the response text
def get_response_message(response):
    return response.choices[0].message.content

# extract and return the total number of tokens
def get_response_total_tokens(response):
    return response.usage.total_tokens

model = "gpt-3.5-turbo"

encoding = tiktoken.encoding_for_model(model)

token_input_limit = 12289

total_token_count = 0

chat_history = []

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Chatbot: Hello there, I'm your helpful chatbot! Type exit to end our chat. What's your name? ")
    else:
        user_input = input("You: ")
    if user_input.lower() == "exit":
        log.info("\nDate: " + str(datetime.datetime.now()) + "\nTotal tokens: " + str(total_token_count) + "\n\n")
        break
	
    token_count = len(encoding.encode(user_input))
    
    if (token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = get_api_chat_response_message(model, chat_history)
    response_message = get_response_message(response)

    response_total_tokens = get_response_total_tokens(response)
    total_token_count += response_total_tokens

    print("Chatbot: ", response_message)

    chat_history.append({
        "role": "assistant",
        "content": response_message
    })
