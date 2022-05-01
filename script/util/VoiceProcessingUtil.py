import speech_recognition as sr
import os
os.chdir("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
import speech_recognition as sr
import librosa
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.cluster import KMeans

MIC = sr.Microphone(1)
RECOG = sr.Recognizer()
AUDIO_MIC_PATH = "data/mic_audio.wav"
AUDIO_RESULT_PATH = "data/result_audio.wav"

def get_voice_syllables(
    audio_path : str or None = None,
    from_mic : bool or None = False,
    from_file : bool or None = False):
    if(from_file and audio_path == None):
        print("ERROR: No audio path specified")
        return
    if(from_mic):
        speech = audio_from_mic()
    elif(from_file):
        speech = audio_from_file(audio_path=audio_path)
    else:
        print("ERROR: No source specified")
        return
    text = speech_to_text(speech=speech)
    data,rate = load_audio_data(
                    audio_path= audio_path if from_file else AUDIO_MIC_PATH
                )
    clustered_data, label = kmeans_train(data=data,text=text)
    cluster_times = cluster_frame_data(clustered_data=clustered_data,label=label)
    plot_cluster(clustered_data=clustered_data,label=label)
    plot_wave_segmentation(
        cluster_times=cluster_times,
        rate=rate,
        audio_path=audio_path if from_file else AUDIO_MIC_PATH)
    return cluster_times


##---------------------------------------------------------------------------------------

def audio_from_mic():
    with MIC as source:
        speech = RECOG.listen(source)
        with open(AUDIO_MIC_PATH, "wb") as file:
            file.write(speech.get_wav_data())
        return speech

def audio_from_file(audio_path):
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        speech = RECOG.listen(source)
        return speech

#---------------------------------------------------------------------------------------

def speech_to_text(speech : sr.AudioData):
    text = RECOG.recognize_google(speech,language='th')
    print(text)
    return text

def load_audio_data(audio_path : str):
    data, rate = librosa.load(audio_path, sr=1000)
    newdata = abs(data)
    cluster_data = []
    for i in range(len(newdata)):
        if newdata[i] > 0.05:
            cluster_data.append([i,newdata[i]])
    cluster_data = np.array(cluster_data)
    return cluster_data, int(rate)

def kmeans_train(data, text : str):
    k = len(tpu.get_text_syllables(text=text))
    model = KMeans(
        n_clusters=k, 
        n_init=20,
        max_iter=6900,
        random_state=690,
    )
    label = model.fit_predict(data)
    return data, label

def cluster_frame_data(clustered_data,label):
    u_labels = np.unique(label)
    cluster_times = []
    for i in u_labels:
        cluster_times.append([int(clustered_data[label == i , 0].min()),int(clustered_data[label == i , 0].max())])
    return sorted(cluster_times)
    
def plot_cluster(clustered_data,label):
    u_labels = np.unique(label)
    plt.figure(figsize=(50,20))
    for i in u_labels:
        plt.scatter(clustered_data[label == i , 0] , clustered_data[label == i , 1] , label = i)
    plt.legend()
    plt.show()
    plt.savefig("cluster.png")

def plot_wave_segmentation(cluster_times,rate,audio_path):
    eva_rate, evawav = wav.read(audio_path)
    plt.figure(figsize=(30,8))
    plt.plot(evawav,zorder=1)
    plt.vlines(
        list(map(lambda e: int(e[0]*(eva_rate/rate)),cluster_times)),
        ymin=30000,
        ymax=-30000,
        colors="r",
        zorder=1)
    plt.show()
    plt.savefig("wave_segmentation.png")

def save_audio_data(cluster_times,rate,audio_path):
    eva_rate,evawav = wav.read(audio_path)
    c = cluster_times[0]
    e = cluster_times[14]
    wav.write(AUDIO_RESULT_PATH,eva_rate,evawav[c[0]*int(eva_rate/rate):e[1]*int(eva_rate/rate)])