import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
import pygame
import tkinter as tk
import threading
import time
import os

from get_geo_info import getGeoInfo
from get_introduction import get_introduction
from talk import talk

# === 設定 ===
CHROMEDRIVER_PATH = "C:/Users/hyper/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
MAP_FILENAME = "map_capture.png"
BGM_PATH = 'C:/Users/hyper/kazu_ws/tourist_guide/audios/Cat_life.mp3'
AUDIO_PATH = 'C:/Users/hyper/kazu_ws/tourist_guide/audios/audio.mp3'


# Pygame 初期化
pygame.init()
pygame.mixer.init()

# BGM再生
pygame.mixer.music.load(BGM_PATH)
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

# 音量復元用関数
def restore_bgm_volume():
    pygame.mixer.music.set_volume(1.0)

# 地図画像生成
def generate_map(lat, lng):
    m = folium.Map(location=[lat, lng], zoom_start=15)
    folium.Marker([lat, lng], tooltip="現在地").add_to(m)
    m.save("map.html")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=800,600")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("file://" + os.path.abspath("map.html"))
    time.sleep(2)
    driver.save_screenshot(MAP_FILENAME)
    driver.quit()

# 音声と地図表示のシーケンス
def run_audio_sequence():
    geo = getGeoInfo()
    lat,lng=35.682706174695916, 139.75970763389086
    lat, lng, loc = geo.get_geo_info(lat=lat, lng=lng)
    print(f"{lat:.3f}, {lng:.3f}, {loc['prefecture']}{loc['city']}{loc['town']}")

    # 地図生成
    generate_map(lat, lng)

    # 音声生成
    text = get_introduction(loc)
    print(text)

    speaker = talk()
    speaker.generate_wav(text, speaker=1, filepath=AUDIO_PATH)

    pygame.mixer.music.set_volume(0.3)
    se = pygame.mixer.Sound(AUDIO_PATH)
    se.set_volume(1.0)
    se.play()

    # 地図表示（pygameウィンドウ）
    image = pygame.image.load(MAP_FILENAME)
    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption("現在地付き地図")

    # 再生中だけ地図表示
    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False
        screen.blit(image, (0, 0))
        pygame.display.flip()

        if not pygame.mixer.get_busy():
            time.sleep(0.5)
            showing = False

    restore_bgm_volume()
    pygame.display.quit()

# ボタン押下時の処理
def on_button_click():
    threading.Thread(target=run_audio_sequence).start()

# GUI構築
root = tk.Tk()
root.title("Tourist Guide")
button = tk.Button(root, text="現在地案内を再生", command=on_button_click)
button.pack(padx=50, pady=30)
root.mainloop()
