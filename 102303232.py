
# Install dependencies
!pip -q install yt-dlp pydub
!apt -qq install ffmpeg -y

import os
import subprocess
from pydub import AudioSegment
from google.colab import files

# -----------------------------
# USER INPUT (CHANGE HERE)
# -----------------------------
singer = "Arijit Singh"   # Change singer name
num_videos = 15           # Must be > 10
duration = 30             # Must be > 20 (seconds)
output_file = "mashup.mp3"
# -----------------------------

# Validation
if num_videos <= 10:
    raise ValueError("Number of videos must be greater than 10")

if duration <= 20:
    raise ValueError("Duration must be greater than 20 seconds")

print("Inputs validated successfully ✅")

# Create folders
folders = ["videos", "audios", "trimmed"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# -----------------------------
# Download Videos
# -----------------------------
print("Downloading videos from YouTube...")

query = f"ytsearch{num_videos}:{singer} songs"

command = [
    "yt-dlp",
    "-f", "mp4",
    "--no-playlist",
    "-o", "videos/%(title)s.%(ext)s",
    query
]

subprocess.run(command)

# -----------------------------
#Convert to MP3
# -----------------------------
print("Converting videos to audio...")

for file in os.listdir("videos"):
    if file.lower().endswith(".mp4"):
        video_path = os.path.join("videos", file)
        audio_name = os.path.splitext(file)[0] + ".mp3"
        audio_path = os.path.join("audios", audio_name)

        try:
            audio = AudioSegment.from_file(video_path)
            audio.export(audio_path, format="mp3")
        except Exception as e:
            print(f"Skipping {file}: {e}")

# -----------------------------
#Trim Audio
# -----------------------------
print(f"Trimming first {duration} seconds...")

for file in os.listdir("audios"):
    if file.lower().endswith(".mp3"):
        audio_path = os.path.join("audios", file)
        trimmed_path = os.path.join("trimmed", file)

        try:
            audio = AudioSegment.from_mp3(audio_path)
            trimmed_audio = audio[:duration * 1000]
            trimmed_audio.export(trimmed_path, format="mp3")
        except Exception as e:
            print(f"Skipping {file}: {e}")

# -----------------------------
# Merge Audio
# -----------------------------
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

final_audio.export(output_file, format="mp3")

print("Mashup created successfully 🎉")

# -----------------------------
#  Download Final File
# -----------------------------
files.download(output_file)
