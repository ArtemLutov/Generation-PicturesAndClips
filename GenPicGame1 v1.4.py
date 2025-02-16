import random
from ctypes import windll

import pygame
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

from lybrarycolors import *

pygame.init()  # инициализируем сам пайгейм

W = windll.user32.GetSystemMetrics(0) - 10  # ширина width
H = windll.user32.GetSystemMetrics(1) - 70  # высота height

font_text = ImageFont.truetype("arial.ttf", 128)  # указываем шрифт и размер (остальные знаки)
font_text_2 = ImageFont.truetype("arial.ttf", 64)  # указываем шрифт и размер (НАДПИСЬ СВЕРХУ)
font_text_1 = ImageFont.truetype("arial.ttf", 32)  # указываем шрифт и размер (знак вопроса)

#res_music = "resources/sound/dancemusic"  # указываем директорию с чем угодно
#all_mp3_music = [os.path.join(res_music, f) for f in os.listdir(res_music) if f.endswith('.mp3')]  # создаем список мп3 из папки
#random_music = random.choice(all_mp3_music)  # выбираем случайный мп3 из списка
#random_music = AudioFileClip(random_music)


#duration_music = 30  # Длительность видео в секундах
#start_time_music = 50
#random_music = random_music.subclip(start_time_music, start_time_music + 30)
index_img_num = 0

res_bg = "resources/backgrounds_original/"
all_jpg_png = ('.jpg', '.png')
all_image_bg = [os.path.join(res_bg, f) for f in os.listdir(res_bg) if f.endswith(all_jpg_png)]
index_bg = 0

res_bg_mod = "resources/backgrounds_modified/"
all_jpg_png = ('.jpg', '.png')
all_image_bg_mod = [os.path.join(res_bg_mod, f) for f in os.listdir(res_bg_mod) if f.endswith(all_jpg_png)]
index_bg_mod = 0

res_object = "resources/objects/"
all_image_object = [os.path.join(res_object, f) for f in os.listdir(res_object) if f.endswith(all_jpg_png)]
index_object = 0

res_object_monsters = "resources/objectsmonsters/"
all_jpg_png = ('.jpg', '.png')
all_image_monsters = [os.path.join(res_object_monsters, f) for f in os.listdir(res_object_monsters) if f.endswith(all_jpg_png)]
index_monsters = 0

res_object3 = "resources/objects3/"
all_jpg_png = ('.jpg', '.png')
all_image_object3 = [os.path.join(res_object3, f) for f in os.listdir(res_object3) if f.endswith(all_jpg_png)]
index_object3 = 0

res_object_animal = "resources/objectsanimals/"
all_jpg_png = ('.jpg', '.png')
all_image_animal = [os.path.join(res_object_animal, f) for f in os.listdir(res_object_animal) if f.endswith(all_jpg_png)]
index_object4 = 0

