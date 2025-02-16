import pygame
import os
import random
import moviepy.editor as mpe
import cv2
from PIL import Image

# Параметры
background_folder = "resources/backgrounds_original/"
output_folder = "resources/videoclips4/"
audio_file_path = "C:/Users/Артём Лютов/Downloads/m/скоро конец.mp3"
emoji_path = "resources/iconemoji/"
video_duration = 7  # длительность видео в секундах
video_size = (720, 1280)  # размер видео
text_lines = ["рождение", "садик", "1 класс", "2 класс", "3 класс", "4 класс", "5 класс", "6 класс", "7 класс", "8 класс", "9 класс", "10 класс", "11 класс",  "колледж", "универ", "работа", "пенсия"]  # Список событий
font_path = "C:/Windows/Fonts/Arial.ttf"
emoji_font_path = "C:/Windows/Fonts/seguiemj.ttf"  # Путь к шрифту со смайликами
gray = (70, 70, 70)

def get_random_smiley(path):
  """Загружает случайную картинку-смайлик из указанной папки.

  Args:
    path: Путь к папке со смайликами.

  Returns:
    Изображение смайлика в формате pygame.Surface.
  """

  # Получаем список всех файлов в папке.
  files = os.listdir(path)

  # Выбираем случайный файл.
  random_file = random.choice(files)

  # Инициализируем видеомодуль и создаем невидимое окно.
  pygame.display.init()
  pygame.display.set_mode((1, 1))

  # Загружаем изображение.
  emoji_image = pygame.image.load(os.path.join(path, random_file))

  # Уменьшаем размер изображения до 15x15 пикселей.
  emoji_image = pygame.transform.scale(emoji_image, (40, 40))

  return emoji_image.convert_alpha()

def get_next_video_number(output_folder):
    """
    Функция для получения номера, с которого начнется следующее видео.

    Параметры:
    - output_folder : str
      Путь к папке, где хранятся сгенерированные видео.

    Возвращает:
    - int : Номер следующего видео.
    """
    # Получаем список всех файлов в директории
    files = os.listdir(output_folder)

    # Фильтруем список, оставляя только видеофайлы с расширением '.mp4'
    video_files = [file for file in files if file.endswith('.mp4')]

    # Находим максимальный номер среди существующих видео
    max_number = 0
    for video_file in video_files:
        # Предполагаем, что имена файлов соответствуют шаблону "video_<номер>.mp4"
        number_part = video_file.replace('video_', '').replace('.mp4', '')
        try:
            number = int(number_part)
            max_number = max(max_number, number)
        except ValueError:
            # Если часть имени файла не преобразуется в число - пропускаем
            continue

    # Возвращаем следующий номер (максимальный номер + 1)
    return max_number + 1

start_number = get_next_video_number(output_folder)
print(f"Начинаем генерацию видео с номером {start_number}.")

def random_bright_color():
    while True:
        color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        # Проверяем, не слишком ли цвет близок к серому
        if max(color) - min(color) < 15:
            continue
        return color


# Функция для создания изображения с текстом и случайными галочками/крестиками
import os

def create_image_with_text(background_image_path, output_image_path, emoji_path):
    # Инициализируем Pygame
    pygame.init()

    # Загружаем и масштабируем фоновое изображение
    background = pygame.image.load(background_image_path)
    background = pygame.transform.scale(background, video_size)

    # Создаем поверхность для текста с поддержкой альфа-канала
    text_surface = pygame.Surface(video_size, pygame.SRCALPHA)

    # Загружаем шрифты
    font = pygame.font.Font(font_path, 30)

    # Отступ сверху и между строками
    top_padding = 100
    line_spacing = 50

    # Позиционируем текст и смайлики в отдельных строках
    text_x = 50
    text_y = top_padding
    emoji_x = text_x + 100
    emoji_y = text_y

    # Позиционируем второй столбец текста
    second_text_x = 300
    second_emoji_x = 350

    # Отступ смайликов от текста
    emoji_offset = 100

    # Добавляем текст
    for index, line in enumerate(text_lines):
        color = random_bright_color()

        # Добавляем текст
        text_surface.blit(font.render(line, True, color, gray), (text_x, text_y))

        # Загружаем случайный смайлик
        emoji = get_random_smiley(emoji_path)

        # Изменяем размер смайлика до 15x15 пикселей
        emoji = pygame.transform.scale(emoji, (40, 40))

        # Создаем поверхность для смайлика с поддержкой альфа-канала
        emoji_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Вставляем смайлик в поверхность
        emoji_surface.blit(emoji.convert(), (0, 0))



        # Добавляем случайный выбор надписи
        text = random.choice(["пока", "скоро", "не скоро", "сейчас", "гудбай", "привет"])

        # Добавляем второй столбец текста
        text_surface.blit(font.render(text, True, color, gray), (second_text_x, text_y))

        # Создаем поверхность для смайлика с поддержкой альфа-канала
        second_emoji_surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        # Вставляем смайлик в поверхность
        second_emoji_surface.blit(emoji, (0, 0))

        # Добавляем смайлик ко второму столбцу текста
        text_surface.blit(second_emoji_surface, (second_emoji_x + emoji_offset, emoji_y))

        # Увеличиваем позицию по вертикали для следующей строки
        text_y += line_spacing
        emoji_y += line_spacing

    # Наносим поверхность текста на фоновое изображение
    background.blit(text_surface, (0, 0))

    # Сохраняем изображение
    pygame.image.save(background, output_image_path)

    # Завершаем работу Pygame
    pygame.quit()


# Функция для создания видео
def create_video(output_video_path, image_path, audio_path):
    image_clip = mpe.ImageClip(image_path, duration=video_duration)
    audio_clip = mpe.AudioFileClip(audio_path).subclip(0, video_duration)
    final_clip = image_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_video_path, fps=24, audio_codec='aac')

# Создание видео файлов
for i in range(start_number, 1800):
    # Выбираем случайный фон
    random_background = random.choice(os.listdir(background_folder))
    background_image_path = os.path.join(background_folder, random_background)

    # Создаем изображение
    output_image_path = os.path.join(output_folder, f"video_{i}.png")
    create_image_with_text(background_image_path, output_image_path, emoji_path)

    # Создаем видео из изображения
    output_video_path = os.path.join(output_folder, f"video_{i}.mp4")
    create_video(output_video_path, output_image_path, audio_file_path)

    # Удаляем изображение после создания видео (если нужно освободить место)
    os.remove(output_image_path)