# A Simple use case to use ChatGPT OpenAPI to provide responses to questions based on a local text based learning set
# Provide options to use responses from a local text file or use ChatGPT
# Use Smart Mode to use local text file as training data model and save smart answers from ChatGPT into a different file
# Hope this helps a newbie interested to explore and learn

import openai

def load_chat_history(file_path):
    chat_history = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            question = lines[i].strip()
            answer = lines[i + 1].strip()
            chat_history.append({'question': question, 'answer': answer})
    return chat_history

def save_chat_history(file_path, chat_history):
    with open(file_path, 'w') as file:
        for chat in chat_history:
            file.write(chat['question'] + '\n')
            file.write(chat['answer'] + '\n')

def search_chat_history(question, chat_history):
    for chat in chat_history:
        if chat['question'].lower() == question.lower():
            return chat['answer']
    return None


def format_chat_history(chat_history):
    formatted_history = ''
    for chat in chat_history:
        formatted_history += 'Q: ' + chat['question'] + '\n'
        formatted_history += 'A: ' + chat['answer'] + '\n\n'
    return formatted_history

def print_chat_history(chat_history):
    for chat in chat_history:
        print("Question: ", chat['question'])
        print("Answer:   ", chat['answer'])
    return None

def train_chatgpt(qa_pairs):
    # Set up your OpenAI API credentials
    api_key =  'YOUR KEY'
    #replace YOUR KEY with your API key
    openai.api_key = api_key

    # Prepare the training data
    training_data = ""
    for pair in qa_pairs:
        training_data += f"Q: {pair['question']}\nA: {pair['answer']}\n\n"
    try:
        # Fine-tune the base model
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and provide simple insights based on your trained learning model."},
            {"role": "user", "content": training_data}
        ],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.0
    )

        print("ChatGPT training complete: ", response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        # Handles API-specific exceptions
        print("Error String", e)
        error_message = f"OpenAI API Error: {str(e)}"
        return error_message

    except Exception as e:
        # Handles generic exceptions
        error_message = f"An error occurred: {str(e)}"
        return error_message

def query_chatgpt(question,chatmode='normal'):
    
    # Set up your OpenAI API credentials
    api_key =  'YOUR KEY'
    openai.api_key = api_key
    #replace YOUR KEY with your API key
    # Set the model and parameters
    model = 'gpt-3.5-turbo'
    
    try:
        if chatmode != 'smart':
            print("Normal Mode Query")
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
                    ]
            # Generate a response from ChatGPT
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=50,
            )
        else:
            print("Smart Mode Query")
            messages=[
                {"role": "system", "content": "You are a helpful assistant and provide simple insights based on your trained learning model."},
                {"role": "user", "content": question}
                    ]
            # Generate a response from ChatGPT
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.0
            )

        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        # Handles API-specific exceptions
        print("Error String", e)
        error_message = f"OpenAI API Error: {str(e)}"
        return error_message

    except Exception as e:
        # Handles generic exceptions
        error_message = f"An error occurred: {str(e)}"
        return error_message



# Example usage
file_path = 'chat_history.txt'
chat_history = load_chat_history(file_path)
smart_file_path = 'smart_chat_history.txt'
smart_chat_history = load_chat_history(smart_file_path)

while True:
    user_question = input("Ask a question (or type 'smart' for Smart Mode or 'quit' to exit): ")

    if user_question.lower() == 'quit':
        break
    if user_question.lower() != 'smart':
        answer = search_chat_history(user_question, chat_history)
        if answer:    
            print("Answer:", answer)
        else:
            print("Question not found")
            answer = input("Would you like to ask ChatGPT for an answer? (or type 'no' to move on): ")
            if answer.lower() != 'no':
                answer = query_chatgpt(user_question)
                if answer.startswith("OpenAI API Error") or answer.startswith("An error occurred"):
                    print(answer)
                    break
                else:
                    print(answer)
                    chat_history.append({'question': user_question, 'answer': answer})


        #Update the chat history file
        save_chat_history(file_path, chat_history)
        
    else:
        print("Smart Mode: ChatGPT gets trained based on local question answer data set and provides smart answer")
        answer = train_chatgpt(chat_history)
        if answer.startswith("OpenAI API Error") or answer.startswith("An error occurred"):
            print(answer)
            break
        user_question = input("Smart Mode: Ask a question (or 'quit' to exit): ")
        if user_question.lower() == 'quit':
            break
        else:
            answer = query_chatgpt(user_question,'smart')
            if answer.startswith("OpenAI API Error") or answer.startswith("An error occurred"):
                print(answer)
                break
            else:
                print(answer)
                smart_chat_history.append({'question': user_question, 'answer': answer})
            print("End of Smart Mode")
        #Update the smart chat history file
        save_chat_history(smart_file_path, smart_chat_history)
        
    print()   
    print_chat_history(chat_history)
    print()
    print_chat_history(smart_chat_history)
    print()
    print("Love the interaction?")
    print()

print("End of program")
    
