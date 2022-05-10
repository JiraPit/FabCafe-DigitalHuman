import os
import sys
import pandas as pd
sys.path.append("D:\Data\Jira02\Assets\Python\DigitalHuman-Speak")
os.chdir("D:\Data\Jira02\Assets\Python\DigitalHuman-Speak")
import click
import script.util.VoiceProcessingUtil as vpu
import script.util.TextProcessingUtil as tpu
import script.util.BotnoiUtil as bnu

@click.command()
@click.option("--filepath",default="")
@click.option("--text",default="")
@click.option("--amp_filter",default=0.00)
@click.option("--gen_plot",default="n")
@click.option("--min_sample",default=150)
def run(filepath, text, amp_filter,gen_plot,min_sample):
    if (text == ""):
        voice = vpu.audio_from_file(filepath)
        text = vpu.speech_to_text(voice)
    else:
        text = str(text).replace("_"," ")
        voice = bnu.botnoi(text=text)
        filepath = "data/botnoi.wav"
    processed_text = tpu.text_process(text)
    cluster_ranges = vpu.get_voice_syllables(
                audio_path=filepath,
                from_file=True,
                algorithm="hdbscan",
                to_string=False,
                gen_plot = True if(gen_plot == "y") else False,
                min_cluster_size=min_sample,
                amp_filter= amp_filter
            )
    df = pd.DataFrame(columns=["start","end","init","vowel","final"])
    for i in range(len(cluster_ranges)):
        try:
            df = df.append({
                "start":cluster_ranges[i][0],
                "end":cluster_ranges[i][1],
                "init":processed_text[i]["init"],
                "vowel":processed_text[i]["vowel"],
                "final":processed_text[i]["final"]}, 
                ignore_index=True)
        except:
            continue
    df.to_csv("data/data_out.csv",encoding="utf-8")
    click.echo("data/data_out.csv")
    return

if __name__ == "__main__":
    run()