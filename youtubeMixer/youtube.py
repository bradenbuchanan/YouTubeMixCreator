from pytube import YouTube
from moviepy.editor import *
import yt_dlp
import subprocess
import re

def download_video(url, output_path):
    print(f"Downloading video from {url}")

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        # Remove special characters and spaces from the title
        sanitized_title = re.sub(r'[^\w\s]', '_', title)
        sanitized_title = re.sub(r'\s', '_', sanitized_title)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': f'{output_path}/{sanitized_title}.%(ext)s',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Video title: {sanitized_title}")
        ydl.download([url])
        print(f"Video downloaded to {output_path}")
        return sanitized_title

# Extract audio from videos
def extract_audio(video_path, output_path2, video_title):
    audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + '.m4a'
    output_path2 = os.path.join('/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output', f"{video_title}.m4a")

    command = f'ffmpeg -i "{video_path}" -vn -codec:a aac -b:a 128k "{output_path2}"'

    subprocess.run(command, shell=True, check=True)

urls = [
    'https://www.youtube.com/watch?v=7810tcWqzcc',
    'https://www.youtube.com/watch?v=tlecTxx335U&ab_channel=ChristianL%C3%B6ffler-Topic',
    'https://www.youtube.com/watch?v=vM0QTlrTpUA&ab_channel=ThisNeverHappened'
    # Add more song URLs here
]

output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output'

sanitized_titles = []

for url in urls:
    video_title = download_video(url, output_path)
    sanitized_titles.append(video_title)
    video_path = os.path.join(output_path, f"{video_title}.mp4")

    extract_audio(video_path, output_path, video_title)


# Mix audio of files
from pydub import AudioSegment

def mix_audios_with_crossfade(audio_paths, output_path, crossfade_duration=5000):
    mix = AudioSegment.from_file(audio_paths[0], format="m4a")
    
    for path in audio_paths[1:]:
        next_audio = AudioSegment.from_file(path, format="m4a")
        mix = mix.append(next_audio, crossfade=crossfade_duration)

    mix.export(output_path, format="mp4")

audio_paths = [os.path.join(output_path, f'{title}.m4a') for title in sanitized_titles]

output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output/mixed_audio.m4a'

# Call the modified function with the desired crossfade duration in milliseconds (e.g., 15000 ms = 15 seconds)
mix_audios_with_crossfade(audio_paths, output_path, crossfade_duration=20000)