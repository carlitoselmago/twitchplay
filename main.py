#!/usr/bin/env python3
import os
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
TWITCH_CHANNEL = "rubysky9"  # <-- your channel
VIDEO_PATH = "/home/zorin/code/twitchplay/video.mp4"
CHECK_URL = "https://www.google.com"
RETRY_INTERVAL = 10

def wait_for_internet():
    print("[INFO] Waiting for internet connection...")
    while True:
        try:
            requests.get(CHECK_URL, timeout=5)
            print("[INFO] Internet connection detected.")
            return
        except requests.RequestException:
            print(f"[INFO] No connection yet, retrying in {RETRY_INTERVAL}s...")
            time.sleep(RETRY_INTERVAL)

def get_latest_vod_url(channel):
    """Render Twitch videos page and extract the latest VOD link."""
    #url = f"https://www.twitch.tv/{channel}/videos?filter=archives&sort=time"
    url = f"https://www.twitch.tv/{channel}/videos?sort=time"
    print("[INFO] Loading page:", url)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    vod_url = None
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/videos/']"))
        )
        print(elements)
        if elements:
            href = elements[0].get_attribute("href")
            vod_url = href.split("?")[0]
            print("[INFO] Found VOD:", vod_url)
    except Exception as e:
        print("[ERROR] Failed to get VOD link:", e)
    finally:
        driver.quit()
    return vod_url

def download_video(vod_url, output_path):
    tmp_path = output_path + ".tmp.mp4"
    cmd = ["yt-dlp", vod_url, "-o", tmp_path, "--progress", "--max-downloads", "1"]
    print("[INFO] Downloading:", vod_url)
    try:
        subprocess.run(cmd, check=True)
        if os.path.exists(tmp_path):
            os.replace(tmp_path, output_path)
            print("[INFO] Download complete ->", output_path)
            return True
    except subprocess.CalledProcessError:
        print("[ERROR] yt-dlp failed to download the video.")
    except Exception as e:
        print("[ERROR]", e)
    return False

def play_video_loop(video_path):
    if not os.path.exists(video_path):
        print("[ERROR] No video found to play.")
        return
    print("[INFO] Playing video on loop...")
    subprocess.run(["cvlc", "--loop", "--fullscreen", video_path])

if __name__ == "__main__":
    wait_for_internet()
    vod_url = get_latest_vod_url(TWITCH_CHANNEL)
    success = vod_url and download_video(vod_url, VIDEO_PATH)
    if not success:
        print("[WARN] Using previously downloaded video.")
    play_video_loop(VIDEO_PATH)
