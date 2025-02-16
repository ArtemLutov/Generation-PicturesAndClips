import os
import pygame
import sys
import random
import math
import cv2
import numpy as np
import subprocess
from moviepy.editor import *
import lybrarycolors

# Инициализация Pygame без окна
pygame.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)

# Определение параметров
screen_size = (720, 1280)
fps = 30
video_length_seconds = 30
frames_per_video = fps * video_length_seconds

number_of_videos_to_generate = 1600     # указываю сколько хочу видео по итогу загенерить
# Пути к ресурсам
res_bg = "resources/backgrounds_original/"
res_music = "resources/sound/soundWithYTcopyright/"
output_folder = "resources/videoclips3/"

# Получение списка фоновых изображений и музыки
all_jpg_png = ('.jpg', '.png')
all_image_bg = [os.path.join(res_bg, f) for f in os.listdir(res_bg) if f.endswith(all_jpg_png)]
all_music = [os.path.join(res_music, f) for f in os.listdir(res_music) if f.endswith('.mp3')]

# Создание виртуального экрана с поддержкой прозрачности
virtual_screen = pygame.Surface(screen_size, pygame.SRCALPHA)
font = pygame.font.SysFont('Arial', 42)
black = (0, 0, 0)
names_list = [
    "Alexander", "Maria", "Maxim", "Olga", "Ivan", "Sofia", "Mikhail", "Anastasia", "Sergey",
    "Daria", "Dmitry", "Elena", "Alexey", "Katya", "Nikolay", "Anna", "Vladimir", "Victoria",
    "Andrey", "Ksenia", "Artem", "Svetlana", "Pavel", "Yulia", "Kirill", "Alina", "Igor",
    "Olesya", "Egor", "Yana", "Denis", "Polina", "Anton", "Natalia", "Vadim", "Galina",
    "Stanislav", "Elizaveta", "Konstantin", "Tatiana", "Roman", "Irina", "Viktor", "Marina",
    "Evgeny", "Nadezhda", "Boris", "Lyudmila", "Oleg", "Larisa", "Ruslan", "Valeria",
    "Leonid", "Olivia", "Yaroslav", "Veronika", "Georgy", "Diana", "Daniil", "Alla",
    "Nikita", "Ekaterina", "Makar", "Anya", "Gleb", "Lilia", "Timofey", "Ulyana",
    "Fedor", "Karina", "Petr", "Eva", "Grigory", "Milana", "Eduard", "Daria",
    "Stepan", "Lada", "Vasily", "Sofia", "Yuri", "Lina", "Alexander", "Zoya",
    "Vladislav", "Kira", "Kuzma", "Inna", "Artyom", "Serafima", "Matvey", "Angelina",
    # Добавим еще имен для достижения 300
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas",
    "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul",
    "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald",
    "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan",
    "Stephen", "Larry", "Justin", "Scott", "Brandon", "Frank", "Benjamin", "Gregory", "Raymond",
    "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose",
    "Henry", "Douglas", "Adam", "Peter", "Nathan", "Zachary", "Walter", "Kyle", "Harold",
    "Carl", "Jeremy", "Keith", "Roger", "Gerald", "Ethan", "Arthur", "Terry", "Christian",
    "Sean", "Lawrence", "Austin", "Joe", "Noah", "Jesse", "Albert", "Bryan", "Billy", "Bruce",
    "Willie", "Jordan", "Dylan", "Alan", "Ralph", "Gabriel", "Roy", "Juan", "Wayne", "Eugene",
    "Logan", "Randy", "Louis", "Russell", "Vincent", "Philip", "Bobby", "Johnny", "Bradley"
]


def random_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

