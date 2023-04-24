# YouTubeMixCreator

## Description

The goal of this project is to download different music from YouTube and create mixes that are easy to upload. 

## Recommendations from GPT4 to optimize the script

1. Download audio directly: Instead of downloading both the video and audio, then extracting the audio, you can download just the audio directly. This will save time and storage space.
2. Use a configuration file for URLs: Instead of hardcoding the URLs in the script, you can use a separate configuration file (e.g., a JSON or text file) to store the URLs. This makes it easier to manage and update the URLs without modifying the script.
3. Customizable output path: Allow users to provide the output path as an argument or use a configuration file, so they can easily change the output location without modifying the script.
4. Error handling: Add proper error handling to handle potential issues, such as invalid URLs, network errors, or issues with file paths.
