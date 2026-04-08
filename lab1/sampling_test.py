from ollama_client import call_ollama

prompt = "Write a creative opening line for a story:"

print("Testing sampling parameters:\n")

# Test 1: Low top-k (focused)
print("1. Low top-k (focused selection):")
response = call_ollama(
    prompt, 
    temperature=0.8, 
    top_k=10, 
    num_predict=30
)
print(f"{response}\n")

# Test 2: High top-k (diverse)
print("2. High top-k (diverse selection):")
response = call_ollama(
    prompt, 
    temperature=0.8, 
    top_k=50, 
    num_predict=30
)
print(f"{response}\n")

# Test 3: Low top-p (conservative)
print("3. Low top-p (conservative):")
response = call_ollama(
    prompt, 
    temperature=0.8, 
    top_p=0.5, 
    num_predict=30
)
print(f"{response}\n")

# Test 4: High top-p (exploratory)
print("4. High top-p (exploratory):")
response = call_ollama(
    prompt, 
    temperature=0.8, 
    top_p=0.95, 
    num_predict=30
)
print(f"{response}\n")