# Создание текстового изображения
text_img1 = Image.new('RGBA', (560, 48), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text1 = ImageDraw.Draw(text_img1)

text_img3 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text3 = ImageDraw.Draw(text_img3)
text_img5 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text5 = ImageDraw.Draw(text_img5)
text_img7 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text7 = ImageDraw.Draw(text_img7)
text_img9 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text9 = ImageDraw.Draw(text_img9)
text_img11 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text11 = ImageDraw.Draw(text_img11)
text_img13 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text13 = ImageDraw.Draw(text_img13)
text_img14 = Image.new('RGBA', (74, 74), (128, 128, 128, 0)) # размеры области, цвет, всё такое
draw_text14 = ImageDraw.Draw(text_img14)

    # СПРАВКА получается отступ по ширине: 100 + картинка 72 + отступ 28 + (плюс) 74 + отступ 28 потому откуда то координата 402 для равно появляется и я хуй знает как считать то
for bg_image_path in all_image_bg:
    img_bg = Image.open(bg_image_path)
    # Изменяем размеры
    img_bg = img_bg.resize((720, 1280)) # соотношение сторон 9:16 у телефона
    # Создаем новый объект ImageDraw
    draw = ImageDraw.Draw(img_bg)
    draw_text1.text((0, 0), "Нерешаемые задачи от деда-сергея", fill=white, font=font_text_1)
    img_bg.paste(text_img1, (100, 110))  # координаты откуда начинаем рисовать текстовую область

    draw_text3.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img3, (405, 220))  # координаты откуда начинаем рисовать текстовую область
    draw_text5.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img5, (405, 355))  # координаты откуда начинаем рисовать текстовую область
    draw_text7.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img7, (405, 490))  # координаты откуда начинаем рисовать текстовую область
    draw_text9.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img9, (405, 625))  # координаты откуда начинаем рисовать текстовую область
    draw_text11.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img11, (405, 760))  # координаты откуда начинаем рисовать текстовую область
    draw_text13.text((0, -35), "=", fill=white, font=font_text)
    img_bg.paste(text_img13, (405, 895))  # координаты откуда начинаем рисовать текстовую область
    draw_text14.text((0, -5), "??", fill=white, font=font_text_2)
    img_bg.paste(text_img14, (515, 895))  # координаты откуда начинаем рисовать текстовую область

    # Цикл по всем объектам
    for i, object_image_path in enumerate(all_image_object):
        object_img = Image.open(object_image_path)
        # Изменяем размеры
        object_img = object_img.resize((120, 120))

        # Определяем координаты для объекта
        # 1 ряд начало
        object_x = 75
        object_y = 200


        # Наложение объекта на фото
        # Начало 1 ряда
        img_bg.paste(object_img, (object_x, object_y))
        for u, object_monsters_path in enumerate(all_image_monsters):
            rand_sign = random.choice(["+", "-", "/", "*"])
            rand_sign2 = random.choice(["+", "-", "/", "*"])
            rand_sign3 = random.choice(["+", "-", "/", "*"])
            rand_sign4 = random.choice(["+", "-", "/", "*"])
            rand_sign5 = random.choice(["+", "-", "/", "*"])
            rand_sign6 = random.choice(["+", "-", "/", "*"])
            text_img2 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text2 = ImageDraw.Draw(text_img2)
            text_img4 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text4 = ImageDraw.Draw(text_img4)
            text_img6 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text6 = ImageDraw.Draw(text_img6)
            text_img8 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text8 = ImageDraw.Draw(text_img8)
            text_img10 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text10 = ImageDraw.Draw(text_img10)
            text_img12 = Image.new('RGBA', (74, 74), (128, 128, 128, 0))  # размеры области, цвет, всё такое
            draw_text12 = ImageDraw.Draw(text_img12)

            if rand_sign == "+":
                draw_text2.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign == "-":
                draw_text2.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign == "*":
                draw_text2.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign == "/":
                draw_text2.text((15, -25), "/", fill=white, font=font_text)

            if rand_sign2 == "+":
                draw_text4.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign2 == "-":
                draw_text4.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign2 == "*":
                draw_text4.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign2 == "/":
                draw_text4.text((15, -25), "/", fill=white, font=font_text)

            if rand_sign3 == "+":
                draw_text6.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign3 == "-":
                draw_text6.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign3 == "*":
                draw_text6.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign3 == "/":
                draw_text6.text((15, -25), "/", fill=white, font=font_text)

            if rand_sign4 == "+":
                draw_text8.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign4 == "-":
                draw_text8.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign4 == "*":
                draw_text8.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign4 == "/":
                draw_text8.text((15, -25), "/", fill=white, font=font_text)

            if rand_sign5 == "+":
                draw_text10.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign5 == "-":
                draw_text10.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign5 == "*":
                draw_text10.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign5 == "/":
                draw_text10.text((15, -25), "/", fill=white, font=font_text)

            if rand_sign6 == "+":
                draw_text12.text((0, -35), "+", fill=white, font=font_text)
            elif rand_sign6 == "-":
                draw_text12.text((15, -45), "-", fill=white, font=font_text)
            elif rand_sign6 == "*":
                draw_text12.text((10, -5), "*", fill=white, font=font_text)
            elif rand_sign6 == "/":
                draw_text12.text((15, -25), "/", fill=white, font=font_text)

            img_bg.paste(text_img2, (200, 220))  # координаты откуда начинаем рисовать текстовую область
            img_bg.paste(text_img4, (200, 355))  # координаты откуда начинаем рисовать текстовую область
            img_bg.paste(text_img6, (200, 490))  # координаты откуда начинаем рисовать текстовую область
            img_bg.paste(text_img8, (200, 625))  # координаты откуда начинаем рисовать текстовую область
            img_bg.paste(text_img10, (200, 760))  # координаты откуда начинаем рисовать текстовую область
            img_bg.paste(text_img12, (200, 895))  # координаты откуда начинаем рисовать текстовую область

            object_monsters_img = Image.open(object_monsters_path)
            random_object3 = random.choice(all_image_object3)
            random_object31 = random.choice(all_image_object3)
            random_animal_img = random.choice(all_image_animal)
            random_animal_img2 = random.choice(all_image_animal)
            object3_img = Image.open(random_object3)
            object31_img = Image.open(random_object31)
            animal_img = Image.open(random_animal_img)
            animal_img2 = Image.open(random_animal_img2)
            # Изменяем размеры
            object_monsters_img = object_monsters_img.resize((120, 120))
            object3_img = object3_img.resize((120, 120))
            object31_img = object31_img.resize((120, 120))
            animal_img = animal_img.resize((120, 120))
            animal_img2 = animal_img2.resize((120, 120))

            # Определяем координаты для объекта
            # 1 ряд продолжение
            object1_x = 280
            object1_y = object_y
            object_monsters2_x = 490
            object_monsters2_y = object_y
            # 2 ряд
            object_monsters3_x = 75
            object_monsters3_y = 335
            object4_x = 280
            object4_y = object_monsters3_y
            object5_x = 490
            object5_y = object4_y
            # 3 ряд
            object6_x = 75
            object6_y = 468
            object_monsters7_x = 280
            object_monsters7_y = object6_y
            object8_x = 490
            object8_y = object6_y
            # 4 ряд
            object9_x = 75
            object9_y = 602
            object10_x = 280
            object10_y = object9_y
            object11_x = 490
            object11_y = object9_y
            # 5 ряд
            object12_x = 75
            object12_y = 737
            object13_x = 280
            object13_y = object12_y
            object14_x = 490
            object14_y = object12_y
            # 6 ряд
            object15_x = 75
            object15_y = 872
            object16_x = 280
            object16_y = object15_y


            # Наложение объекта на фото
            # 1 ряд
            img_bg.paste(animal_img2, (object1_x, object1_y))
            img_bg.paste(object_monsters_img, (object_monsters2_x, object_monsters2_y))
            img_bg.paste(object_monsters_img, (object_monsters3_x, object_monsters3_y))
            img_bg.paste(object_img, (object4_x, object4_y))
            img_bg.paste(object3_img, (object5_x, object5_y))

            img_bg.paste(object3_img, (object6_x, object6_y))
            img_bg.paste(object_monsters_img, (object_monsters7_x, object_monsters7_y))
            img_bg.paste(animal_img, (object8_x, object8_y))
            img_bg.paste(object31_img, (object9_x, object9_y))
            img_bg.paste(object_img, (object10_x, object10_y))
            img_bg.paste(animal_img, (object11_x, object11_y))
            img_bg.paste(object31_img, (object12_x, object12_y))
            img_bg.paste(animal_img, (object13_x, object13_y))
            img_bg.paste(object_monsters_img, (object14_x, object14_y))
            img_bg.paste(animal_img, (object15_x, object15_y))
            img_bg.paste(object3_img, (object16_x, object16_y))
            # Сохраняем измененное изображение
            img_bg.save(f"resources/backgrounds_modified/image_modified{index_img_num}.png")
            index_bg = (index_bg + 1) % len(res_bg)
            index_object = (index_object + 1) % len(res_object)
            index_monsters = (index_monsters + 1) % len(res_object_monsters)
            index_object3 = (index_object3 + 1) % len(res_object3)
            index_img_num = (index_img_num + 1)
            #for y, object_bg_mod_path in enumerate(all_image_bg_mod):
#
            #    object_bg_mod_clip = Image.open(object_bg_mod_path)
            #    object_bg_mod_clip_np = np.array(object_bg_mod_clip)
            #    create_clip = ImageClip(object_bg_mod_clip_np)
            #    video_clip = CompositeVideoClip([create_clip.set_duration(duration_music)])
            #    video_clip = video_clip.set_audio(random_music)
            #    video_clip.write_videofile(f"resources/videoclips/videoclip{index_bg_mod}.mp4", fps=60)
            #    index_bg_mod = (index_bg_mod + 1) % len(res_bg_mod)


# Закрываем изображение
img_bg.close()
object_img.close()
object_monsters_img.close()
object3_img.close()
random_animal_img.close()
random_animal_img2.close()
