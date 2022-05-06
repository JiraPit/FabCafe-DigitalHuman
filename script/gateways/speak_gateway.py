import os
import sys
sys.path.append("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import click
import script.util.VoiceProcessingUtil as vpu
import script.util.TextProcessingUtil as tpu

@click.command()
@click.option("--filepath",default="")
@click.option("--text",default=None)
def main(filepath, text):
    os.chdir("C:/Users/pitak/Desktop/DigitalHuman-Speak")
    if (text == None):
        voice = vpu.audio_from_file(filepath)
        text = vpu.speech_to_text(voice)
    processed_text = tpu.text_process(text)
    cluster_ranges = vpu.get_voice_syllables(
                audio_path=filepath,
                from_file=True,
                algorithm="hdbscan",
                to_string=False,
            )
    mapped_ranges = []
    for i in range(len(cluster_ranges)):
        try:
            mapped_ranges.append([processed_text[i],cluster_ranges[i]])
        except:
            click.echo("no i")
    
    click.echo(mapped_ranges)
    return mapped_ranges

if __name__ == "__main__":
    main()