import pygame
import button
import random
import operator
from bidi import algorithm
import persian_reshaper
import os
import subprocess


pygame.init()

WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("میرزا در جنگل")

font_64 = pygame.font.Font("assets/A_Ketab_Bold.TTF", 64)
font_48 = pygame.font.Font("assets/A_Ketab_Bold.TTF", 48)
font_24 = pygame.font.Font("assets/A_Ketab_Bold.TTF", 24)
font_26 = pygame.font.SysFont("Script", 26)

namequery = algorithm.get_display(persian_reshaper.reshape('میرزا در جنگل'))
levelquery = algorithm.get_display(persian_reshaper.reshape('مرحله را انتخاب کنید!'))
startquery = algorithm.get_display(persian_reshaper.reshape(' '))
scorequery = algorithm.get_display(persian_reshaper.reshape('امتیاز '))
scorequery2 = algorithm.get_display(persian_reshaper.reshape('امتیاز شما '))
winquery01 = algorithm.get_display(persian_reshaper.reshape('برنده شدی'))
lossquery02 = algorithm.get_display(persian_reshaper.reshape('باختی'))

guide_pdf = "assets/Guide.pdf"

gamename = font_64.render((namequery), True, (255, 255, 255))
gamename_rect = gamename.get_rect()
gamename_rect.center = (1280 // 2, 720 // 2)
gamestart = font_24.render((startquery), True, (255, 255, 255))
gamestart_rect = gamestart.get_rect()
gamestart_rect.center = (1280 // 2, 720 * 2 // 3)

slide = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-slide-0{frame}.png"), (200, 148)) for frame in
         range(0, 2)]
jump = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-jump-0{frame}.png"), (200, 148)) for frame in
        range(2, 6)]
run = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-run-0{frame}.png"), (200, 148)) for frame in
       range(0, 6)]
bg = pygame.transform.scale(pygame.image.load('assets/Background.gif'), (1280, 720))
bg02 = pygame.transform.scale(pygame.image.load('assets/Background.png'), (1280, 720))
# winbg = pygame.transform.scale(pygame.image.load('assets/win_game.jpg'), (1280, 720))
# lossbg = pygame.transform.scale(pygame.image.load('assets/end_game2.png'), (1280, 720))
axe = pygame.transform.scale(pygame.image.load("assets/box-remove.png"), (60, 59))
sign = pygame.transform.scale(pygame.image.load("assets/box-remove.png"), (100, 157))
box = pygame.transform.scale(pygame.image.load("assets/box-remove.png"), (60, 60))

# load button
chemistary_butt = pygame.transform.scale(pygame.image.load("assets/chem.png"), (110, 115))
algebra_butt = pygame.transform.scale(pygame.image.load("assets/math.png"), (110, 115))
help_button = pygame.transform.scale(pygame.image.load("assets/help.png"), (50, 50))
exit_button = pygame.transform.scale(pygame.image.load("assets/exit.png"), (50, 50))
back_butt = pygame.transform.scale(pygame.image.load("assets/back.png"), (55, 55))
level1_butt = pygame.transform.scale(pygame.image.load("assets/level01.png"), (150, 150))
level2_butt = pygame.transform.scale(pygame.image.load("assets/level02.png"), (150, 150))
level3_butt = pygame.transform.scale(pygame.image.load("assets/level03.png"), (150, 150))
# level4_button = pygame.transform.scale(pygame.image.load("assets/exit.png"), (50, 50))


# button
chem_butt = button.Button(304, 125, chemistary_butt, 1)
math_butt = button.Button(904, 125, algebra_butt, 1)
help_butt = button.Button(1160, 645, help_button, 1)
exit_butt = button.Button(70, 645, exit_button, 1)
back_button = button.Button(170, 645, back_butt, 1)
level1_button = button.Button(300, 285, level1_butt, 1)
level2_button = button.Button(600, 285, level2_butt, 1)
level3_button = button.Button(900, 285, level3_butt, 1)


bg_x = 0
bg_x2 = bg.get_width()

clock = pygame.time.Clock()


