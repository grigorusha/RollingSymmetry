# Импортируем библиотеку pygame
import pygame
from pygame import *

import pygame_widgets
from pygame_widgets.button import Button

import random
import math
import copy

import webbrowser
from tkinter import Tk
from tkinter import filedialog as fd
import os

# Объявляем базовые переменные
SIZE_X_START = 13
SIZE_Y_START = 5
SIZE_X = SIZE_X_START
SIZE_Y = SIZE_Y_START

TG60 = math.sqrt(3)
TG30 = TG60/3
PANEL = 35*2

EDGE_PYRAMID = 60
HEIGHT_PYRAMID = int(EDGE_PYRAMID*TG60/2)
RADIUS = int(EDGE_PYRAMID/2.05)
BORDER = 15

HEIGHT_3D_PYRAMID = int(EDGE_PYRAMID*math.sqrt(6)/3)

EDGEka = int(RADIUS*0.8)
EDGE_PYRAMIDka = int(EDGE_PYRAMID+2*EDGEka*TG60)
HEIGHT_PYRAMIDka = HEIGHT_PYRAMID+EDGEka*3

BORDERka = int(RADIUS*1.2)
BORDERe = int(BORDERka*TG60*2/3)

BACKGROUND_COLOR = "#000000"
GRAY_COLOR = "#808080"
GRAY_COLOR2 = "#C0CCB0"
RED_COLOR = "#FF0000"
PYRAMID_COLOR = [("W","#FFFFFF"),("B","#0000FF"),("R","#FF0000"),("G","#008000")]
GRADIENT_COLOR = [ [(255, 255, 255, 255), (120, 120, 120, 255)], [(000, 000, 255, 255), (0, 0, 100, 255)],
                   [(255, 0, 0, 255), (100, 0, 0, 255)], [(000, 255, 000, 255), (0, 0, 150, 255)],
                   [(250, 250, 0, 255), (150, 150, 0, 255)], [(250, 0, 250, 255), (150, 0, 150, 255)]]

level = []
solved_level = []
filename = ""

BTN_CLICK = False
BTN_CLICK_STR = ""

def init_level(y,x):
    level = []
    for ny in range(y):
        str = []
        for nx in range(x):
            str.append(0)
        level.append(str)

    level = [ [9,9,0,1,0,0,3,0,0,1,0,9,9],
              [9,2,0,0,0,0,0,0,0,0,0,2,9],
              [0,0,0,0,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,1,0,0,0,1,0,0,0,1],
              [9,0,3,0,0,0,2,0,0,0,3,0,9] ]

    solved_level = copy.deepcopy(level)
    return level,solved_level

def button_Button_click(button_str):
    global BTN_CLICK, BTN_CLICK_STR
    BTN_CLICK_STR = button_str
    BTN_CLICK = True

def button_Size_click(y,x):
    global SIZE_X,SIZE_Y,BTN_CLICK, BTN_CLICK_STR
    if (SIZE_X>3)and(x<0):
        SIZE_X = SIZE_X + x
        BTN_CLICK_STR = "minusx"
    if (SIZE_X<9)and(x>0):
        SIZE_X = SIZE_X + x
        BTN_CLICK_STR = "plusx"
    if (SIZE_Y>2)and(y<0):
        SIZE_Y = SIZE_Y + y
        BTN_CLICK_STR = "minusy"
    if (SIZE_Y<8)and(y>0):
        SIZE_Y = SIZE_Y + y
        BTN_CLICK_STR = "plusy"
    BTN_CLICK = True

def ret_cell(level, y, x):
    if (0 <= y < SIZE_Y) and (0 <= x < SIZE_X):
        if level[y][x] == 0:
            return 0
        elif level[y][x] < 9:
            return level[y][x]
    return -1

