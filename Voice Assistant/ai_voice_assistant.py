import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Load AI Model
llm = OllamaLLM(model="mistral:7b")  # Change to "llama3" or another Ollama model

# Initialize Memory (LangChain v1.0+)
Chat_history = ChatMessageHistory()

# Initialize Text-to-Speech Engine

# Speech Recognition
recognizer = sr.Recognizer()

# Function to Speak
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)  # Adjust speaking spee]d
    engine.say(text)
    engine.runAndWait()

# Function to Listen
def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"👂 You Said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("🤖 Sorry, I couldn't understand. Try again!")
        return ""
    except sr.RequestError:
        print("⚠️ Speech Recognition Service Unavailable")
        return ""

# AI Chat Prompt
display_prompt = PromptTemplate(
    input_variables=['Chat_history','question'],
    template=( "You are a helpful AI assistant.\n"
        "Here is the conversation so far:\n{Chat_history}\n\n"
        "The user just asked: {question}\n"
    )
)
# AI Chat Prompt
speak_prompt = PromptTemplate(
    input_variables=['Chat_history','question'],
    template=( "You are a helpful AI assistant.\n"
        "Here is the conversation so far:\n{Chat_history}\n\n"
        "The user just asked: {question}\n"
    )
)

# Function to Process AI Responses
def run_chain(question,Chat_history,prompt):
    Chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in Chat_history.messages])

    response = llm.invoke(prompt.format(Chat_history=Chat_history_text, question=question))

    # Ensure response is string
    if hasattr(response, "content"):
        response_text = response.content
    else:
        response_text = str(response)

    Chat_history.add_user_message(question)
    Chat_history.add_ai_message(response_text)

    return response_text


# Main Loop
speak("Hello! I am your AI Assistant. How can I help you today?")
displayChain = ChatMessageHistory()
speakChain = ChatMessageHistory()


while True:
    query = listen()
    if "exit" in query or "stop" in query:
        speak("Goodbye! Have a great day.")
        break
    if query:
        response = run_chain(query,displayChain,display_prompt)
        print(f"\n🤖 AI Response: {response}")
    
    # response = llm.invoke(prompt.format(Chat_history=Chat_histo/ry_text, question=question))
        to_speak = llm.invoke("Summarize and reduce the length of this Ai agent response for audio conversation. Make sure it represents all nuances and not too long for listening, as in audio explanation\n" + response)
        # Ensure response is string
        if hasattr(to_speak, "content"):
            to_speak = to_speak.content
        else:
            to_speak = str(to_speak)
        print(f"\n🤖 AI Response: {to_speak}")
        speak(to_speak)
