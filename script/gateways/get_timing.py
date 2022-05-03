import sys
sys.path.append("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import click
import script.util.VoiceProcessingUtil as vpu

@click.command()
@click.option("--filepath",default="")
def main(filepath):
    cluster_ranges = vpu.get_voice_syllables(
                audio_path=filepath,
                from_file=True,
                algorithm="hdbscan",
                to_string=True,
            )
    click.echo(cluster_ranges)
    return cluster_ranges

if __name__ == "__main__":
    main()