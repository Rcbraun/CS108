import ollama

# Replace with your server URL
client = ollama.Client(host='127.0.0.1:11434')

def test_connection():
    try:
        # List available models
        models = client.list()
        print("🎉 Connected successfully!")
        print("\nAvailable models:")
        for model in models['models']:
            print(f"  - {model['model']}")
        return True
    except Exception as e:
        print(f"✗ Error connecting: {e}")
        return False

if __name__ == "__main__":
    test_connection()