class menu(object):
    def __init__(self, char_algebra, char_chem, game_pauesd,intro_selected_game,clock_variable,running,end,
                 obstacles,obstacle_hitboxes,equations,elements,elements_hitbox,equation_correct_hitboxes,equation_wrong_hitboxes,
                 restart,selected_level):
        self.char_algebra = False
        self.char_chem = False
        self.game_pauesd = False
        self.restart = restart
        self.intro_selected_game = intro_selected_game
        self.selected_level = selected_level
        self.clock_variable = clock_variable
        self.running = running
        self.end = end
        self.obstacles = obstacles
        self.obstacle_hitboxes = obstacle_hitboxes
        self.equations = equations
        self.elements = elements
        self.elements_hitbox = elements_hitbox
        self.equation_correct_hitboxes = equation_correct_hitboxes
        self.equation_wrong_hitboxes = equation_wrong_hitboxes

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_jump = False
        self.jump_count = 10
        self.is_run = True
        self.is_slide = False
        self.run_frame = 0
        self.jump_frame = 0
        self.slide_frame = 0
        self.distance = 0
        self.game_score = 0
        self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 115)
        self.algebra = False
        self.chem = False

    def draw(self, win):
        if self.is_run:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 115)
            if self.run_frame + 1 >= 18:
                self.run_frame = 0
            win.blit(run[self.run_frame // 3], (self.x, self.y))
            self.run_frame += 1
        if self.is_jump:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 100)
            if self.jump_frame + 1 >= 18:
                self.jump_frame = 0
            win.blit(jump[self.jump_frame // 5], (self.x, self.y))
            self.jump_frame += 1
            self.run_frame = 0
        if self.is_slide:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 80, 65, 60)
            if self.slide_frame + 1 >= 6:
                self.slide_frame = 0
            win.blit(slide[self.slide_frame // 3], (self.x, self.y))
            self.slide_frame += 1
            self.run_frame = 0


class obstacle(object):
    def __init__(self, x, y, width, height, name, obst):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.obst = obst
        if self.name == "axe":
            self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 45, 45)

        else:
            self.hitbox = pygame.Rect(self.x, self.y, 75, 75)

    def draw(self, win):
        if self.name == "axe":
            self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 45, 45)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 75, 75)
        win.blit(self.obst, (self.x, self.y))
        main_menu.obstacle_hitboxes.append(self.hitbox)


def text(txt, color, size):
    font = pygame.font.Font("assets/B_Koodak_Bold.TTF", size)
    mtxt = font.render(txt, False, color)
    return mtxt


def en_text(txt, color, size):
    font = pygame.font.Font("assets/8-BITWONDER.TTF", size)
    mtxt = font.render(txt, False, color)
    return mtxt


def per_text(txt, color, size):
    txt = algorithm.get_display(persian_reshaper.reshape(txt))
    font = pygame.font.Font("assets/B_Koodak_Bold.TTF", size)
    mtxt = font.render(txt, False, color)
    return mtxt


class equation(object):
    def __init__(self, x, y, width, height, name, equit, size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.equit = equit
        self.size = size
        self.answerX = 0
        self.answerY = 0
        self.color = (249, 246, 238)

        if self.name == "question":
            self.hitbox = (self.x, self.y + 10, text(self.equit, self.color, self.size))
        if self.name == "answer":
            self.hitbox = (self.x, self.y, text(self.equit, self.color, self.size))
            self.answerX = self.x
            self.answerY = self.y
        if self.name == "wrong":
            self.hitbox = (self.x, self.y + 40, text(self.equit, self.color, self.size))

    def draw(self, win):
        if self.name == "question":
            self.hitbox = (self.x, self.y + 10, text(self.equit, self.color, self.size))
        if self.name == "answer":
            self.hitbox = (self.x, self.y, text(self.equit, self.color, self.size))
        if self.name == "wrong":
            self.hitbox = (self.x, self.y + 40, text(self.equit, self.color, self.size))

        equit_cont = text(self.equit, self.color, self.size)
        equit_pos = (self.x, self.y)
        win.blit(equit_cont, equit_pos)
        main_menu.equation_wrong_hitboxes.append(self.hitbox)


class elementc(object):
    def __init__(self, x, y, width, height, name, element, size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.element = element
        self.size = size
        self.answerX = 0
        self.answerY = 0
        self.color = (249, 246, 238)

        if self.name == "question":
            self.hitbox = (self.x, self.y + 10, per_text(self.element, self.color, self.size))
        if self.name == "answer":
            self.hitbox = (self.x, self.y, en_text(self.element, self.color, self.size))
            self.answerX = self.x
            self.answerY = self.y

        if self.name == "wrong":
            self.hitbox = (self.x, self.y + 40, en_text(self.element, self.color, self.size))

    def draw(self, win):
        if self.name == "question":
            self.hitbox = (self.x, self.y + 10, per_text(self.element, self.color, self.size))
            element_cont = per_text(self.element, self.color, self.size)
        if self.name == "answer":
            self.hitbox = (self.x, self.y, en_text(self.element, self.color, self.size))
            element_cont = en_text(self.element, self.color, self.size)
        if self.name == "wrong":
            self.hitbox = (self.x, self.y + 40, en_text(self.element, self.color, self.size))
            element_cont = en_text(self.element, self.color, self.size)
        element_pos = (self.x, self.y)

        win.blit(element_cont, element_pos)
        main_menu.elements_hitbox.append(self.hitbox)

def redraw_game_window():
    score = font_24.render((scorequery) + str(char.game_score), True, (255, 255, 255))
    score_rect = score.get_rect()
    score_rect.center = (1100, 100)
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    win.blit(score, score_rect)
    char.draw(win)
    for obst in main_menu.obstacles:
        obst.draw(win)
    pygame.display.update()

    for equi in main_menu.equations:
        equi.draw(win)
    pygame.display.update()

    for elm in main_menu.elements:
        elm.draw(win)
    pygame.display.update()


def levels_page():
    levels = True

    while levels:
        # win.fill((0, 0, 0))
        win.blit(bg02, (bg_x, 0))
        win.blit(bg02, (bg_x2, 0))

        level_cont = text(levelquery, (255, 255, 255), 25)
        level_pos = (1020, 80)
        win.blit(level_cont, level_pos)

        score = text(scorequery2 + " " + str(char.game_score), (255, 255, 255), 25)
        score_rect = score.get_rect()
        score_rect.center = (120, 80)
        win.blit(score, score_rect)

        # Render buttons for different levels
        level1_button.draw(win)
        level2_button.draw(win)
        level3_button.draw(win)
        back_button.draw(win)
        exit_butt.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # quit()
            if exit_butt.draw(win):
                pygame.quit()
                # quit()
            if back_button.draw(win):
                game_intro()
            if level1_button.draw(win):
                levels = False
                main_menu.selected_level = 1
                main_menu.clock_variable = 25
                if main_menu.intro_selected_game == "Chem":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                if main_menu.intro_selected_game == "Math":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                #
                #
                # game_loop()  # Call the game loop with the selected level
            if level2_button.draw(win):
                levels = False
                main_menu.selected_level = 2
                main_menu.clock_variable = 38
                if main_menu.intro_selected_game == "Chem":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                    # game_loop()
                if main_menu.intro_selected_game == "Math":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                    # game_loop()
                # game_loop()  # Call the game loop with the selected level
            if level3_button.draw(win):
                levels = False
                main_menu.selected_level = 3
                main_menu.clock_variable = 60
                if main_menu.intro_selected_game == "Chem":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                    # game_loop()
                if main_menu.intro_selected_game == "Math":
                    main_menu.char_chem = True
                    main_menu.char_algebra = False
                    # win_game()





def game_intro():
    intro = True

    while intro:
        win.blit(bg, (0, 0))
        win.blit(gamename, gamename_rect)
        win.blit(gamestart, gamestart_rect)
        chem_butt.draw(win)
        math_butt.draw(win)
        help_butt.draw(win)
        exit_butt.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # end = False
                pygame.quit()
                # quit()
            # if event.type == pygame.KEYDOWN:
            if help_butt.draw(win):
                # intro = False
                main_menu.char_chem = False
                main_menu.char_algebra = False
                # os.startfile('assets/Guide.pdf')  # Call the Guide
                subprocess.Popen(['start', '', guide_pdf], shell=True)
            if exit_butt.draw(win):
                pygame.quit()
                # quit()
            if chem_butt.draw(win):
                intro = False
                main_menu.intro_selected_game = "Chem"
                levels_page()
                main_menu.char_chem = True
                main_menu.char_algebra = False
            if math_butt.draw(win):
                intro = False
                main_menu.intro_selected_game = "Math"
                levels_page()
                main_menu.char_chem = False
                main_menu.char_algebra = True


def game_loop():

    main_menu.running = True
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT, random.randrange(1000, 1200))
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randrange(900, 1100))
    pygame.time.set_timer(pygame.USEREVENT + 2, random.randrange(800, 1000))
    pygame.time.set_timer(pygame.USEREVENT + 3, random.randrange(700, 900))
    pygame.time.set_timer(pygame.USEREVENT + 4, random.randrange(650, 800))
    pygame.time.set_timer(pygame.USEREVENT + 5, random.randrange(650, 700))

    distance_initial = 0
    while main_menu.running:

        clock_variable = main_menu.clock_variable
        exit_butt.draw(win)
        back_button.draw(win)
        pygame.display.update()

        # frame rate
        clock.tick(clock_variable)

        # scrolling screen
        global bg_x
        global bg_x2
        bg_x -= 10
        bg_x2 -= 10
        if bg_x < bg.get_width() * -1:
            bg_x = bg.get_width()
        if bg_x2 < bg.get_width() * -1:
            bg_x2 = bg.get_width()

        # different condition for speed
        char.distance += 1
        distance_initial += 1

        # Scenarios
        if (char.distance % 2000) == 0:
            clock_variable += 5

        # exit & slide end listeners
        for event in pygame.event.get():
            if exit_butt.draw(win):
                pygame.quit()
                # quit()
            if back_button.draw(win):
                main_menu.equations.clear()
                main_menu.elements.clear()
                main_menu.obstacles.clear()
                pygame.display.update()
                game_intro()
            if event.type == pygame.QUIT:
                # game_intro()
                pygame.quit()
                # quit()
            elif event.type == pygame.KEYUP and char.is_slide:
                char.is_slide = False
                char.is_run = True

            else:

                if main_menu.char_algebra:
                    rand2 = random.randint(0, 4)
                    if char.distance % 2 != 0 and (char.distance % 15) == 0:  # Even
                        operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul)]

                        if main_menu.selected_level == 1:
                            variable1 = random.randint(0, 5)
                            variable2 = random.randint(0, 5)
                        elif main_menu.selected_level == 2:
                            variable1 = random.randint(0, 12)
                            variable2 = random.randint(0, 12)
                        elif main_menu.selected_level == 3:
                            variable1 = random.randint(0, 25)
                            variable2 = random.randint(0, 25)

                        op, fn = random.choice(operators)
                        answer = fn(variable1, variable2)
                        wrong_answer = fn(answer, random.randint(2, 5))

                        equations_question = "{} {} {} = {}".format(variable1, op, variable2, "؟")
                        main_menu.equations.append(
                            equation(WIN_WIDTH, WIN_HEIGHT - 560, 100, 50, 'question', equations_question, 40))
                        if rand2 >= 2:
                            main_menu.equations.append(
                                equation(WIN_WIDTH, WIN_HEIGHT - 300, 50, 50, 'answer', str(answer), 30))
                            main_menu.equations.append(
                                equation(WIN_WIDTH, WIN_HEIGHT - 149, 50, 50, 'wrong', str(wrong_answer), 30))
                        else:
                            main_menu.equations.append(
                                equation(WIN_WIDTH, WIN_HEIGHT - 149, 50, 50, 'answer', str(answer), 30))
                            main_menu.equations.append(
                                equation(WIN_WIDTH, WIN_HEIGHT - 300, 50, 50, 'wrong', str(wrong_answer), 30))
                    elif char.distance % 2 == 0 and (char.distance % 15) == 0:  # Odd iterations
                            main_menu.obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 139, 50, 50, 'box', box))


                if main_menu.char_chem:

                    rand = random.randint(0, 2)
                    rand2 = random.randint(0, 4)

                    if main_menu.selected_level == 1: #دسته‌بندی شده بر اساس سختی عناصر
                        mandaliof = {'هیدروژن': 'H', 'هلیم': 'He', 'بریلیوم': 'Be', 'بور': 'B', 'کربن': 'C',
                                     'نیتروژن': 'N', 'اکسیژن': 'O', 'فلوئور': 'F', 'نئون': 'Ne', 'سدیم': 'Na',
                                     'منیزیم': 'Mg', 'آلومینیوم': 'Al', 'سیلیکا': 'Si', 'فسفر': 'P',
                                     'گوگرد': 'S','کلر': 'Cl', 'آرگون': 'Ar'}
                    elif main_menu.selected_level == 2:
                        mandaliof = {'پتاسیم': 'K', 'کلسیم': 'Ca', 'اسکاندیوم': 'Sc', 'تیتانیوم': 'Ti',
                                           'وانادیوم': 'V',
                                           'کروم': 'Cr', 'منگنز': 'Mn', 'آهن': 'Fe', 'نیکل': 'Ni', 'مس': 'Cu',
                                           'روی': 'Zn', 'گالیوم': 'Ga', 'ژرمانیوم': 'Ge', 'آرسنیک': 'As',
                                           'سلنیوم': 'Se','برم': 'Br', 'کریپتون': 'Kr'}
                    elif main_menu.selected_level == 3:
                        mandaliof = {'استرانسیم': 'Sr', 'ایتریم': 'Y', 'زیرکونیم': 'Zr', 'نیوبیوم': 'Nb',
                                         'مولیبدن': 'Mo','تکنسیم': 'Tc', 'روتنیوم': 'Ru', 'رودیم': 'Rh', 'پالادیم': 'Pd', 'نقره': 'Ag',
                                         'کادمیوم': 'Cd', 'ایندیم': 'In', 'قلع': 'Sn', 'آنتیموان': 'Sb', 'تلوریم': 'Te',
                                         'ید': 'I', 'زنون': 'Xe', 'سزیم': 'Cs'}

                    element, persnam = random.choice(list(mandaliof.items()))
                    fakename = random.choice(list(mandaliof.values()))

                    if char.distance % 2 != 0 and (char.distance % 15) == 0:  # Even
                        main_menu.elements.append(
                            elementc(WIN_WIDTH, WIN_HEIGHT - 560, 100, 50, 'question', element, 40))
                        if rand2 >= 2:
                            main_menu.elements.append(
                                elementc(WIN_WIDTH, WIN_HEIGHT - 300, 50, 50, 'answer', fakename, 30))
                            main_menu.elements.append(
                                elementc(WIN_WIDTH, WIN_HEIGHT - 149, 50, 50, 'wrong', persnam, 30))
                        else:
                            main_menu.elements.append(
                                elementc(WIN_WIDTH, WIN_HEIGHT - 149, 50, 50, 'answer', persnam, 30))
                            main_menu.elements.append(
                                elementc(WIN_WIDTH, WIN_HEIGHT - 300, 50, 50, 'wrong', str(fakename), 30))

                    elif char.distance % 2 == 0 and (char.distance % 15) == 0:
                            main_menu.obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 139, 50, 50, 'box', box))


        collision_index = char.hitbox.collidelist(main_menu.obstacle_hitboxes)
        if collision_index != -1:
            main_menu.running = False
        main_menu.obstacle_hitboxes.clear()

        for obst in main_menu.obstacles:
            obst.x -= 10
            if obst.x < 0:
                main_menu.obstacles.remove(obst)

        if main_menu.char_algebra:
            for equ in main_menu.equations:
                equ.x -= 10
                if equ.name == 'answer':

                    if equ.x == char.x and equ.y == char.y + 79:  # age javabe dorost pain bashe
                        char.game_score += 1
                    if (equ.x == char.x + 130 or equ.x == char.x + 100) and (
                            equ.y == char.y + 120.5 or equ.y == char.y + 120 or equ.y == char.y + 118):  # age javabe dorost balai bashe
                        char.game_score += 1

                if equ.x < 0:
                    main_menu.equations.remove(equ)

        if main_menu.char_chem:
            for elm in main_menu.elements:
                elm.x -= 10
                if elm.name == 'answer':

                    if elm.x == char.x and elm.y == char.y + 79:  # age javabe dorost pain bashe 79
                        char.game_score += 1
                    if (elm.x == char.x + 130 or elm.x == char.x + 100) and (
                            elm.y == char.y + 120.5 or elm.y == char.y + 120 or elm.y == char.y + 118):  # age javabe dorost balai bashe
                        char.game_score += 1

                if elm.x < 0:
                    main_menu.elements.remove(elm)

        # player input
        keys = pygame.key.get_pressed()
        if not (char.is_jump) and keys[pygame.K_SPACE]:
            char.is_jump = True
            char.is_run = False
            char.is_slide = False
        elif char.is_jump:
            if char.jump_count >= -10:
                neg = 1
                if (char.jump_count < 0):
                    neg = -1
                char.y -= (char.jump_count ** 2) * neg * 0.5
                char.jump_count -= 1
            else:
                char.is_jump = False
                char.is_run = True
                char.jump_count = 10
        if not (char.is_slide) and not (char.is_jump) and keys[pygame.K_DOWN]:
            char.is_slide = True
            char.is_jump = False
            char.is_run = False

        #levels Score
        if char.game_score == 6 and main_menu.selected_level == 1:
            print("Win First Level")
            main_menu.running = False
            main_menu.equations.clear()
            main_menu.elements.clear()
            main_menu.obstacles.clear()
            main_menu.obstacle_hitboxes.clear()
            pygame.display.update()
            win_game()
        if char.game_score == 12 and main_menu.selected_level == 2:
            print("Win First Level")
            main_menu.running = False
            main_menu.equations.clear()
            main_menu.elements.clear()
            main_menu.obstacles.clear()
            main_menu.obstacle_hitboxes.clear()
            pygame.display.update()
            win_game()
        if char.game_score == 25 and main_menu.selected_level == 3:
            print("Win First Level")
            main_menu.running = False
            main_menu.equations.clear()
            main_menu.elements.clear()
            main_menu.obstacles.clear()
            main_menu.obstacle_hitboxes.clear()
            pygame.display.update()
            win_game()



        # redraw function
        redraw_game_window()

