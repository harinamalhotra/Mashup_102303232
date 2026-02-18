import subprocess
import os
from pydub import AudioSegment


def create_mashup(singer, num_videos, duration, output_file):

    # Validation
    if num_videos <= 10:
        raise ValueError("Number of videos must be greater than 10")

    if duration <= 20:
        raise ValueError("Duration must be greater than 20 seconds")

    # Create required folders safely
    folders = ["videos", "audios", "trimmed"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    print("Downloading videos...")

    query = f"ytsearch{num_videos}:{singer} songs"

    download_command = [
        "yt-dlp",
        "--no-playlist",
        "-f", "mp4",
        "-o", "videos/%(title)s.%(ext)s",
        query
    ]

    download_result = subprocess.run(download_command, capture_output=True)

    if download_result.returncode != 0:
        print("Download failed. Continuing with existing files...")

    print("Converting videos to mp3...")

    # Convert MP4 → MP3
    for file in os.listdir("videos"):
        if file.lower().endswith(".mp4"):
            video_path = os.path.join("videos", file)
            audio_name = os.path.splitext(file)[0] + ".mp3"
            audio_path = os.path.join("audios", audio_name)

            try:
                audio = AudioSegment.from_file(video_path)
                audio.export(audio_path, format="mp3")
            except Exception as e:
                print(f"Error converting {file}: {e}")

    print("Trimming audio...")

    # Trim audio to given duration
    for file in os.listdir("audios"):
        if file.lower().endswith(".mp3"):
            audio_path = os.path.join("audios", file)
            trimmed_path = os.path.join("trimmed", file)

            try:
                audio = AudioSegment.from_mp3(audio_path)
                trimmed_audio = audio[:duration * 1000]
                trimmed_audio.export(trimmed_path, format="mp3")
            except Exception as e:
                print(f"Error trimming {file}: {e}")

    print("Merging audio...")

    final_audio = AudioSegment.empty()

    # Merge all trimmed files
    for file in sorted(os.listdir("trimmed")):
        if file.lower().endswith(".mp3"):
            audio_path = os.path.join("trimmed", file)
            try:
                audio = AudioSegment.from_mp3(audio_path)
                final_audio += audio
            except Exception as e:
                print(f"Error merging {file}: {e}")

    final_audio.export(output_file, format="mp3")

    print("Mashup created successfully!")
