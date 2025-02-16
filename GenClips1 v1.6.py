import hashlib
import random

import pygame
import numpy as np
import os
from lybrarycolors import *
from ctypes import windll
from moviepy.editor import *

from PIL import Image, ImageDraw, ImageFont

pygame.init()  # инициализируем сам пайгейм

W = windll.user32.GetSystemMetrics(0) - 10  # ширина width
H = windll.user32.GetSystemMetrics(1) - 70  # высота height

font_text = ImageFont.truetype("arial.ttf", 128)  # указываем шрифт и размер (остальные знаки)
font_text_2 = ImageFont.truetype("arial.ttf", 64)  # указываем шрифт и размер (НАДПИСЬ СВЕРХУ)
font_text_1 = ImageFont.truetype("arial.ttf", 32)  # указываем шрифт и размер (знак вопроса)

res_music = "resources/sound/dancemusic"  # указываем директорию с чем угодно
all_mp3_music = [os.path.join(res_music, f) for f in os.listdir(res_music) if f.endswith('.mp3')]  # создаем список мп3 из папки
random_music = random.choice(all_mp3_music)  # выбираем случайный мп3 из списка
random_music = AudioFileClip(random_music)
 # загружает песню случайную из папки на фоне
#pygame.mixer.music.play(0, 50)

duration_music = 30  # Длительность видео в секундах
start_time_music = 50
random_music = random_music.subclip(start_time_music, start_time_music + 30)
index_img_num = 0

res_bg_mod = "resources/backgrounds_modified/"
all_jpg_png = ('.jpg', '.png')
all_image_bg_mod = [os.path.join(res_bg_mod, f) for f in os.listdir(res_bg_mod) if f.endswith(all_jpg_png)]
index_bg_mod = 0

res_video_clips = "resources/videoclips/"
all_mp4 = ('.mp4')
all_video_clips = [os.path.join(res_video_clips, f) for f in os.listdir(res_video_clips) if f.endswith(all_mp4)]
index_video_clips = 0

for y, object_bg_mod_path in enumerate(all_image_bg_mod):
    object_bg_mod_clip = Image.open(object_bg_mod_path)
    object_bg_mod_clip_np = np.array(object_bg_mod_clip)
    create_clip = ImageClip(object_bg_mod_clip_np)
    video_clip = CompositeVideoClip([create_clip.set_duration(duration_music)])
    video_clip = video_clip.set_audio(random_music)
    hash_md5 = hashlib.md5()
    with open(object_bg_mod_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    file_hash = hash_md5.hexdigest()
    if os.path.exists(res_video_clips):
        for i, video_clips_path in enumerate(all_video_clips):
            object_video_clip = open(video_clips_path)
            existing_file_hash = hashlib.md5(open(video_clips_path, "rb").read()).hexdigest()
            # Проверка совпадения имени файла и хэш-суммы
        if file_hash == existing_file_hash:
            print("Файл с таким именем и хэш-суммой уже существует")
        else:
            # Сохранение видео с уникальным именем
            video_clip.write_videofile(f"resources/videoclips/videoclip{index_bg_mod}.mp4", fps=60)
            index_bg_mod = (index_bg_mod + 1) % len(res_bg_mod)
            index_video_clips = (index_bg_mod + 1)
    else:
        # Сохранение видео с уникальным именем
        video_clip.write_videofile(f"resources/videoclips/videoclip{index_bg_mod}.mp4", fps=60)
        index_bg_mod = (index_bg_mod + 1) % len(res_bg_mod)
        index_video_clips = (index_bg_mod + 1)




# Закрываем изображение
object_bg_mod_clip.close()

