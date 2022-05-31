from fastapi import FastAPI, UploadFile
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import librosa
import uvicorn

app = FastAPI()
RECOG = sr.Recognizer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/speech_recog")
def speech_recog (file: Union[UploadFile, None] = None):
    # speech_to_text(sr.AudioData())
    data, rate = librosa.load()
    return {"data": file.file}

def speech_to_text(speech : sr.AudioData):
    text = RECOG.recognize_google(speech,language='th')
    return text

if __name__ == "__main__":
    uvicorn.run(app,port=8080)