import requests

def lemmatize(text):
    url = "https://zerbitzuak.hitz.eus/api/lemma_private"
    headers = {
        "accept": "application/json",
        "apikey": "5OEBMAp0+tS9vJSGZPqyfK0PtFtztkec",
        "Content-Type": "application/json"
    }
    data = {"text": text}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an exception for 4xx/5xx responses
        result = response.json()
        print(result)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")

with open('testtext.txt', 'r') as f:
    lemmatize(f.read())