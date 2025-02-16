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

res_music = "resources/sound/soundWithYT/"  # указываем директорию с чем угодно
all_mp3_music = [os.path.join(res_music, f) for f in os.listdir(res_music) if f.endswith('.mp3')]  # создаем список мп3 из папки
random_music = random.choice(all_mp3_music)  # выбираем случайный мп3 из списка
random_music = AudioFileClip(random_music)

duration_music = 30  # Длительность видео в секундах
start_time_music = 50
random_music = random_music.subclip(start_time_music, start_time_music + 30)
index_img_num = 0

res_bg_mod = "resources/backgrounds_modified2/"
all_jpg_png = ('.jpg', '.png')
all_image_bg_mod = [os.path.join(res_bg_mod, f) for f in os.listdir(res_bg_mod) if f.endswith(all_jpg_png)]
index_bg_mod = 0

res_video_clips = "resources/videoclips2/"
all_mp4 = ('.mp4')
all_video_clips = [os.path.join(res_video_clips, f) for f in os.listdir(res_video_clips) if f.endswith(all_mp4)]
index_video_clips = 0


def get_next_video_index(video_clips_directory):
    # Получаем список всех файлов в каталоге видеоклипов
    video_files = os.listdir(video_clips_directory)
    # Отфильтровываем список, чтобы остались только файлы с указанным шаблоном
    video_clips = [f for f in video_files if f.startswith('videoclip') and f.endswith('.mp4')]
    # Возвращаем количество таких файлов, что будет следующим индексом при создании нового видеоклипа
    print("последний видосик: ", len(video_clips))
    return len(video_clips)


index_bg_mod = get_next_video_index(res_video_clips)

for img_path, music_path in zip(all_image_bg_mod, all_mp3_music):
    # Загрузка картинки и музыки
    img_clip = ImageClip(img_path, duration=duration_music)
    music_clip = AudioFileClip(music_path).subclip(start_time_music, start_time_music + duration_music)

    # Соединяем картинку и музыку
    final_clip = img_clip.set_audio(music_clip)

    # Сохраняем видео в папку
    output_filename = f"videoclip{index_bg_mod}.mp4"
    output_path = os.path.join(res_video_clips, output_filename)

    final_clip.write_videofile(output_path, fps=60)
    final_clip.close()
    print(f"Создан видеоклип: {output_path}")
    # Инкрементируем индекс видеоклипа
    index_bg_mod += 1

print("Все видеоклипы были созданы.")