def win_game():
    main_menu.win = True
    clock_variable = 10
    pygame.display.update()
    # frame rate
    clock.tick(clock_variable)
    while main_menu.win:
        exit_butt.draw(win)
        back_button.draw(win)
        pygame.display.update()
        # win.blit(winbg, (bg_x, 0))
        pygame.display.update()
        win.fill((0, 0, 0))

        end_msg = font_64.render((winquery01), True, (255, 255, 255))
        end_msg_rect = end_msg.get_rect()
        end_msg_rect.center = (1280 // 2, 720 // 2)

        score = font_64.render((scorequery2) + str(char.game_score), True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.center = (1280 // 2, 720 * 2 // 3)
        win.blit(end_msg, end_msg_rect)
        win.blit(score, score_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                main_menu.running = False
                game_intro()
                # pygame.quit()
                # quit()
            if exit_butt.draw(win):
                pygame.quit()
                # quit()
            if back_button.draw(win):
                main_menu.running = True
                main_menu.end = False
                main_menu.restart = True
                main_menu.win = False
                main_menu.equations.clear()
                main_menu.elements.clear()
                main_menu.obstacles.clear()
                main_menu.obstacle_hitboxes.clear()
                game_intro()

def game_end():
    main_menu.end = True

    while main_menu.end:
        exit_butt.draw(win)
        back_button.draw(win)
        clock_variable = 0
        # frame rate
        clock.tick(clock_variable)
        pygame.display.update()
        win.fill((0, 0, 0))
        # win.blit(lossbg, (bg_x, 0))
        # win.blit(lossbg, (bg_x2, 0))
        pygame.display.update()

        end_msg = font_64.render((lossquery02), True, (0,0,139))
        end_msg_rect = end_msg.get_rect()
        end_msg_rect.center = (1280 // 2, 720 // 2)

        score = font_64.render((scorequery2) + str(char.game_score), True, (128,0,0))
        score_rect = score.get_rect()
        score_rect.center = (1280 // 2, 720 * 2 // 3)
        win.blit(end_msg, end_msg_rect)
        win.blit(score, score_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                main_menu.running = False
                game_intro()
                # pygame.quit()
            if exit_butt.draw(win):
                pygame.quit()
            if back_button.draw(win):
                main_menu.running = True
                main_menu.end = False
                main_menu.restart = True
                main_menu.equations.clear()
                main_menu.elements.clear()
                main_menu.obstacles.clear()
                main_menu.obstacle_hitboxes.clear()
                game_intro()



main_menu = menu(False, False, False,"",25,False,False,[],[],[],[],[],[],[],False,1)
char = player(150, WIN_HEIGHT - 228, 200, 148)
game_intro()
game_loop()
game_end()
pygame.quit()