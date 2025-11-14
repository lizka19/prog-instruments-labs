import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1000, 800))

clock = pygame.time.Clock()

text_preset = pygame.font.SysFont('arial', 27)
text_preset_mini = pygame.font.SysFont('arial', 10)

fon = (238, 198, 170)
interface = (171, 205, 239)
text_color = (153, 102, 102)


class PhysicsConstants:
    GRAVITY = 9.8
    TIME_STEP = 0.0001
    MAX_TIME = 10.0  # Защита от бесконечного цикла


class DisplayConstants:
    SERIF_SPACING = 30
    AXIS_OFFSET = 20
    LINE_WIDTH = 3


class TrajectoryCalculator:
    def __init__(self, start_speed):
        self.v_0 = start_speed
        self.coords = []
        self.s = 0
        self.h = 0
        self.a_angle = None

    def calculate_trajectory(self, a_angle):
        """Рассчитывает траекторию для заданного угла.
        Возвращает кортеж (координаты, дальность, высота)
        Является идемпотентной функцией - при одинаковых входных данных возвращает одинаковый результат"""
        if not (0 <= a_angle <= math.pi / 2):
            raise ValueError("Angle must be between 0 and π/2")

        return self._calculate_physics(a_angle)

    def _calculate_physics(self, a_angle):
        """Чистая функция вычислений траектории"""
        coords = []
        t = 0
        s = self.v_0 ** 2 * math.sin(2 * a_angle) / PhysicsConstants.GRAVITY
        h = self.v_0 ** 2 * math.sin(a_angle) ** 2 / (2 * PhysicsConstants.GRAVITY)

        iteration_count = 0
        max_iterations = int(PhysicsConstants.MAX_TIME / PhysicsConstants.TIME_STEP)

        while iteration_count < max_iterations:
            x = (self.v_0 * math.cos(a_angle) * t)
            y = -(x * math.tan(a_angle) - x ** 2 * (
                        PhysicsConstants.GRAVITY / (2 * self.v_0 ** 2 * math.cos(a_angle) ** 2)))
            coords.append((x, y))
            t += PhysicsConstants.TIME_STEP
            iteration_count += 1

            if y > 0.001:  # Упрощенное условие выхода
                break

        # Обновляем состояние только после успешного расчета
        self.coords = coords
        self.s = s
        self.h = h
        self.a_angle = a_angle

        return coords, s, h


class CoordinateSystem:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y

    def draw_axes(self, screen):
        pygame.draw.line(screen, 'blue', (self.start_x, self.start_y), (self.start_x, 200))
        pygame.draw.line(screen, 'blue', (self.start_x, self.start_y), (800, self.start_y))

    def draw_scale_marks(self, screen, scale):
        self._draw_vertical_scale_marks(screen, scale)
        self._draw_horizontal_scale_marks(screen, scale)

    def _draw_vertical_scale_marks(self, screen, scale):
        """Отрисовка вертикальных меток (ось Y)"""
        for serif, text_value in zip(range(self.start_y, 200, -DisplayConstants.SERIF_SPACING),
                                     range(0, self.start_y, DisplayConstants.SERIF_SPACING)):
            pygame.draw.line(screen, 'blue', (self.start_x - 2, serif), (self.start_x + 2, serif))
            text = text_preset_mini.render('{:<03.2f}'.format(text_value / scale), True, 'black')
            screen.blit(text, (self.start_x - DisplayConstants.AXIS_OFFSET, serif))

    def _draw_horizontal_scale_marks(self, screen, scale):
        """Отрисовка горизонтальных меток (ось X)"""
        for serif, text_value in zip(range(self.start_x, 800, DisplayConstants.SERIF_SPACING),
                                     range(0, self.start_x + 1000, DisplayConstants.SERIF_SPACING)):
            text = text_preset_mini.render('{:<03.2f}'.format(text_value / scale), True, 'black')
            screen.blit(text, (serif, self.start_y + 10))
            pygame.draw.line(screen, 'blue', (serif, self.start_y - 2), (serif, self.start_y + 2))


