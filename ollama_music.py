import requests

OLLAMA_HOST = 'http://localhost:11434'  # Adjust if your Ollama server is running elsewhere
MODEL = 'gemma3:4b'

def query_ollama(prompt):
    url = f"{OLLAMA_HOST}/api/chat"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    prompt = (
        "Hey there! As someone who absolutely adores classical music, I’d love "
        "to know your take on the top 10 greatest classical composers of all time. "
        "Could you please list them out with a little note on why they stand out? 🎶"
    )

    result = query_ollama(prompt)

    print("Response from Ollama (gemma3:4b):\n")
    for message in result.get('messages', []):
        print(message['content'])

if __name__ == "__main__":
    main()