def pyram_find_empty(level, y, x):

    def ret_area(level, pos_mas):
        for pos in pos_mas:
            cell = ret_cell(level,pos[0],pos[1])
            if cell > 0:
                return 1
        if level[pos_mas[0][0]][pos_mas[0][1]] == 0:
            return 0
        return -1

    pyram_epty = []
    orient = (y % 2 == 0) == (x % 2 == 0)  # уголок вверх

    if orient: # уголок вверх
        if y < SIZE_Y - 1:
            area = ret_area(level, ((y+1,x),(y+2,x),(y+1,x+1),(y+2,x+1),(y+1,x-1),(y+2,x-1)))
            if (area == 0):
                pyram_epty.append((y+1, x, 1))
        if x > 0:
            area = ret_area(level, ((y,x-1),(y,x-2),(y,x-3),(y-1,x-1),(y-1,x-2),(y-1,x-3)))
            if (area == 0):
                pyram_epty.append((y, x - 1, 2))
        if x < SIZE_X-1:
            area = ret_area(level, ((y,x+1),(y,x+2),(y,x+3),(y-1,x+1),(y-1,x+2),(y-1,x+3)))
            if (area == 0):
                pyram_epty.append((y, x + 1, 3))

    else:  # уголок вниз
        if y > 0:
            area = ret_area(level, ((y-1,x),(y-2,x),(y-1,x+1),(y-2,x+1),(y-1,x-1),(y-2,x-1)))
            if (area == 0):
                pyram_epty.append((y-1, x, 1))
        if x > 0:
            area = ret_area(level, ((y,x-1),(y,x-2),(y,x-3),(y+1,x-1),(y+1,x-2),(y+1,x-3)))
            if (area == 0):
                pyram_epty.append((y, x - 1, 2))
        if x < SIZE_X-1:
            area = ret_area(level, ((y,x+1),(y,x+2),(y,x+3),(y+1,x+1),(y+1,x+2),(y+1,x+3)))
            if (area == 0):
                pyram_epty.append((y, x + 1, 3))

    return pyram_epty

