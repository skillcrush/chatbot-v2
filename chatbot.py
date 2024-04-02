from openai import OpenAI
import tiktoken

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

    # extract the response text
    response_content = api_response.choices[0].message.content

    # return the response text
    return response_content

model = "gpt-3.5-turbo"

encoding = tiktoken.encoding_for_model(model)

# print the encoding variable
# print(encoding)

token_input_limit = 12289

chat_history = []

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Chatbot: Hello there, I'm your helpful chatbot! Type exit to end our chat. What's your name? ")
    else:
        user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    # encode the user input
    # user_input_encoded = encoding.encode(user_input)
    # print the encoded user input
    # print(user_input_encoded)
    
    # update the token_count to be the length of the user input
    token_count = len(encoding.encode(user_input))
    # print the token_count
    # print(token_count)
    
    if (token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = get_api_chat_response_message(model, chat_history)

    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": response
    })
