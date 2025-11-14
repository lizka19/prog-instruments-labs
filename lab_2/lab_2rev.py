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


class Graphic:

    def __init__(self, start_pos, start_speed, time, color):

        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.x = 0
        self.y = 0
        self.v_0 = start_speed
        self.coords = []
        self.color = color
        self.a_angle = None
        self.s = 0
        self.h = 0

    def graphic(self, a_angle):

        self.coords = []
        t = 0
        self.s = self.v_0 ** 2 * math.sin(2 * a_angle) / PhysicsConstants.GRAVITY
        print('s =', self.s)
        self.h = self.v_0 ** 2 * math.sin(a_angle) ** 2 / (2 * PhysicsConstants.GRAVITY)
        print('h =', self.h)
        self.a_angle = a_angle

        while True:

            self.x = (self.v_0 * math.cos(a_angle) * t)
            self.y = -(self.x * math.tan(a_angle) - self.x ** 2 * (PhysicsConstants.GRAVITY / (2 * self.v_0 ** 2 * math.cos(a_angle) ** 2)))
            self.x = self.x
            self.coords.append((self.x, self.y))
            t += PhysicsConstants.TIME_STEP

            if self.y + self.start_y > self.start_y + 0.001:
                break

    def draw(self, screen, scale, main_stats):
        for num in range(len(self.coords) - 1):
            pygame.draw.line(screen, self.color,
                             (self.coords[num][0] * scale + self.start_x, self.coords[num][1] * scale + self.start_y),
                             (self.coords[num + 1][0] * scale + self.start_x,
                              self.coords[num + 1][1] * scale + self.start_y), DisplayConstants.LINE_WIDTH)

        for serif, text in zip(range(self.start_y, 200, -DisplayConstants.SERIF_SPACING), range(0, self.start_y, DisplayConstants.SERIF_SPACING)):
            pygame.draw.line(screen, 'blue', (self.start_x - 2, serif), (self.start_x + 2, serif))
            text = text_preset_mini.render('{:<03.2f}'.format(text / scale), True, 'black')
            screen.blit(text, (self.start_x - DisplayConstants.AXIS_OFFSET, serif))

        for serif_1, text_1 in zip(range(self.start_x, 800, DisplayConstants.SERIF_SPACING), range(0, self.start_x + 1000, DisplayConstants.SERIF_SPACING)):
            text_1 = text_preset_mini.render('{:<03.2f}'.format(text_1 / scale), True, 'black')
            screen.blit(text_1, (serif_1, self.start_y + 10))
            pygame.draw.line(screen, 'blue', (serif_1, self.start_y - 2), (serif_1, self.start_y + 2))

        text = text_preset.render(str('{:0<1.2f}'.format(self.s)), True, self.color)
        screen.blit(text, main_stats)
        text = text_preset.render(str('{:0<1.2f}'.format(self.h)), True, self.color)
        screen.blit(text, (main_stats[0], main_stats[1] + 50))

        pygame.draw.line(screen, 'blue', (self.start_x, self.start_y), (self.start_x, 200))
        pygame.draw.line(screen, 'blue', (self.start_x, self.start_y), (800, self.start_y))

        pygame.draw.line(screen, self.color, (self.start_x - 2, -self.h * scale + self.start_y),
                         (self.start_x + 2, -self.h * scale + self.start_y), DisplayConstants.LINE_WIDTH)
        text = text_preset_mini.render(str(round(self.h, 2)), True, self.color)
        screen.blit(text, (self.start_x + 10, -self.h * scale + self.start_y))

        pygame.draw.line(screen, self.color, (self.s * scale + self.start_x, self.start_y - 2),
                         (self.s * scale + self.start_x, self.start_y + 2), DisplayConstants.LINE_WIDTH)
        text = text_preset_mini.render(str(round(self.s, 2)), True, self.color)
        screen.blit(text, (self.s * scale + self.start_x, self.start_y - 15))


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
menushka = Menu((700, 200), colors, 250, 40)

scale = 800
scale = scale_slider.slide(scale)
while True:

    screen.fill(fon)
    menushka.menu()
    choice = menushka.choice
    scale = scale_slider.slide()
    scale_slider.draw(screen)
    scale = scale_slider.slide()
    a_angle = angle_slider.slide(graphics[choice].a_angle)
    print('angle =', a_angle)
    graphics[choice].graphic(a_angle)

    menushka.draw(screen)

    for graphic_p, main_stats in zip(graphics, range(200, 1000, 100)):
        graphic_p.draw(screen, scale, (main_stats, 200))

    angle_slider.draw(screen)
    pygame.display.flip()

    event = pygame.event.get()

    pygame.event.pump()
    clock.tick(10)