from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Laod AI model
llm = OllamaLLM(model='llama3.2:1b')

# Initialize Memory
Chat_history = ChatMessageHistory()  # stores user-Ai conversation history

# Define Ai chat prompt
prompt = PromptTemplate(
    input_variables=['Chat_history','question'],
    template=( "You are a helpful AI assistant.\n"
        "Here is the conversation so far:\n{Chat_history}\n\n"
        "The user just asked: {question}\n"
        "Keep the amswers simple and direct."
    )
)

# function to run AI chat with memory
def run_chain(question):
    # retrieve chat history manually
    Chat_history_text = "\n".join([f"{msg.type.capitalize()}:{msg.content}" for msg in Chat_history.messages])
    
    # Run AI response generation
    response = llm.invoke(prompt.format(Chat_history=Chat_history_text,question=question))
    
    # Store new user input & AI response in memory
    Chat_history.add_user_message(question)
    Chat_history.add_ai_message(response)
    
    return response

# Interactive CLI chatbot
print("\n AI chatbot with memory")
print("type 'exit' to stop." )

while True:
    user_input = input("\n You:")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    ai_response = run_chain(user_input)
    print(f"\n Ai: {ai_response}")