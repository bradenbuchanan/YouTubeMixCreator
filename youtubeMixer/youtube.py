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
    'https://www.youtube.com/watch?v=QyGpkd477-Y', #Only you
    'https://www.youtube.com/watch?v=j95-HloCj_o', #do you feel the same?
    'https://www.youtube.com/watch?v=opXR8laenl8', #ocula - clear (extended mix)
    'https://www.youtube.com/watch?v=-1Q-Ple93D4', #on the run - ocula
    'https://www.youtube.com/watch?v=r4qI_2ZA8Gc', #not alone - ocula remix
    'https://www.youtube.com/watch?v=MvKgfk2XToo', #feel around you ocula remix
    'https://www.youtube.com/watch?v=3aSVdptdcSU', #come around - ocula
    'https://www.youtube.com/watch?v=94QDU3leasg', #waves - ocula remix
    'https://www.youtube.com/watch?v=8GtiWHNbL14', #try me ocula
    'https://www.youtube.com/watch?v=26y8g7KQaTs', #be there - ocula
    'https://www.youtube.com/watch?v=V0uyIMevop8', #green willow - ocula
    'https://www.youtube.com/watch?v=qDgvrEZR5_0', #closer to the edge
    'https://www.youtube.com/watch?v=udqh_P0q2-Y', #empirical ocula
    'https://www.youtube.com/watch?v=ZYk0ayxtGSI', #one more time - ocula remix
    'https://www.youtube.com/watch?v=oxc0dRbdgzw', #rise - ocula
    'https://www.youtube.com/watch?v=ilHCTOZFNEQ', #tephra ocula
    'https://www.youtube.com/watch?v=IvLy3C0iPig', #years on end - extended mix
    'https://www.youtube.com/watch?v=0rG3R58kQ98', #home away from home
    'https://www.youtube.com/watch?v=CvxbSokNsJA', #no logic
    'https://www.youtube.com/watch?v=Eadahopy8Vs', #no borders
    'https://www.youtube.com/watch?v=MFLYELJLhR0', #the last turn
    'https://www.youtube.com/watch?v=lx83eZV7oIg', #what remains
    'https://www.youtube.com/watch?v=m_UWBJVlQ7M', #renaissance
    'https://www.youtube.com/watch?v=HYobBsfcpR4', #summit
    'https://www.youtube.com/watch?v=7gJl-BxyO0I', #if only (you could be here)
  ]

#Write time stamps
def write_timestamps_to_file(sanitized_titles, timestamps, output_path):
    with open(output_path, 'w') as f:
        for title, timestamp in zip(sanitized_titles, timestamps):
            f.write(f"Title: {title}, Start Time: {timestamp / 1000.0} seconds\n")
 

output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output'

sanitized_titles = []

for url in urls:
    video_title = download_video(url, output_path)
    sanitized_titles.append(video_title)
    video_path = os.path.join(output_path, f"{video_title}.mp4")

    extract_audio(video_path, output_path, video_title)

# writing time stamps
def write_timestamps_to_file(sanitized_titles, timestamps, output_path):
    with open(output_path, 'w') as f:
        for title, timestamp in zip(sanitized_titles, timestamps):
            f.write(f"Title: {title}, Start Time: {timestamp / 1000.0} seconds\n")

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
mix_audios_with_crossfade(audio_paths, output_path, crossfade_duration=23000)


# Calculate timestamps based on durations
durations = []
timestamps = [0]  # Start timestamp for first song is 0

for title in sanitized_titles:
    audio_path = os.path.join('/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output', f"{title}.m4a")
    audio = AudioSegment.from_file(audio_path, format="m4a")
    durations.append(len(audio))

for i in range(1, len(durations)):
    # Update timestamp with duration of the current song plus crossfade time which is subtracted because it is shared between two songs
    timestamps.append(timestamps[i-1] + durations[i-1] - 23000)

#converts seconds to minutes and seconds during file export
# def write_timestamps_to_file(sanitized_titles, timestamps, output_path):
#     with open(output_path, 'w') as f:
#         for title, timestamp in zip(sanitized_titles, timestamps):
#             minutes, seconds = divmod(timestamp / 1000.0, 60)
#             f.write(f"Title: {title}, Start Time: {int(minutes)} minutes {seconds:.3f} seconds\n")

# Writing timestamps to a text file
timestamps_output_path = '/Users/bradenbuchanan/Documents/pythonProgramming/youtubeMixer/output/timestamps.txt'
write_timestamps_to_file(sanitized_titles, timestamps, timestamps_output_path)