# Убедимся, что папка для сохранения видео существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Добавление текста на виртуальный экран перед его записью в видео
def draw_text(surface, text_top, text_bottom):
    font = pygame.font.SysFont('Arial', 34)
    text_surface_top = font.render(text_top, True, pygame.Color('black'), pygame.Color('gray'))
    text_surface_bottom = font.render(text_bottom, True, pygame.Color('black'), pygame.Color('gray'))

    text_rect_top = text_surface_top.get_rect(center=(screen_size[0] // 2, 150))
    text_rect_bottom = text_surface_bottom.get_rect(center=(screen_size[0] // 2, 200))  # последнее значение больше = ниже текст.

    surface.blit(text_surface_top, text_rect_top.topleft)
    surface.blit(text_surface_bottom, text_rect_bottom.topleft)


existing_videos = len([name for name in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, name)) and name.endswith('.mp4')])
video_count = existing_videos  # Стартуем с последнего существующего видеофайла

print(f"Получается начинаем создание видео с номера: {video_count}")

while video_count < number_of_videos_to_generate:
    bg_img_path = all_image_bg[video_count % len(all_image_bg)]
    music_path = all_music[video_count % len(all_music)]
    random_name = random.choice(names_list)  # Выбор случайного имени для текста

    temp_video_name = f'temp_videoclip{video_count}.mp4'
    final_video_name = f'final_videoclip{video_count}.mp4'
    temp_video_output_path = os.path.join('resources/', temp_video_name)
    final_video_output_path = os.path.join(output_folder, final_video_name)

    print(f"Запуск работы над видео номер {video_count}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(temp_video_output_path, fourcc, fps, (screen_size[0], screen_size[1]))

    if not video_writer.isOpened():
        print(f"Не удалось открыть файл {temp_video_output_path} для записи.")
        continue

    background = pygame.image.load(bg_img_path).convert()
    background = pygame.transform.scale(background, screen_size)

    angle = 0
    separation = 0
    separation_change = 0.25

    # Создаем контент для видео
    content_list = [str(random.randint(1, 100)) for _ in range(7)] + ["??"]
    random.shuffle(content_list)
    segment_colors = [random_color() for _ in range(8)]

    # Цикл для создания и записи каждого кадра видео
    for frame_number in range(frames_per_video):
        # Очищаем экран
        virtual_screen.fill((0, 0, 0))

        # Загружаем и рендерим фон
        background = pygame.image.load(bg_img_path).convert()
        background = pygame.transform.scale(background, screen_size)

        virtual_screen.blit(background, (0, 0))

        separation += separation_change
        if separation > 20 or separation < 0:
            separation_change *= -1  # Изменение направления движения восьмиугольника

        center_x, center_y = screen_size[0] // 2, screen_size[1] // 2
        inner_radius, outer_radius = 200, 300

        # Отрисовка восьмиугольника
        for i in range(8):
            angle_offset = (math.pi * 2 / 8) * i
            next_angle_offset = (math.pi * 2 / 8) * (i + 1)

            separation_offset = separation * (i % 2 * 2 - 1)

            inner_point = (center_x + math.cos(angle_offset + math.radians(angle)) * (inner_radius + separation_offset),
                           center_y + math.sin(angle_offset + math.radians(angle)) * (inner_radius + separation_offset))
            next_inner_point = (center_x + math.cos(next_angle_offset + math.radians(angle)) * (inner_radius + separation_offset),
                                center_y + math.sin(next_angle_offset + math.radians(angle)) * (inner_radius + separation_offset))
            outer_point = (center_x + math.cos(next_angle_offset + math.radians(angle)) * (outer_radius + separation_offset),
                           center_y + math.sin(next_angle_offset + math.radians(angle)) * (outer_radius + separation_offset))
            next_outer_point = (center_x + math.cos(angle_offset + math.radians(angle)) * (outer_radius + separation_offset),
                                center_y + math.sin(angle_offset + math.radians(angle)) * (outer_radius + separation_offset))

            points = [inner_point, next_inner_point, outer_point, next_outer_point]
            pygame.draw.polygon(virtual_screen, segment_colors[i], points)
            pygame.draw.lines(virtual_screen, black, True, points, 5)

            # Опционально: добавление текста на каждый сегмент восьмиугольника
            # (исправьте расположение текста по вашему предпочтению)
            text_surf = font.render(content_list[i], True, black)
            text_rect = text_surf.get_rect(center=((inner_point[0] + next_inner_point[0] + outer_point[0] + next_outer_point[0]) / 4,
                                                   (inner_point[1] + next_inner_point[1] + outer_point[1] + next_outer_point[1]) / 4))
            virtual_screen.blit(text_surf, text_rect)

        angle += 0.25  # Увеличиваем угол для вращения в следующем кадре

        # Добавляем текст на каждый кадр
        text_top_position = (screen_size[0] // 2 - 200, 100)
        text_bottom_position = (screen_size[0] // 2 - 200, 150)
        draw_text(virtual_screen, "Unsolvable exercise of GODFATHER SERGEI", f"Send a video for {random_name}")

        # Конвертируем кадр из Pygame в формат, подходящий для OpenCV
        frame = pygame.surfarray.array3d(virtual_screen)
        frame = cv2.transpose(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        video_writer.write(frame)  # Записываем кадр в видеофайл

    video_writer.release()  # Высвобождаем записывающий объект

    # Добавление аудио к видео с использованием FFmpeg
    start_time = random.randint(30, 50)  # Начальное время для аудио
    duration = video_length_seconds  # Продолжительность аудио

    ffmpeg_command = [
        'C:/Users/Артём Лютов/ffmpeg-2024/ffmpeg/bin/ffmpeg.exe',  # Проверьте и укажите актуальный путь
        '-y',
        '-i', temp_video_output_path,
        '-ss', str(start_time),  # Случайное начальное время аудио
        '-t', str(video_length_seconds),  # Длительность аудио – 30 секунд
        '-i', music_path,
        '-async', '1',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict',
        '-2',
        final_video_output_path
    ]

    subprocess.run(ffmpeg_command)


    if os.path.exists(temp_video_output_path):
        os.remove(temp_video_output_path)  # Удаляем временный файл

    print(f"Видео {final_video_name} создано")

    video_count += 1  # Увеличиваем счетчик видео

print("Все видео были успешно созданы.")
pygame.quit()
sys.exit()