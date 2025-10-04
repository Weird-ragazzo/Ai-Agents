from langchain_ollama import OllamaLLM
llm = OllamaLLM(model='llama3.2:1b')
print("\n Welcome! State your Query.")
while True:
    Q = input("Question(or 'exit' to stop): ")
    if Q.lower() == 'exit':
        print('Goodbye!')
        break
    R = llm.invoke(Q)
    print("\nResponse:",R)
    