def gradient_circle(radius, startcolor, endcolor, cir, inv, offset=(0, 0)):
    diameter = radius * 2
    bigSurf = pygame.Surface((diameter, diameter)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / diameter
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm, gm, bm, am = (er - sr) * dd, (eg - sg) * dd, (eb - sb) * dd, (ea - sa) * dd

    draw_circle = pygame.draw.circle
    for rad in range(diameter, 0, -1):
        draw_circle(bigSurf, (er + int(rm * rad), eg + int(gm * rad), eb + int(bm * rad), ea + int(am * rad)),
                    (radius + inv*offset[0], radius + inv*offset[1]), rad, 2)

    for rad in range(radius, diameter, 1):
        draw_circle(bigSurf, (0, 0, 0, 0), (radius, radius), rad, 2)

    if cir:
        draw_circle(bigSurf, (0, 0, 0, 255), (radius, radius), radius, 2)

    return bigSurf

def read_file(fl):
    global filename

    if fl or filename=="":
        dir = os.path.abspath(os.curdir)
        filetypes = (("Text file", "*.txt"),("Any file", "*"))
        filename = fd.askopenfilename(title="Open Level", initialdir=dir,filetypes=filetypes)
        if filename=="":
            return ""

    x = y = 0
    level = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for nom,str in enumerate(lines):
            str = str.replace('\n','')
            str = str.strip()
            if str == "": break

            str_mas = []
            while len(str)>=1:
                sim = str[0]
                str = str[1:]
                str_mas.append(int(sim))
            level.append(str_mas)
            y += 1
            x = max(x,len(str_mas))
    return level, y, x

def save_file(level):
    dir = os.path.abspath(os.curdir)
    filetypes = (("Text file", "*.txt"),("Any file", "*"))
    filename = fd.asksaveasfile("w", title="Save Level as...", initialdir=dir,filetypes=filetypes)
    if filename==None:
        return ""

    with open(filename.name, 'w') as f:
        for string in level:
            line = ""
            for pyr in string:
                line += str(pyr)
            f.write(line+"\n")

def coordinate_calc(ny, nx, SHIFT=0):
    BORD = BORDER + RADIUS
    orient = (ny % 2 == 0) == (nx % 2 == 0)  # уголок вверх
    fl_or = 1 if orient else -1
    fl_y = 0 if orient else 1
    # x1,y1 - вершина, x2,yy и x3,yy - основание, x1,y0 - центр
    if (nx % 2 == 0):  # 1 ряд, наверх или 2 ряд, вниз
        x1 = ((nx+1)*EDGE_PYRAMID)//2 + BORD
    else:  # 2 ряд, наверх или 1 ряд, вниз
        x1 = ((nx+2)//2)*EDGE_PYRAMID + BORD

    y1 = (ny+fl_y) * HEIGHT_PYRAMID + BORD
    yy = y1 + HEIGHT_PYRAMID * fl_or

    if SHIFT==0:
        y0 = y1 + int(2 * HEIGHT_PYRAMID / 3) * fl_or
        x2 = x1 + int(EDGE_PYRAMID / 2) * fl_or
        x3 = x1 - int(EDGE_PYRAMID / 2) * fl_or
        if orient:
            x2,x3=x3,x2
        return x1, y1, x2, x3, yy, y0
    else:
        SHIFTka = int(EDGE_PYRAMID + 2*SHIFT * TG60)

        x1_grid = x1
        y1_grid = y1 - SHIFT*2 * fl_or
        yy_grid = yy + SHIFT * fl_or
        x2_grid = x1 + int(SHIFTka / 2) * fl_or
        x3_grid = x1 - int(SHIFTka / 2) * fl_or
        return x1_grid, y1_grid, x2_grid, x3_grid, yy_grid

def rotate_point_around_line(point, angle_deg, line_point1, line_point2):
    if point == line_point1 or point == line_point2:
        return point

    angle_rad = math.radians(angle_deg)

    # Разбираем вершину и точки прямой
    x, y, z = point
    x1, y1, z1 = line_point1
    x2, y2, z2 = line_point2

    # Вычисляем вектор направления прямой (по условию z1=z2=0)
    dx = x2 - x1
    dy = y2 - y1

    # Нормализуем вектор направления
    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
        dx /= length
        dy /= length

    # Переносим точку в систему координат, где прямая проходит через начало координат
    x -= x1
    y -= y1

    # Поворачиваем систему координат так, чтобы прямая совпала с осью X
    # (это эквивалентно повороту на угол -angle_y, где angle_y - угол между прямой и осью X)
    angle_y = math.atan2(dy, dx)
    cos_y = math.cos(-angle_y)
    sin_y = math.sin(-angle_y)

    # Поворот системы координат (эквивалентно повороту точки в обратную сторону)
    new_x = x * cos_y - y * sin_y
    new_y = x * sin_y + y * cos_y
    z = z  # z не меняется

    # Теперь выполняем поворот вокруг оси X (так как прямая теперь совпадает с осью X)
    new_y_rot = new_y * math.cos(angle_rad) - z * math.sin(angle_rad)
    new_z_rot = new_y * math.sin(angle_rad) + z * math.cos(angle_rad)

    # Возвращаем систему координат в исходное положение
    # 1. Обратный поворот от оси X к исходной прямой
    cos_y_rev = math.cos(angle_y)
    sin_y_rev = math.sin(angle_y)

    final_x = new_x * cos_y_rev - new_y_rot * sin_y_rev
    final_y = new_x * sin_y_rev + new_y_rot * cos_y_rev
    final_z = new_z_rot

    # Возвращаем точку в исходную позицию (отмена переноса)
    final_x += x1
    final_y += y1

    return (final_x,final_y,final_z)

def main():
    global SIZE_X,SIZE_Y, BTN_CLICK,BTN_CLICK_STR, filename

    # основные константы
    SIZE_X = SIZE_X_START
    SIZE_Y = SIZE_Y_START
    offset = (-int(RADIUS/3), -int(RADIUS/3))
    file_ext = False

    # основная инициализация
    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    font_button = pygame.font.SysFont("ArialB",18)
    timer = pygame.time.Clock()
    Tk().withdraw()

    icon = os.path.join(os.path.abspath(os.curdir),"Rolling Symmetry.png")
    if os.path.isfile(icon):
        pygame.display.set_icon(pygame.image.load(icon))

    ################################################################################
    ################################################################################
    # перезапуск программы при смене параметров
    while True:
        # дополнительные константы
        WIN_WIDTH = int(EDGE_PYRAMID * (SIZE_X/2+0.5))+BORDER*2+RADIUS*2  # Ширина создаваемого окна
        WIN_HEIGHT = SIZE_Y * HEIGHT_PYRAMID+BORDER*2+RADIUS*2  # Высота

        if file_ext:
            # file_ext = False
            solved_level = []
        else:
            level,solved_level = init_level(SIZE_Y, SIZE_X)

        scramble_move = 0
        moves_stack = []
        moves = 0
        solved = True
        animation_on = False
        rotation_angle = 0  # Текущий угол поворота
        finish_angle = math.degrees(math.acos(-1/3)) # 1.91063323617 - угол поворота пирамидки.
        rotation_speed = finish_angle/5  # Скорость вращения в градусах за кадр

        # инициализация окна
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT+PANEL))  # Создаем окошко
        pygame.display.set_caption("Rolling Symmetry")  # Пишем в шапку
        screen.fill(BACKGROUND_COLOR) # Заливаем поверхность сплошным цветом

        # инициализация окна с подсказкой
        GAME = (WIN_WIDTH, WIN_HEIGHT)
        game_scr = Surface(GAME)
        HELP = (WIN_WIDTH//3, WIN_HEIGHT//3)

        help = False
        help_gen = True

        # инициализация кнопок
        if True:
            button_y1 = WIN_HEIGHT + 10 + 10
            button_Reset = Button(screen, 10, button_y1, 45, 20, text='Reset', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("reset"))
            button_Scramble = Button(screen, button_Reset.textRect.right+10, button_y1, 70, 20, text='Scramble', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("scramble"))
            button_Undo = Button(screen, button_Scramble.textRect.right+10, button_y1, 40, 20, text='Undo', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("undo"))

            button_Open = Button(screen, button_Undo.textRect.right+20, button_y1, 45, 20, text='Open', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("open"))
            button_Save = Button(screen, button_Open.textRect.right+10, button_y1, 45, 20, text='Save', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("save"))

            button_About = Button(screen, button_Save.textRect.right+20, button_y1, 60, 20, text='About ->', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#0000FF", hoverColour="#0000FF", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("about"))

            button_y2 = button_y1 + 25
            button_Help = Button(screen, 10, button_y2, 80, 20, text='Solved State', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("help"))
            button_y2 += 4

        button_set = [button_Reset, button_Scramble, button_Undo, button_Open, button_Save, button_About, button_Help]

        ################################################################################
        ################################################################################
        # Основной цикл программы
        while True:
            if not animation_on:

                mouse_x = mouse_y = face = 0
                pyramid_pos_x = pyramid_pos_y = -1
                pyramid_pos_x_pred = pyramid_pos_y_pred = -1
                undo = False

                ################################################################################
                # обработка событий
                if scramble_move == 0:
                    events = pygame.event.get()
                    for ev in events:  # Обрабатываем события
                        if (ev.type == QUIT):
                            return SystemExit, "QUIT"
                        if (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                            help = False if help else help
                        if (ev.type == KEYDOWN and ev.key == K_F1):
                            BTN_CLICK = True
                            BTN_CLICK_STR = "help"
                        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                            if not help:
                                mouse_x = ev.pos[0]
                                mouse_y = ev.pos[1]
                            help = False if help else help
                        if ev.type == MOUSEBUTTONDOWN and ev.button == 5:
                            BTN_CLICK = True
                            BTN_CLICK_STR = "undo"

                    ################################################################################
                    # обработка нажатия на кнопки
                    if BTN_CLICK:
                        fl_break = True
                        if BTN_CLICK_STR=="reset" and not help:
                            if not file_ext:
                                fl_break = True
                                SIZE_X, SIZE_Y = SIZE_X_START, SIZE_Y_START
                            else:
                                fl_break = False
                                fil = read_file(False)
                                if fil != "":
                                    fl_break = True
                                    level, SIZE_Y, SIZE_X = fil
                                    file_ext = True
                        if BTN_CLICK_STR=="scramble" and not help:
                            fl_break = False
                            scramble_move = SIZE_X * SIZE_Y * 200
                            pos_pred = (0, 0)
                        if BTN_CLICK_STR=="undo":
                            fl_break = False
                            if len(moves_stack) > 0:
                                vek,face,pyramid_pos_y,pyramid_pos_x = moves_stack.pop()
                                vek = (vek + 1) % 4 + 1
                                if face>1: face = 5-face
                                moves -= 1
                                undo = True
                        if BTN_CLICK_STR=="open":
                            fl_break = False
                            fil = read_file(True)
                            if fil != "":
                                fl_break = True
                                level, SIZE_Y, SIZE_X = fil
                                file_ext = True
                        if BTN_CLICK_STR=="save":
                            fl_break = False
                            save_file(level)

                        if BTN_CLICK_STR=="about":
                            fl_break = False
                            webbrowser.open("https://github.com/grigorusha/RollingSymmetry", new=2, autoraise=True)
                            webbrowser.open("https://twistypuzzles.com/forum/viewtopic.php?t=38581", new=2, autoraise=True)
                            webbrowser.open("https://twistypuzzles.com/forum/viewtopic.php?p=421131#p421131", new=2, autoraise=True)
                        if BTN_CLICK_STR=="help":
                            fl_break = False
                            help = not help

                        BTN_CLICK = False
                        BTN_CLICK_STR = ""
                        if fl_break: break
                else:
                    # обработка рандома для Скрамбла - ищем пирамидку, которую можно повернуть
                    pyram_mas = []
                    for ny, row in enumerate(level):
                        for nx, pyramid in enumerate(row):
                            if 0 < pyramid < 9:
                                pyram_empty = pyram_find_empty(level, ny, nx)
                                if len(pyram_empty) > 0:
                                    pyram_mas.append([ny,nx])

                    while True:
                        pos = random.randint(0, len(pyram_mas) - 1)
                        if pos_pred == (0,0) or pos_pred != pyram_mas[pos]:
                            break
                    pos_pred = (pyramid_pos_y, pyramid_pos_x)
                    pyramid_pos_y, pyramid_pos_x = pyram_mas[pos]
                    pyram_empty = pyram_find_empty(level, pyramid_pos_y, pyramid_pos_x)
                    len_p = len(pyram_empty)
                    if len_p>0:
                        vek = random.randint(0,len_p-1)
                        face = pyram_empty[vek][2]

                ################################################################################
                # обработка нажатия на пирамидки в игровом поле

                if mouse_x+mouse_y > 0 and not help:
                    fl_stop = False
                    for ny, row in enumerate(level):
                        for nx,pyramid in enumerate(row):
                            if 0<pyramid<9:
                                orient = (ny % 2 == 0) == (nx % 2 == 0) # уголок вверх

                                ############################################
                                # расчет всех координат
                                # x1,y1 - вершина, x2,yy и x3,yy - основание, x1,y0 - центр
                                x1_grid,y1_grid,x2_grid,x3_grid,yy_grid = coordinate_calc(ny, nx, EDGEka)

                                x0 = abs(x2_grid-x3_grid)//2
                                if orient and x3_grid<mouse_x<x2_grid and y1_grid<mouse_y<yy_grid: # в прямоугольнике, вверх
                                    xx,yy = mouse_x-x3_grid, HEIGHT_PYRAMIDka-(mouse_y-y1_grid)
                                elif not orient and x2_grid<mouse_x<x3_grid and yy_grid<mouse_y<y1_grid: # в прямоугольнике
                                    xx,yy = mouse_x-x2_grid, mouse_y-yy_grid
                                else: continue

                                xm = EDGE_PYRAMIDka-xx
                                tg1 = yy if xx==0 else yy/xx
                                tg2 = yy if xm==0 else yy/xm

                                tg11 = yy if xx==0 else (HEIGHT_PYRAMIDka-yy)/xx
                                tg22 = yy if xm==0 else (HEIGHT_PYRAMIDka-yy)/xm

                                if not ( (xx < x0 and tg1 < TG60) or (xx >= x0 and tg2 < TG60) ):
                                    continue
                                pyramid_pos_x = nx
                                pyramid_pos_y = ny
                                if pyramid_pos_x >= SIZE_X: pyramid_pos_x = -1

                                if (xx < x0 and tg1 < TG30) or (xx >= x0 and tg2 < TG30):
                                    face = 1
                                elif (xx < x0):
                                    face = 2
                                else:
                                    face = 3

                                fl_stop = True
                                break
                        if fl_stop: break

                ################################################################################
                ################################################################################
                # логика игры - выполнение перемещений
                if (pyramid_pos_x>=0) and (pyramid_pos_y>=0):
                    pyram = level[pyramid_pos_y][pyramid_pos_x]
                    if pyram > 0 and pyram < 9:
                        pyram_empty = pyram_find_empty(level, pyramid_pos_y, pyramid_pos_x)
                        if len(pyram_empty) > 0:
                            if len(pyram_empty)==1:
                                pos = 0
                                face = 0
                                vek = pyram_empty[0][2]
                            else:
                                vek = 0
                                for pos,epmty_pos in enumerate(pyram_empty):
                                    if epmty_pos[2] == face:
                                        vek = face
                                        break

                            if vek != 0:
                                pyramid_pos_y_pred, pyramid_pos_x_pred = pyram_empty[pos][0], pyram_empty[pos][1]

                                level[pyram_empty[pos][0]][pyram_empty[pos][1]] = pyram
                                level[pyramid_pos_y][pyramid_pos_x] = 0

                                if not undo:
                                    moves += 1
                                    moves_stack.append([vek,pyram_empty[pos][2],pyram_empty[pos][0],pyram_empty[pos][1]])

                                if scramble_move == 0:
                                    animation_on = True

                if scramble_move != 0:
                    scramble_move -= 1
                    moves_stack = []
                    moves = 0
                    continue
                    # отрисовка не нужна

                # проверка на решенное состояние
                solved = True
                if solved_level != level:
                    solved = False

            else:
                pass

            ################################################################################
            ################################################################################

            if not animation_on:
                # отрисовка игрового поля
                screen.fill(BACKGROUND_COLOR)

                pf = Surface((WIN_WIDTH, WIN_HEIGHT))
                pf.fill(Color(GRAY_COLOR))
                screen.blit(pf, (0, 0))
                pf = Surface((WIN_WIDTH, 10))
                pf.fill(Color("#B88800"))
                screen.blit(pf, (0, WIN_HEIGHT))

                ################################################################################
                # text
                # screen.blit(textx, textx_place)
                # screen.blit(texty, texty_place)

                text_moves = font.render('Moves: ' + str(moves), True, PYRAMID_COLOR[2][1])
                text_moves_place = text_moves.get_rect(topleft=(button_Help.textRect.right+20, button_y2-7))
                screen.blit(text_moves, text_moves_place)
                if solved:
                    text_solved = font.render('Solved', True, PYRAMID_COLOR[0][1])
                else:
                    text_solved = font.render('not solved', True, RED_COLOR)
                text_solved_place = text_solved.get_rect(topleft=(text_moves_place.right + 10, button_y2-7))
                screen.blit(text_solved, text_solved_place)

            ############################################
            # отрисовка сетки и пирамидок
            game_scr.fill(Color(GRAY_COLOR))
            for type_obj in range(4):
                for ny, row in enumerate(level):
                    for nx,pyramid in enumerate(row):
                        if animation_on and type_obj == 2:
                            if ( (pyramid_pos_x == nx) and (pyramid_pos_y == ny) ) or ( (pyramid_pos_x_pred == nx) and (pyramid_pos_y_pred == ny) ): continue

                        orient = (ny % 2 == 0) == (nx % 2 == 0) # уголок вверх

                        ############################################
                        # расчет всех координат

                        # x1,y1 - вершина, x2,yy и x3,yy - основание, x1,y0 - центр
                        x1,y1,x2,x3,yy,y0 = coordinate_calc(ny, nx)
                        x1_grid, y1_grid, x2_grid, x3_grid, yy_grid = coordinate_calc(ny, nx, BORDERka)

                        ############################################
                        # отрисовка границ
                        if type_obj == 0 and pyramid != 9:
                            if orient:  # уголок вверх
                                cell = ret_cell(level, ny, nx-1)
                                if cell==-1 or cell==9:
                                    draw.line(game_scr, GRAY_COLOR2, [x1_grid-BORDERe//2, y1_grid+BORDERka], [x3_grid+BORDERe//2, yy_grid-BORDERka], 2)
                                cell = ret_cell(level, ny, nx+1)
                                if cell == -1 or cell == 9:
                                    draw.line(game_scr, GRAY_COLOR2, [x1_grid+BORDERe//2, y1_grid+BORDERka], [x2_grid-BORDERe//2, yy_grid-BORDERka], 2)
                                cell = ret_cell(level, ny + 1, nx)
                                if cell == -1 or cell == 9:
                                    draw.line(game_scr, GRAY_COLOR2, [x2_grid-BORDERe, yy_grid],[x3_grid+BORDERe, yy_grid], 2)
                            else:  # уголок вниз
                                cell = ret_cell(level, ny, nx-1)
                                if cell==-1 or cell==9:
                                    draw.line(game_scr, GRAY_COLOR2, [x1_grid-BORDERe//2, y1_grid-BORDERka], [x2_grid+BORDERe//2, yy_grid+BORDERka], 2)
                                cell = ret_cell(level, ny, nx+1)
                                if cell == -1 or cell == 9:
                                    draw.line(game_scr, GRAY_COLOR2, [x1_grid+BORDERe//2, y1_grid-BORDERka], [x3_grid-BORDERe//2, yy_grid+BORDERka], 2)
                                cell = ret_cell(level, ny-1, nx)
                                if cell==-1 or cell==9:
                                    draw.line(game_scr, GRAY_COLOR2, [x2_grid+BORDERe, yy_grid],[x3_grid-BORDERe, yy_grid], 2)

                        # # отрисовка точек
                        # if type_obj == 0 and pyramid == 9:
                        #     draw.circle(game_scr, GRAY_COLOR2, (x1, y1), 3)
                        #     draw.circle(game_scr, GRAY_COLOR2, (x2, yy), 3)
                        #     draw.circle(game_scr, GRAY_COLOR2, (x3, yy), 3)

                        # отрисовка лунок
                        if type_obj == 1 and pyramid == 0:
                            RAD = int(RADIUS / 1.4)
                            scol, ecol = (160, 160, 160, 255), (120, 120, 120, 255)
                            game_scr.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x1-RAD, y1-RAD))
                            game_scr.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x2-RAD, yy-RAD))
                            game_scr.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x3-RAD, yy-RAD))

                        # отрисовка пирамидок
                        if type_obj == 2 and pyramid > 0 and pyramid < 9:  # пирамидка
                            scol,ecol = GRADIENT_COLOR[pyramid-1]
                            game_scr.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x1-RADIUS, y1-RADIUS))
                            game_scr.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x2-RADIUS, yy-RADIUS))
                            game_scr.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x3-RADIUS, yy-RADIUS))
                            game_scr.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x1-RADIUS, y0-RADIUS))

                        # if type_obj == 3 and pyramid > 0 and pyramid < 9:  # сетка для отладки
                        #     x1_grid,y1_grid,x2_grid,x3_grid,yy_grid = coordinate_calc(ny, nx, BORDERka)
                        #     draw.line(game_scr, GRAY_COLOR2, [x1_grid, y1_grid], [x2_grid, yy_grid], 2)
                        #     draw.line(game_scr, GRAY_COLOR2, [x1_grid, y1_grid], [x3_grid, yy_grid], 2)
                        #     draw.line(game_scr, GRAY_COLOR2, [x2_grid, yy_grid], [x3_grid, yy_grid], 2)

            if animation_on:
                # цикл Анимации

                if rotation_angle==0:
                    ny,nx = pyramid_pos_y,pyramid_pos_x
                    orient = (ny % 2 == 0) == (nx % 2 == 0)  # уголок вверх

                    ############################################
                    # расчет всех координат

                    # x1,y1 - вершина, x2,yy и x3,yy - основание, x1,y0 - центр, hh - высота 3д пирамидки
                    x1, y1, x2, x3, yy, y0 = coordinate_calc(ny, nx)
                    hh = HEIGHT_3D_PYRAMID

                    if vek==1:
                        line_p1, line_p2 = [x2,yy,0],[x3,yy,0]
                        mul = 1 if not orient else -1
                    elif vek==2:
                        line_p1, line_p2 = [x2,yy,0],[x1,y1,0]
                        mul = 1 if orient else -1
                    elif vek==3:
                        line_p1, line_p2 = [x3,yy,0],[x1,y1,0]
                        mul = 1 if not orient else -1
                    initial_pyramid_vertices = [[x2,yy,0],[x3,yy,0],[x1,y1,0],[x1,y0,hh]]
                    pass
                pyramid = level[pyramid_pos_y_pred][pyramid_pos_x_pred]

                ############################################
                # запуск вращения

                # Обновление угла поворота
                rotation_angle += rotation_speed

                rotated_pyramid_vertices = []
                for point in initial_pyramid_vertices:
                    rotated_vertex = rotate_point_around_line(point, mul * rotation_angle, line_p1, line_p2)
                    rotated_pyramid_vertices.append(rotated_vertex)
                rotated_pyramid_vertices.sort(key=lambda par: (par[2]))

                for vertex in rotated_pyramid_vertices:
                    xx,yy,zz = vertex
                    scol, ecol = GRADIENT_COLOR[pyramid - 1]
                    game_scr.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (xx - RADIUS, yy - RADIUS))

                if rotation_angle>=finish_angle:
                    animation_on = False
                    rotation_angle = 0

            screen.blit(game_scr, (0, 0))

            # окно помощи
            if help_gen:
                help_gen = False
                help_screen = pygame.transform.scale(game_scr, HELP)
            if help:
                screen.blit(help_screen, (GAME[0]-HELP[0]-BORDER//3,BORDER//3))
                draw.rect(screen, Color("#B88800"), (GAME[0]-HELP[0]-2*(BORDER//3), 0, HELP[0]+2*(BORDER//3), HELP[1]+2*(BORDER//3)), BORDER // 3)

            #####################################################################################
            pygame_widgets.update(events)
            pygame.display.update()  # обновление и вывод всех изменений на экран
            timer.tick(60)

        # удаляем кнопки
        for btn in button_set:
            btn.hide()

main()