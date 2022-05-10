import requests
URL = "https://voice.botnoi.ai/api/service/generate_audio"

def botnoi(text : str):
    payload = {"text":text, "speaker":"5", "volume":5, "speed":1, "type_media":"wav"}
    headers = {
        'Botnoi-Token': '888e8f47223f1b32655de381fe38a29a8b2355bc8e30a246f0a4b61bf8dd70f8',
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", URL, headers=headers, json=payload)
    doc = requests.get(str(response.json()["audio_url"]))
    with open('data/botnoi.wav', 'wb') as f:
        f.write(doc.content)

    return str(response.json()["audio_url"])
    