class TrajectoryRenderer:
    def __init__(self, start_pos, color):
        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.color = color

    def draw_trajectory(self, screen, coords, scale):
        if not coords:
            return  # Защита от пустых данных

        for num in range(len(coords) - 1):
            start_point = self._scale_point(coords[num], scale)
            end_point = self._scale_point(coords[num + 1], scale)
            pygame.draw.line(screen, self.color, start_point, end_point, DisplayConstants.LINE_WIDTH)

    def _scale_point(self, point, scale):
        """Масштабирует точку согласно текущему масштабу"""
        return (point[0] * scale + self.start_x, point[1] * scale + self.start_y)

    def draw_metrics(self, screen, scale, main_stats, s, h):
        self._draw_main_metrics(screen, main_stats, s, h)
        self._draw_height_marker(screen, scale, h)
        self._draw_distance_marker(screen, scale, s)

    def _draw_main_metrics(self, screen, main_stats, s, h):
        """Отрисовка основных числовых метрик"""
        s_text = text_preset.render(str('{:0<1.2f}'.format(s)), True, self.color)
        screen.blit(s_text, main_stats)

        h_text = text_preset.render(str('{:0<1.2f}'.format(h)), True, self.color)
        screen.blit(h_text, (main_stats[0], main_stats[1] + 50))

    def _draw_height_marker(self, screen, scale, h):
        """Отрисовка маркера высоты на графике"""
        height_y = -h * scale + self.start_y
        pygame.draw.line(screen, self.color,
                         (self.start_x - 2, height_y),
                         (self.start_x + 2, height_y),
                         DisplayConstants.LINE_WIDTH)

        height_text = text_preset_mini.render(str(round(h, 2)), True, self.color)
        screen.blit(height_text, (self.start_x + 10, height_y))

    def _draw_distance_marker(self, screen, scale, s):
        """Отрисовка маркера дальности на графике"""
        distance_x = s * scale + self.start_x
        pygame.draw.line(screen, self.color,
                         (distance_x, self.start_y - 2),
                         (distance_x, self.start_y + 2),
                         DisplayConstants.LINE_WIDTH)

        distance_text = text_preset_mini.render(str(round(s, 2)), True, self.color)
        screen.blit(distance_text, (distance_x, self.start_y - 15))


class Graphic:
    def __init__(self, start_pos, start_speed, color):
        self.calculator = TrajectoryCalculator(start_speed)
        self.coord_system = CoordinateSystem(start_pos[0], start_pos[1])
        self.renderer = TrajectoryRenderer(start_pos, color)
        self.start_x, self.start_y = start_pos
        self.color = color

    def calculate_and_update_trajectory(self, a_angle):
        """Рассчитывает и обновляет траекторию.
        Является предсказуемой - всегда возвращает одинаковый результат для одинаковых входных данных"""
        try:
            coords, s, h = self.calculator.calculate_trajectory(a_angle)
            return True  # Успешное выполнение
        except ValueError as e:
            print(f"Ошибка расчета траектории: {e}")
            return False  # Ошибка выполнения

    def draw(self, screen, scale, main_stats):
        """Отрисовка всех компонентов графика"""
        self._draw_trajectory_component(screen, scale)
        self._draw_coordinate_system(screen, scale)
        self._draw_metrics_component(screen, scale, main_stats)

    def _draw_trajectory_component(self, screen, scale):
        """Отрисовка траектории"""
        if self.calculator.coords:
            self.renderer.draw_trajectory(screen, self.calculator.coords, scale)

    def _draw_coordinate_system(self, screen, scale):
        """Отрисовка системы координат"""
        self.coord_system.draw_axes(screen)
        self.coord_system.draw_scale_marks(screen, scale)

    def _draw_metrics_component(self, screen, scale, main_stats):
        """Отрисовка метрик"""
        self.renderer.draw_metrics(screen, scale, main_stats,
                                   self.calculator.s, self.calculator.h)


def check_position(x, y, width, height):
    cursor_x = pygame.mouse.get_pos()[0]
    cursor_y = pygame.mouse.get_pos()[1]

    if x < cursor_x < x + width and y < cursor_y < y + height:
        return True
    else:
        return False


colors = ['red', 'blue', 'black', 'green']


