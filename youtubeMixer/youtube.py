from pytube import YouTube
from moviepy.editor import *
import yt_dlp
import subprocess



# Download videos
def download_video(url, output_path):
    print(f"Downloading video from {url}")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Video title: {info['title']}")
        ydl.download([url])
        print(f"Video downloaded to {output_path}")

urls = [
    'https://www.youtube.com/watch?v=7810tcWqzcc',
    'https://www.youtube.com/watch?v=CARHyGAsv6Y',
]

output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output'

for url in urls:
    download_video(url, output_path)


# Extract audio from videos
def extract_audio(video_path, output_path2):
    audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
    output_audio_path = os.path.join(output_path2, audio_file_name)
    command = f'ffmpeg -i "{video_path}" -codec:a libmp3lame -qscale:a 2 "{output_audio_path}"'
    subprocess.run(command, shell=True, check=True)

video_paths = [
    os.path.join(output_path, 'Lane 8 - Brightest Lights feat POLIÇA.mp4'),
    os.path.join(output_path, 'Lane 8 - Woman.mp4')
] # Replace these with the paths to your downloaded videos

output_path2 = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output'

for video_path in video_paths:
    audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
    extract_audio(video_path, os.path.join(output_path2, audio_file_name))

# Mix audio of files
from pydub import AudioSegment

def mix_audios(audio_paths, output_path):
    mix = AudioSegment.empty()
    for path in audio_paths:
        audio = AudioSegment.from_mp3(path)
        mix += audio
    mix.export(output_path, format="mp3", codec="libmp3lame")

audio_paths = audio_paths = [
    os.path.join(output_path2, 'Lane 8 - Woman.mp3'),
    os.path.join(output_path2, 'Lane 8 - Brightest Lights feat POLIÇA.mp3')
] # Replace these with the paths to your extracted audio files

output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output/mixed_audio.mp3'

mix_audios(audio_paths, output_path)

