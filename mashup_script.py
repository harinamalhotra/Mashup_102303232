import os
import sys
import subprocess
from pydub import AudioSegment


# ---------------------------------
# Create Required Folders
# ---------------------------------
def create_folders():
    folders = ["audios", "trimmed"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


# ---------------------------------
# Download Audio Directly (MP3)
# ---------------------------------
def download_videos(singer, count):
    print("Downloading audio from YouTube...")

    query = f"ytsearch{count}:{singer} songs"

    command = [
        sys.executable, "-m", "yt_dlp",
        "-x",                          # Extract audio only
        "--audio-format", "mp3",       # Convert to mp3 directly
        "--no-playlist",
        "-o", "audios/%(title)s.%(ext)s",
        query
    ]

    subprocess.run(command, check=True)


# ---------------------------------
# Trim Audio Files
# ---------------------------------
def trim_audio_files(seconds):
    print(f"Trimming first {seconds} seconds...")

    for file in os.listdir("audios"):
        if file.lower().endswith(".mp3"):
            audio_path = os.path.join("audios", file)
            trimmed_path = os.path.join("trimmed", file)

            try:
                audio = AudioSegment.from_mp3(audio_path)
                trimmed_audio = audio[:seconds * 1000]
                trimmed_audio.export(trimmed_path, format="mp3")
            except Exception as e:
                print(f"Skipping {file}: {e}")


# ---------------------------------
# Merge All Trimmed Audio
# ---------------------------------
def merge_audios(output_file):
    print("Merging audio files...")

    final_audio = AudioSegment.empty()

    for file in sorted(os.listdir("trimmed")):
        if file.lower().endswith(".mp3"):
            audio_path = os.path.join("trimmed", file)
            try:
                audio = AudioSegment.from_mp3(audio_path)
                final_audio += audio
            except Exception as e:
                print(f"Skipping {file}: {e}")

    if len(final_audio) == 0:
        raise Exception("Final mashup is empty! No valid audio found.")

    final_audio.export(output_file, format="mp3")


# ---------------------------------
# Main Function Called by Flask
# ---------------------------------
def create_mashup(singer, num_videos, duration, output_file):

    if num_videos <= 10:
        raise ValueError("Number of videos must be greater than 10")

    if duration <= 20:
        raise ValueError("Duration must be greater than 20 seconds")

    print("Inputs validated successfully ✅")

    create_folders()
    download_videos(singer, num_videos)
    trim_audio_files(duration)
    merge_audios(output_file)

    print("Mashup created successfully 🎉")

