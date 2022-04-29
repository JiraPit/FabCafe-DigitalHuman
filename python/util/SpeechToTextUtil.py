import pyaudio
import speech_recognition as sr
mic = sr.Microphone(1)
recog = sr.Recognizer()
text =""
with mic as source:
    speech = recog.listen(source)
    text = recog.recognize_google(speech,language='th')
print(text)