class Menu:
    def __init__(self, pos, list, width, height):

        self.x = pos[0]
        self.width = width
        self.height = height
        self.y = pos[1]
        self.variables = list
        self.opened = False
        self.flag = True
        self.choice = 0

    def menu(self):

        if (not self.opened) and check_position(self.x, self.y, self.width, self.height) \
                and pygame.mouse.get_pressed()[0]:
            self.opened = True
            self.flag = False

        if not pygame.mouse.get_pressed()[0]:
            self.flag = True

        if self.opened and self.flag:
            for number, choice in enumerate(self.variables):
                stroke = [self.x, self.y + self.height * number, choice]
                if check_position(stroke[0], stroke[1], self.width, self.height):
                    if pygame.mouse.get_pressed()[0]:
                        self.opened = False
                        self.choice = number

    def draw(self, screen):

        if self.opened is False:
            pygame.draw.rect(screen, interface, (self.x, self.y, self.width, self.height))
            text = text_preset.render('Menu', True, text_color)
            screen.blit(text, (self.x + 5, self.y + 5))

        else:
            for number, choice in enumerate(self.variables):
                stroke = [self.x, self.y + self.height * number, choice]

                pygame.draw.rect(screen, interface, (stroke[0], stroke[1], self.width, self.height))
                pygame.draw.rect(screen, choice, (stroke[0] + 200, stroke[1] + 10, 22, 22))
                text = text_preset.render(choice.capitalize(), True, choice)
                screen.blit(text, (self.x + 12, stroke[1] + 5))


class Slider:
    def __init__(self, coord, lenght, max_value, start_value, minimal_value):

        self.minimal_value = minimal_value
        self.max_value = max_value
        self.x = coord[0]
        self.y = coord[1]
        self.current_value = self.minimal_value
        self.lenght = lenght
        self.s_height = 21
        self.s_width = DisplayConstants.AXIS_OFFSET
        self.s_x = self.x + 0
        self.s_y = self.y - self.s_height // 2
        self.flag = False
        self.new_posx = None
        self.value = start_value

    def slide(self, value=None):

        if value is not None:
            self.s_x = (self.lenght * value) / self.max_value + self.x
            self.value = value

        if not self.flag:
            if pygame.mouse.get_pressed()[0] and self.s_x < pygame.mouse.get_pos()[0] < self.s_x + self.s_width \
                    and self.s_y < pygame.mouse.get_pos()[1] < self.s_y + self.s_height:
                self.new_posx = pygame.mouse.get_pos()[0] + 0
                new_posy = pygame.mouse.get_pos()[1]
                self.flag = True

        elif self.flag is True:

            self.s_x = self.s_x + (pygame.mouse.get_pos()[0] - self.new_posx)

            if self.s_x > self.x + self.lenght:
                self.s_x = self.x + self.lenght
            if self.s_x < self.x:
                self.s_x = self.x

            self.value = (self.s_x - self.x) / (
                    self.lenght / (self.max_value - self.minimal_value)) + self.minimal_value
            self.new_posx = pygame.mouse.get_pos()[0]
            if not pygame.mouse.get_pressed()[0]:
                self.flag = False

        print(self.value)
        return self.value

    def draw(self, screen):
        pygame.draw.line(screen, 'black', (self.x, self.y), (self.x + self.lenght, self.y), DisplayConstants.LINE_WIDTH)
        pygame.draw.rect(screen, 'white', ((self.s_x, self.s_y), (self.s_width, self.s_height)))


angle_slider = Slider([50, DisplayConstants.AXIS_OFFSET], 700, (math.pi / 2), 0, 0)
graphics = []
for color in colors:
    graphics.append(Graphic((DisplayConstants.AXIS_OFFSET, 780), int(input('Введите начальную скорость')), 0.5, color))
scale_slider = Slider([50, 50], 700, 1000, 1500, 1)
color_menu = Menu((700, 200), colors, 250, 40)

scale = 800
scale = scale_slider.slide(scale)
while True:

    screen.fill(fon)
    color_menu.menu()
    choice = color_menu.choice
    scale = scale_slider.slide()
    scale_slider.draw(screen)
    scale = scale_slider.slide()
    a_angle = angle_slider.slide(graphics[choice].calculator.a_angle)
    print('angle =', a_angle)

    # Используем новый предсказуемый метод
    success = graphics[choice].calculate_and_update_trajectory(a_angle)
    if not success:
        print("Не удалось рассчитать траекторию")

    color_menu.draw(screen)

    for graphic_p, main_stats in zip(graphics, range(200, 1000, 100)):
        graphic_p.draw(screen, scale, (main_stats, 200))

    angle_slider.draw(screen)
    pygame.display.flip()

    event = pygame.event.get()

    pygame.event.pump()
    clock.tick(10)