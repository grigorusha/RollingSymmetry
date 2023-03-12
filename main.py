# Импортируем библиотеку pygame
import pygame
from pygame import *

import pygame_widgets
from pygame_widgets.button import Button

import random
import math
import copy

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
PANEL = 33*2

EDGE_PYRAMID = 60
HEIGHT_PYRAMID = int(EDGE_PYRAMID*TG60/2)
RADIUS = int(EDGE_PYRAMID/2.1)
BORDER = 10

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

def pyram_find_empty(level, y, x):
    def ret_cell(level, y, x):
        if (0 <= y < SIZE_Y) and (0 <= x < SIZE_X):
            if level[y][x] == 0:
                return 0
            elif level[y][x] < 9:
                return level[y][x]
        return -1

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
        if x > 1:
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
        if x > 1:
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

def read_file():
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
            str_mas = []
            while len(str)>=1:
                sim = str[0]
                str = str[2:]
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
                line += str(pyr)+" "
            f.write(line+"\n")

def main():
    global SIZE_X,SIZE_Y, BTN_CLICK,BTN_CLICK_STR

    # основные константы
    SIZE_X = SIZE_X_START
    SIZE_Y = SIZE_Y_START
    offset = (-int(RADIUS/3), -int(RADIUS/3))
    file_ext = False

    # основная инициализация
    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    timer = pygame.time.Clock()
    Tk().withdraw()

    ################################################################################
    ################################################################################
    # перезапуск программы при смене параметров
    while True:
        # дополнительные константы
        WIN_WIDTH = int(EDGE_PYRAMID * (SIZE_X/2+0.5))+BORDER*2+RADIUS*2  # Ширина создаваемого окна
        WIN_HEIGHT = SIZE_Y * HEIGHT_PYRAMID+BORDER*2+RADIUS*2  # Высота

        if file_ext:
            file_ext = False
            solved_level = []
        else:
            level,solved_level = init_level(SIZE_Y, SIZE_X)

        scramble_move = 0
        moves_stack = []
        moves = 0
        solved = True

        # инициализация окна
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT+PANEL))  # Создаем окошко
        pygame.display.set_caption("Rolling Symmetry")  # Пишем в шапку
        screen.fill(BACKGROUND_COLOR) # Заливаем поверхность сплошным цветом

        # инициализация кнопок
        if True:
            button_y1 = WIN_HEIGHT + BORDER + 10
            button_Reset = Button(screen, 10, button_y1, 45, 20, text='Reset', fontSize=20, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("reset"))
            button_Scramble = Button(screen, button_Reset.textRect.right+10, button_y1, 70, 20, text='Scramble', fontSize=20, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("scramble"))
            button_Undo = Button(screen, button_Scramble.textRect.right+10, button_y1, 40, 20, text='Undo', fontSize=20, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("undo"))

            button_Open = Button(screen, button_Undo.textRect.right+20, button_y1, 45, 20, text='Open', fontSize=20, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("open"))
            button_Save = Button(screen, button_Open.textRect.right+10, button_y1, 45, 20, text='Save', fontSize=20, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("save"))

            button_y3 = button_y1 + 30
        button_set = [button_Reset, button_Scramble, button_Undo, button_Open, button_Save] # , button_MinusX, button_PlusX, button_MinusY, button_PlusY

        ################################################################################
        ################################################################################
        # Основной цикл программы
        while True:
            mouse_x = mouse_y = face = 0
            pyramid_pos_x = pyramid_pos_y = -1
            undo = False

            ################################################################################
            # обработка событий
            if scramble_move == 0:
                timer.tick(10)

                events = pygame.event.get()
                for ev in events:  # Обрабатываем события
                    if (ev.type == QUIT) or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                        return SystemExit, "QUIT"
                    if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                        mouse_x = ev.pos[0]
                        mouse_y = ev.pos[1]
                    if ev.type == MOUSEBUTTONDOWN and ev.button == 5:
                        BTN_CLICK = True
                        BTN_CLICK_STR = "undo"

                ################################################################################
                # обработка нажатия на кнопки
                if BTN_CLICK:
                    fl_break = True
                    if BTN_CLICK_STR=="reset":
                        fl_break = True
                    if BTN_CLICK_STR=="scramble":
                        fl_break = False
                        scramble_move = SIZE_X * SIZE_Y * 100
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
                        fil = read_file()
                        if fil != "":
                            fl_break = True
                            level, SIZE_Y, SIZE_X = fil
                            file_ext = True
                    if BTN_CLICK_STR=="save":
                        fl_break = False
                        save_file(level)

                    BTN_CLICK = False
                    BTN_CLICK_STR = ""
                    if fl_break: break
            else:
                # обработка рандома для Скрамбла
                # ищем пирамидку, которую можно повернуть
                pyram_mas = []
                for ny, row in enumerate(level):
                    for nx, pyramid in enumerate(row):
                        if 0 < pyramid < 9:
                            pyram_empty = pyram_find_empty(level, ny, nx)
                            if len(pyram_empty) > 0:
                                pyram_mas.append([ny,nx])

                pos = random.randint(0, len(pyram_mas) - 1)
                pyramid_pos_y, pyramid_pos_x = pyram_mas[pos]
                pyramid = level[pyramid_pos_y][pyramid_pos_x]
                pyram_empty = pyram_find_empty(level, pyramid_pos_y, pyramid_pos_x)
                len_p = len(pyram_empty)
                if len_p>0:
                    vek = random.randint(0,len_p-1)
                    face = pyram_empty[vek][2]

            ################################################################################
            # обработка нажатия на пирамидки в игровом поле

            if mouse_x+mouse_y > 0:
                BORD = BORDER + RADIUS
                if BORD<mouse_y<(WIN_HEIGHT-BORD) and BORD<mouse_x<(WIN_WIDTH-BORD): # мышь внутри игрового поля
                    yy = (mouse_y-BORD)//HEIGHT_PYRAMID # строка
                    y2 = (mouse_y-BORD)% HEIGHT_PYRAMID # координаты в строке

                    xx = int((mouse_x-BORD)//(EDGE_PYRAMID/2)) # номер прямоугольного блока
                    x2 = int((mouse_x-BORD)% (EDGE_PYRAMID/2)) # координаты в блоке

                    pyramid_pos_y = yy

                    try: tg1 = y2/x2
                    except: tg1 = y2
                    try: tg11 = (HEIGHT_PYRAMID-y2)/(EDGE_PYRAMID/2-x2)
                    except: tg11 = y2

                    try: tg2 = y2/(EDGE_PYRAMID/2-x2)
                    except: tg2 = y2
                    try: tg22 = (HEIGHT_PYRAMID-y2)/x2
                    except: tg22 = y2

                    # разбор прямоугольных блоков шириной в пирамидку
                    if (yy % 2 == 0) == (xx % 2 == 0):  # 1 ряд, четные с 0 или 2 ряд, нечетные с 1
                        if tg2>TG60:
                            pyramid_pos_x = xx
                        else:
                            pyramid_pos_x = xx-1

                        orient = (pyramid_pos_y % 2 == 0) == (pyramid_pos_x % 2 == 0)  # уголок вверх
                        if tg2 < TG30 or tg22<TG30:
                            face = 1
                        elif orient:
                            face = 2
                        else:
                            face = 3
                    else: # elif (yy % 2 == 0) and (xx % 2 == 1):  # 1 ряд, нечетные с 1 или 2 ряд, четные с 0
                        if tg1>TG60:
                            pyramid_pos_x = xx-1
                        else:
                            pyramid_pos_x = xx

                        orient = (pyramid_pos_y % 2 == 0) == (pyramid_pos_x % 2 == 0)  # уголок вверх
                        if tg1<TG30 or tg11<TG30:
                            face = 1
                        elif orient:
                            face = 3
                        else:
                            face = 2

                    if pyramid_pos_x >= SIZE_X : pyramid_pos_x = -1

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
                            level[pyram_empty[pos][0]][pyram_empty[pos][1]] = pyram
                            level[pyramid_pos_y][pyramid_pos_x] = 0

                            if not undo:
                                moves += 1
                                moves_stack.append([vek,pyram_empty[pos][2],pyram_empty[pos][0],pyram_empty[pos][1]])

            if scramble_move != 0:
                scramble_move -= 1
                moves_stack = []
                moves = 0
                continue
                # отрисовка не нужна

            ################################################################################
            ################################################################################
            # отрисовка игрового поля
            screen.fill(BACKGROUND_COLOR)

            pf = Surface((WIN_WIDTH, WIN_HEIGHT))
            pf.fill(Color(GRAY_COLOR))
            screen.blit(pf, (0, 0))
            pf = Surface((WIN_WIDTH, BORDER))
            pf.fill(Color("#B88800"))
            screen.blit(pf, (0, WIN_HEIGHT))

            ################################################################################
            # text
            # screen.blit(textx, textx_place)
            # screen.blit(texty, texty_place)

            text_moves = font.render('Moves: ' + str(moves), True, PYRAMID_COLOR[2][1])
            text_moves_place = text_moves.get_rect(topleft=(10, button_y3-7))
            screen.blit(text_moves, text_moves_place)
            if solved:
                text_solved = font.render('Solved', True, PYRAMID_COLOR[0][1])
            else:
                text_solved = font.render('not solved', True, RED_COLOR)
            text_solved_place = text_solved.get_rect(topleft=(text_moves_place.right + 10, button_y3-7))
            screen.blit(text_solved, text_solved_place)

            ############################################
            # отрисовка сетки и пирамидок
            for fl_empty in range(3):
                for ny, row in enumerate(level):
                    for nx,pyramid in enumerate(row):
                        orient = (ny % 2 == 0) == (nx % 2 == 0) # уголок вверх

                        ############################################
                        # расчет всех координат
                        BORD = BORDER + RADIUS

                        if orient: # уголок вверх
                            fl_or = 1
                            if (ny % 2 == 0) and (nx % 2 == 0):  # 1 ряд, наверх
                                x1 = int(EDGE_PYRAMID / 2) + (nx // 2) * EDGE_PYRAMID + BORD
                            elif (ny % 2 == 1) and (nx % 2 == 1):  # 2 ряд, наверх
                                x1 = (nx // 2 + nx % 2) * EDGE_PYRAMID + BORD
                            y1 = ny * HEIGHT_PYRAMID + BORD
                            yy_grid = y1 + HEIGHT_PYRAMID
                        else:  # уголок вниз
                            fl_or = -1
                            if (ny % 2 == 0) and (nx % 2 == 1):  # 1 ряд, вниз
                                x1 = (nx // 2 + nx % 2) * EDGE_PYRAMID + BORD
                            elif (ny % 2 == 1) and (nx % 2 == 0):  # 2 ряд, вниз
                                x1 = int(EDGE_PYRAMID / 2) + (nx // 2) * EDGE_PYRAMID + BORD
                            y1 = (ny+1) * HEIGHT_PYRAMID + BORD
                            yy_grid = y1 - HEIGHT_PYRAMID

                        y1_grid = y1
                        y0  = y1 + int(2 * HEIGHT_PYRAMID / 3) * fl_or
                        x2_grid  = x1 + int(EDGE_PYRAMID / 2) * fl_or
                        x3_grid  = x1 - int(EDGE_PYRAMID / 2) * fl_or

                        # отрисовка пирамидок и лунок

                        if fl_empty == 0 and pyramid == 9:
                            draw.circle(screen, GRAY_COLOR2, (x1, y1_grid), 3)
                            draw.circle(screen, GRAY_COLOR2, (x2_grid, yy_grid), 3)
                            draw.circle(screen, GRAY_COLOR2, (x3_grid, yy_grid), 3)

                        if fl_empty == 1 and pyramid == 0:
                            RAD = int(RADIUS / 1.4)
                            scol, ecol = (160, 160, 160, 255), (120, 120, 120, 255)
                            screen.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x1-RAD, y1_grid-RAD))
                            screen.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x2_grid-RAD, yy_grid-RAD))
                            screen.blit(gradient_circle(RAD, scol, ecol, False, -1, offset=offset), (x3_grid-RAD, yy_grid-RAD))

                        if fl_empty == 2 and pyramid > 0 and pyramid < 9:  # пирамидка
                            scol,ecol = GRADIENT_COLOR[pyramid-1]
                            screen.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x1-RADIUS, y1_grid-RADIUS))
                            screen.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x2_grid-RADIUS, yy_grid-RADIUS))
                            screen.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x3_grid-RADIUS, yy_grid-RADIUS))
                            screen.blit(gradient_circle(RADIUS, scol, ecol, True, 1, offset=offset), (x1-RADIUS, y0-RADIUS))

            #####################################################################################
            pygame_widgets.update(events)
            pygame.display.update()  # обновление и вывод всех изменений на экран

        # удаляем кнопки
        for btn in button_set:
            btn.hide()

main()