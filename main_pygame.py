import pygame
import tkinter as tk
from get_geo_info import getGeoInfo
from get_introduction import get_introduction
from talk import talk
import threading
import time

# ファイルパス
BGM_PATH = 'C:/Users/hyper/kazu_ws/tourist_guide/audios/Cat_life.mp3'
AUDIO_PATH = 'C:/Users/hyper/kazu_ws/tourist_guide/audios/audio.mp3'

# 初期化
pygame.init()
pygame.mixer.init()

# BGMの再生
pygame.mixer.music.load(BGM_PATH)
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)  # ループ再生

# 音量回復処理
def restore_bgm_volume():
    pygame.mixer.music.set_volume(1.0)

# ボタン押下時の処理
def on_button_click():
    threading.Thread(target=run_audio_sequence).start()  # GUIを止めないように別スレッドで実行

def run_audio_sequence():
    # 地理情報と紹介文取得
    cls = getGeoInfo()
    lat, lng, loc = cls.get_geo_info()
    print(f"{lat:.3f} {lng:.3f} {loc['prefecture']}{loc['city']}{loc['town']}")

    text = get_introduction(loc)
    print(text)

    # 音声合成
    cls2 = talk()
    cls2.generate_wav(text, speaker=1, filepath=AUDIO_PATH)
    
    # BGM音量を下げる
    pygame.mixer.music.set_volume(0.3)

    # 効果音として再生
    se_sound = pygame.mixer.Sound(AUDIO_PATH)
    se_sound.set_volume(1.0)
    se_sound.play()

    # 再生が終わるまで待機
    while pygame.mixer.get_busy():
        time.sleep(0.1)

    # BGM音量を戻す
    restore_bgm_volume()

# GUI構築
root = tk.Tk()
root.title("Tourist Guide")

button = tk.Button(root, text="現在地案内を再生", command=on_button_click)
button.pack(padx=50, pady=30)

# GUI実行
root.mainloop()
