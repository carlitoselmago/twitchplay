#!/usr/bin/env python3
import os
import time
import subprocess
import requests
from datetime import datetime

# === CONFIGURATION ===
TWITCH_CHANNEL = "example_channel"  # <-- change this
VIDEO_PATH = "/home/pi/video.mp4"   # full path to save video
CHECK_URL = "https://www.google.com"
RETRY_INTERVAL = 10                 # seconds between internet checks

# === FUNCTIONS ===
def wait_for_internet():
    """Wait until the system has an active internet connection."""
    print("[INFO] Waiting for internet connection...")
    while True:
        try:
            requests.get(CHECK_URL, timeout=5)
            print("[INFO] Internet connection detected.")
            return
        except requests.RequestException:
            print("[INFO] No connection yet, retrying in", RETRY_INTERVAL, "seconds...")
            time.sleep(RETRY_INTERVAL)

def download_latest_twitch_video(channel, output_path):
    """Use yt-dlp to download the latest VOD from a Twitch channel."""
    tmp_output = output_path + ".tmp.mp4"
    cmd = [
        "yt-dlp",
        f"https://www.twitch.tv/{channel}",
        "-o", tmp_output,
        "--no-playlist",  # only the latest VOD
        "--max-downloads", "1",
        "--progress"
    ]
    print("[INFO] Starting download from Twitch:", channel)
    try:
        subprocess.run(cmd, check=True)
        # If successful, replace the old video
        if os.path.exists(tmp_output):
            os.replace(tmp_output, output_path)
            print("[INFO] Download complete. Saved as:", output_path)
            return True
    except subprocess.CalledProcessError:
        print("[ERROR] yt-dlp failed to download the video.")
    except Exception as e:
        print("[ERROR]", e)
    return False

def play_video_loop(video_path):
    """Play the video in an infinite loop using VLC."""
    if not os.path.exists(video_path):
        print("[ERROR] No video found to play.")
        return
    print("[INFO] Launching VLC in loop mode...")
    subprocess.run(["cvlc", "--loop", "--fullscreen", video_path])

# === MAIN SCRIPT ===
if __name__ == "__main__":
    wait_for_internet()
    success = download_latest_twitch_video(TWITCH_CHANNEL, VIDEO_PATH)
    if not success:
        print("[WARN] Using previously downloaded video.")
    play_video_loop(VIDEO_PATH)
