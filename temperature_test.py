from ollama_client import call_ollama

prompt = "Complete this sentence: The weather today is"

print("Testing different temperatures:\n")

for temp in [0.0, 0.5, 1.0, 1.5]:
    print(f"Temperature: {temp}")
    response = call_ollama(
        prompt, 
        temperature=temp, 
        num_predict=20
    )
    print(f"Response: {response}\n")