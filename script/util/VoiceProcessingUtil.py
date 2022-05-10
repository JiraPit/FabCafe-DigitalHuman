import sys
sys.path.append("E:\Data\Jira02\Assets\Python\DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
import speech_recognition as sr
import librosa
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.cluster import KMeans
from hdbscan import HDBSCAN

MIC = sr.Microphone(1)
RECOG = sr.Recognizer()
AUDIO_MIC_PATH = "data/mic_audio.wav"
AUDIO_RESULT_PATH = "data/result_audio.wav"

def get_voice_syllables(
    audio_path : str or None = None,
    from_mic : bool or None = False,
    from_file : bool or None = False,
    algorithm : str or None = "hdbscan",
    gen_voice : bool or None = False,
    gen_voice_start : int or None = 0,
    gen_voice_end : int or None = 0,
    gen_plot : bool or None = False,
    to_string : bool or None = False,
    amp_filter : float or None = 0,
    min_cluster_size : int or None = 50,
    ):
    #-verifying
    if(from_file and audio_path == None):
        return print("ERROR: No audio path specified")
    if(algorithm not in ["hdbscan","kmeans"]):
        return print("ERROR: unknown algorithm")
    #-algorithm 1
    if(amp_filter<=0):
        if(algorithm == "kmeans"):
            rate = 1000
            amp_threshold=0.04
        elif(algorithm == "hdbscan"):
            rate = 44100
            amp_threshold=0.1
    else:
        if(algorithm == "kmeans"):
            rate = 1000
            amp_threshold=amp_filter
        elif(algorithm == "hdbscan"):
            rate = 44100
            amp_threshold=amp_filter

    #-init data from source
    if(from_mic):
        speech = audio_from_mic()
    elif(from_file):
        speech = audio_from_file(audio_path=audio_path)
    else:
        return print("ERROR: No source specified")
    #-get text from speech
    if algorithm == "kmeans":
        text = speech_to_text(speech=speech)
    #-load and pre-process
    data,rate = load_audio_data(
                    audio_path= audio_path if from_file else AUDIO_MIC_PATH,
                    rate=rate,
                    amp_threshold=amp_threshold,
                )
    #-algorithm 2
    if(algorithm == "kmeans"):
        clustered_data, label = kmeans_train(data=data,text=text)
    elif(algorithm == "hdbscan"):
        clustered_data, label = hdbscan_train(data=data,min_cluster_size=min_cluster_size)
    cluster_ranges = get_cluster_frame(clustered_data=clustered_data,label=label)
    #-plot
    if (gen_plot):
        plot_cluster(clustered_data=clustered_data,label=label)
        plot_wave_segmentation(
            cluster_times=cluster_ranges,
            rate=rate,
            audio_path=audio_path if from_file else AUDIO_MIC_PATH)
    #-generate sub-voice
    if(gen_voice):
        save_audio_data(
            cluster_ranges=cluster_ranges,
            audio_path=audio_path if from_file else AUDIO_MIC_PATH,
            rate=rate,
            start=gen_voice_start,
            end=gen_voice_end)
    cluster_S_ranges = frame_to_second(
        cluster_ranges=cluster_ranges,
        audio_path=audio_path if from_file else AUDIO_MIC_PATH,
        rate=rate
        )
    if (to_string):
        return clusters_to_string(cluster_S_ranges=cluster_S_ranges)
    else:
        return cluster_S_ranges

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
    return text

def load_audio_data(audio_path : str, rate : int, amp_threshold : int):
    data, rate = librosa.load(audio_path, sr=rate)
    newdata = abs(data)
    cluster_data = []
    for i in range(len(newdata)):
        if newdata[i] > amp_threshold:
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

def hdbscan_train(data,min_cluster_size):
    model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=None,
        algorithm="best")
    label = model.fit_predict(data)
    return data, label

def get_cluster_frame(clustered_data,label):
    u_labels = np.unique(label)
    u_labels = np.delete(u_labels,np.where(u_labels==-1))
    cluster_ranges = []
    for i in u_labels:
        cluster_ranges.append([int(clustered_data[label == i , 0].min()),int(clustered_data[label == i , 0].max())])
    return sorted(cluster_ranges)

def get_cluster_frame(clustered_data,label):
    u_labels = np.unique(label)
    u_labels = np.delete(u_labels,np.where(u_labels==-1))
    cluster_ranges = []
    for i in u_labels:
        cluster_ranges.append([int(clustered_data[label == i , 0].min()),int(clustered_data[label == i , 0].max())])
    return sorted(cluster_ranges)

def frame_to_second(cluster_ranges,audio_path,rate):
    cluster_ranges = list(map(lambda x: [x[0]/rate,x[1]/rate],cluster_ranges))
    return cluster_ranges

def clusters_to_string(cluster_S_ranges):
    result = ""
    for S_range in cluster_S_ranges:
        for S in S_range:
            result += str(S)
            result += ","
        result += "/"
    result = result.replace(",/","/")
    return result
#--------------------------------------------------------------------------------------------------   
def plot_cluster(clustered_data,label):
    u_labels = np.unique(label)
    u_labels = np.delete(u_labels,np.where(u_labels==-1))
    plt.figure(figsize=(50,20))
    for i in u_labels:
        plt.scatter(clustered_data[label == i , 0] , clustered_data[label == i , 1] , label = i)
    plt.legend()
    plt.savefig("cluster.png")
    plt.show()

def plot_wave_segmentation(cluster_times,rate,audio_path):
    eva_rate, evawav = wav.read(audio_path)
    plt.figure(figsize=(30,8))
    plt.plot(evawav,zorder=2)
    plt.vlines(
        list(map(lambda e: int(e[0]*(eva_rate/rate)),cluster_times)),
        ymin=35000,
        ymax=-35000,
        colors="r",
        zorder=3)
    for e in cluster_times:
        plt.axvspan(e[0]*(eva_rate/rate),e[1]*(eva_rate/rate),color="lightgray",zorder=1)
    plt.savefig("wave_segmentation.png")
    plt.show()
    

#----------------------------------------------------------------------------------------------------
def save_audio_data(cluster_ranges,rate,audio_path,start : int, end : str):
    eva_rate,evawav = wav.read(audio_path)
    silence,silence_rate = librosa.load("data/Test/silence.wav", sr=eva_rate)
    c = cluster_ranges[start]
    e = cluster_ranges[end]
    dataToWrite = np.concatenate((silence,evawav[c[0]*int(eva_rate/rate):(e[1]*int(eva_rate/rate))],silence))
    wav.write(AUDIO_RESULT_PATH,eva_rate,dataToWrite)