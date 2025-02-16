import os

import pygame
import random
import lybrarycolors

# Инициализация Pygame и шрифта
pygame.init()
pygame.font.init()

# Константы
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280
CUBE_SIZE = 50  # Размер кубика
CUBES_PER_ROW = 3  # Количество кубиков в ряду
MARGIN = 20      # Отступы
TEXT_MARGIN = 150 # Отступ для текста
EQUALS_MARGIN = CUBE_SIZE

# Цвета
GRAY = (192, 192, 192)
PINK = (255, 160, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка экрана
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Unsolvable exercise of GODFATHER SERGEI')

# Настройка шрифта
font = pygame.font.SysFont('Arial', 32)
font2 = pygame.font.SysFont('Arial', 64)

res_bg = "resources/backgrounds_original/"
all_jpg_png = ('.jpg', '.png')
all_image_bg = [os.path.join(res_bg, f) for f in os.listdir(res_bg) if f.endswith(all_jpg_png)]
index_bg = 0
#random_bg = random.choice(all_image_bg)  # выбираем случайный задний фон из списка
#background_image = pygame.image.load(random_bg)
#background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Класс ColoredCube
class ColoredCube:
    def __init__(self, size):
        self.size = size
        self.colors = [GRAY, PINK]
        self.cubes = [[random.choice(self.colors) for _ in range(3)] for _ in range(3)]

    def draw(self, surface, position):
        # Отрисовка кубиков
        for i in range(3):
            for j in range(3):
                color = self.cubes[i][j]
                rect = pygame.Rect(
                    position[0] + j*self.size, position[1] + i*self.size,
                    self.size, self.size
                )
                pygame.draw.rect(surface, color, rect, 0)
                pygame.draw.rect(surface, WHITE, rect, 2)  # Границы кубика


# Отрисовка текста
def draw_text(surface, text, position, text_size, text_color):
    font = pygame.font.SysFont('Arial', text_size)
    text_surface = font.render(text, True, text_color, BLACK)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)

def get_next_image_index(save_dir):
    # Получаем список всех файлов в каталоге сохранения
    existing_files = os.listdir(save_dir)
    # Отфильтровываем список, чтобы остались только файлы с указанным шаблоном
    existing_images = [filename for filename in existing_files if filename.startswith('image_modified_') and filename.endswith('.png')]
    # Возвращаем количество этих файлов
    print('последний номер генерации: ', len(existing_images))
    return len(existing_images)


def save_image(screen, filename):
    pygame.image.save(screen, filename)


save_dir = 'resources/backgrounds_modified2/'
# Создание списка кубиков
def main():
    next_index = get_next_image_index(save_dir)  # Получаем следующий индекс
    os.makedirs(save_dir, exist_ok=True)

    for index, bg_path in enumerate(all_image_bg, start=next_index):

        cubes = [ColoredCube(CUBE_SIZE) for _ in range(15)]
        background_image = pygame.image.load(bg_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Создаём новый поверхностный объект, который будет служить холстом
        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Очистка холста и отрисовка фона
        canvas.blit(background_image, (0, 0))

        # Отрисовка надписи
        draw_text(canvas, "Unsolvable exercise of GODFATHER SERGEI", (SCREEN_WIDTH // 2, 55), 32, PINK)

        # Отрисовка кубиков
        for row in range(4):
            for column in range(3):
                # Вычисляем X координату для первого и второго кубика
                cube_x = MARGIN + column * (CUBE_SIZE + MARGIN)
                cube_y = TEXT_MARGIN + row * (CUBE_SIZE * 3 + MARGIN * 2)

                # Позиция первого кубика в каждом ряду
                first_cube_x = MARGIN
                first_cube_y = TEXT_MARGIN + row * (CUBE_SIZE * 3 + MARGIN)

                # Отрисовка первого кубика
                cube = cubes[row * 3]  # Первый кубик в каждом ряду
                cube.draw(canvas, (first_cube_x, first_cube_y))

                # Позиция второго кубика
                second_cube_x = first_cube_x + CUBE_SIZE * 3 + MARGIN
                second_cube_y = first_cube_y

                # Отрисовка второго кубика
                cube = cubes[row * 3 + 1]  # Второй кубик в каждом ряду
                cube.draw(canvas, (second_cube_x, second_cube_y))

                # Позиция знака равенства
                equals_x = second_cube_x + CUBE_SIZE * 3 + MARGIN * 2
                equals_y = first_cube_y + CUBE_SIZE  # Середина кубика по вертикали

                # Отображение знака равно
                draw_text(canvas, '=', (equals_x, equals_y), 64, PINK)  # Например, зададим размер в 64

                if row < 3:  # Для первых трёх строк рисуем третий кубик
                    third_cube_x = equals_x + MARGIN * 2
                    third_cube_y = first_cube_y
                    cube = cubes[row * 3 + 2]
                    cube.draw(canvas, (third_cube_x, third_cube_y))
                else:  # В четвёртом ряду после знака равенства ставим "??"
                    question_x = equals_x + MARGIN * 6
                    draw_text(canvas, '??', (question_x, equals_y), 64, PINK)  # Например, зададим размер в 64
        save_path = os.path.join(save_dir, f'image_modified_{index + 1}.png')
        pygame.image.save(canvas, save_path)
        print(f"Saved: {save_path}")
    # После выполнения всех операций
    print("All images have been saved.")
    pygame.quit()

if __name__ == "__main__":
    # Инициализация Pygame не требует создания окна
    pygame.init()
    main()