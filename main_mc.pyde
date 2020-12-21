"""
**************************************************************************************************************************************************************************************************************************************

Группа: 3431101/000001
Рязанцев Дмитрий Леонидович

**************************************************************************************************************************************************************************************************************************************
"""


#TODO
"""
☑     наложение блюра при паузе и гамеовере
☑     звук
☑     табличка что это я все написал
"""




"""
///////////////////////////////////////////DEFINES/////////////////////////////////////////////////
"""
#Настройки игры
d_max_rocket_count = 5                   #макс. количество ракет на карте НА СТАРТЕ ИГРЫ (в 1 тик)
d_exp_radius_tolerance = 40              #радиус взрыва ракет игрока (влияет на сложность)
d_difficulty_factor = 1.00               #/стартовый/ коэффициент начисления очков от сложности (влияет на очки)
d_player_rocket_speed = 10               #скорость ракет игрока без бонусов

#Настройки графики
d_draw_trails = True                     #отрисовка хвостов ракет
d_draw_trails_p = True                   #отрисовка хвостов ракет игрока

"""
///////////////////////////////////////////DEFINES/////////////////////////////////////////////////
"""

import time
import random

add_library('beads')

ac1 = AudioContext()

"""
-------------ИГРОВЫЕ ПЕРЕМЕННЫЕ-----------------
"""
game_over = False
score = 0
paused = False
"""
------------------------------------------------
"""

global_rocket_count = 0       #текущее количество вражеских ракет на карте
mouse_click_count = 0         #количество нажатий ЛКМ

destroyed = [False, False, False, False, False, False, False, False]                      #массив bool с состоянием башенок (1-8)
check_once = [True, True, True, True, True, True, True, True, True, True]                 #массив bool для выполнения изменения сложности 1 раз

RocketArray = []              #массив ракет
MissileArray = []             #массив ракет игрока

rand_start_x = []             #массивы, хранящие случайные координаты, углы и скорости для ракет
rand_angle = []
rand_step = []

current_exp_x = []
current_exp_y = []

class Missile(object):
    
    removetrace = False       #чек на линии после столкновения
    start_scale = 10          #переменная для отрисовки взрыва
    check = False             #чек на сужение после взрыва
    check_onetime_1 = True    #чек на выполнение добавления в массив один раз
    check_onetime_2 = True    #чек уборку из массива один раз
    #index = 0                #номер в массиве текущих взрывов
    def __init__(self, target_x, target_y, counter, draw_trails, d_player_rocket):
        self.target_x = target_x         #координата ОХ цели
        self.target_y = target_y         #координата ОУ цели
        self.start_x = width/2           #координата точки запуска
        self.start_y = height-20   
        self.ox = self.start_x           #текущие координаты
        self.oy = self.start_y
        self.speed = d_player_rocket     #скорость по гипотенузе
        self.draw_trails = draw_trails   #чек отрисовки хвостов
        self.a = atan(float((float(-self.target_y)+float(self.start_y))/(float(self.target_x)-float(self.start_x)+0.00001)))     #угол между траекторией полета и осью ОХ (вычисляется через тангенс)
        self.check_reached = False       #чек взрыва
        self.counter = counter           #чек на убирание ракеты из списка на отрисовку
        #print self.a 
        
        
    def draw_(self):
        if self.removetrace == False and self.draw_trails == True:          #отрисовка хвоста
            line (self.start_x, self.start_y, self.ox, self.oy)
        if self.check_reached == False:                                     #если не достигнута точка взрыва
            if self.target_x > width/2:                                     #направление полета
                self.ox = self.ox+self.speed*cos(self.a)                    
                self.oy = self.oy-self.speed*sin(self.a)
            elif self.target_x < width/2:
                self.ox = self.ox-self.speed*cos(self.a)
                self.oy = self.oy+self.speed*sin(self.a)
            ellipse (self.ox, self.oy, 6, 6)
        if self.ox>=self.target_x-10 and self.ox<=self.target_x+10 and self.oy>=self.target_y-10 and self.oy<=self.target_y+10:
            self.check_reached = True
            
            #запись в массивы координат взрыва
            if self.check_onetime_1 == True:
                current_exp_x.append(self.target_x)
                current_exp_y.append(self.target_y)
                self.check_onetime_1 = False
            #self.index = current_exp_x(self.target_x)
            
            #анимация взрыва
            if self.start_scale<150 and self.check == False:
                self.start_scale=self.start_scale+4
                self.removetrace = True
            elif self.start_scale>=30 and self.check == True:
                self.start_scale=self.start_scale-2
            elif self.start_scale<30 and self.check == True and self.start_scale>=0:
                if self.check_onetime_2 == True:
                    current_exp_x.remove(self.target_x)
                    current_exp_y.remove(self.target_y)
                    self.check_onetime_2 = False
                self.start_scale=self.start_scale-1
                if self.start_scale <= 9:
                    self.counter=False
            else:
                self.check = True
            fill(255,231,10, 160)
            stroke(255,231,10, 160)
            circle(self.ox, self.oy, self.start_scale)
            fill(255,231,10)
            stroke(255,231,10)

class Rocket(object):
    global score
    global d_difficulty_factor
    removetrace = False       #чек на линии после столкновения
    start_scale = 10          #i
    check = False             #чек на сужение после взрыва
    explode = False           #переменная для взрыва
    check_onetime = True      #чек на начисление очков один раз
    
    def __init__(self, start_x, angle, step, counter, draw_trails, d_exp_radius_tolerance):
        self.start_x = start_x                               #стартовая координата по ОХ
        self.ox = start_x                                    #текущая координата ОХ
        self.oy = 0                                          #текущая координата ОУ
        self.angle = angle                                   #угол старта (изменение х от времени)
        self.step = step                                     #скорость (изменение у от времени)
        self.counter = counter                               #счетчик текущих ракет на карте
        self.draw_trails = draw_trails                       #настройка отрисовки трасеров
        self.d_exp_radius_tolerance = d_exp_radius_tolerance #настройка радиуса взрыва (хитбокса) ракет игрока 
        
            #отрисовка 1 ракеты в случайной точке под случайным углом
    def draw_(self):
        if self.removetrace == False and self.draw_trails == True:
            line (self.start_x, 0, self.ox, self.oy)
        if self.oy <= height and self.ox>-150 and self.ox<width+150 and self.explode == False:
            self.oy = self.oy+self.step*2.5*d_difficulty_factor+0.5
            self.ox = self.ox+self.angle
            ellipse (self.ox, self.oy, 5, 5)
        elif self.oy > height or self.ox<-150 or self.ox>width+150:
            self.explode = True
        for o in range (0, len(current_exp_x)):
            if self.ox > current_exp_x[o]-d_exp_radius_tolerance and self.ox < current_exp_x[o]+d_exp_radius_tolerance and self.oy > current_exp_y[o]-d_exp_radius_tolerance and self.oy < current_exp_y[o]+d_exp_radius_tolerance:
                self.explode = True
                if self.check_onetime == True:
                    global score, d_difficulty_factor
                    score=score+100*d_difficulty_factor
                    self.check_onetime = False
        if self.explode == True:
            #анимация взрыва
            if self.start_scale<140 and self.check == False:
                self.start_scale=self.start_scale+2
                self.removetrace = True
            elif self.start_scale>=30 and self.check == True:
                self.start_scale=self.start_scale-0.4
            elif self.start_scale<30 and self.check == True and self.start_scale>=0:
                self.start_scale=self.start_scale-1
                if self.start_scale <= 9:
                    self.counter=False
            else:
                self.check = True
            circle(self.ox, self.oy, self.start_scale)
            
            
            #ломаем башенку
            if self.ox>70 and self.ox<70+125 and self.oy > height-80:
                 destroyed[0] = True
            elif self.ox>70+125 and self.ox<70+125*2 and self.oy > height-80:
                 destroyed[1] = True
            elif self.ox>70+125*2 and self.ox<70+125*3 and self.oy > height-80:
                 destroyed[2] = True
            elif self.ox>70+125*3 and self.ox<70+125*4 and self.oy > height-80:
                 destroyed[3] = True
            elif self.ox>width-55-125*4 and self.ox<width-55-125*3 and self.oy > height-80:
                 destroyed[4] = True
            elif self.ox>width-55-125*3 and self.ox<width-55-125*2 and self.oy > height-80:
                 destroyed[5] = True
            elif self.ox>width-55-125*2 and self.ox<width-55-125 and self.oy > height-80:
                 destroyed[6] = True
            elif self.ox>width-55-125 and self.ox<width-55 and self.oy > height-80:
                 destroyed[7] = True
            #print(i, check)


    
global rocket, missile            #классы $$

def setup():
    global rocket, missile
    global lucky38, arc_, tower, column_1, column_2, bridge, silo
    global lucky38_d, arc__d, tower_d, column_1_d, column_2_d, bridge_d
    global crosshair, filter_, font, font_credits, global_rocket_count, score, pause
    
    
    size(1440, 900)
    smooth(4)
    noCursor()
    strokeWeight(2)
    frameRate(60) 
    
    font = loadFont("CenturyGothic-Bold-48.vlw")
    font_credits = loadFont("GillSansMT-48.vlw")
    
    #**********************ИНИЦИАЛИЗАЦИЯ ЗВУКОВ**********************************
    f_startsound = SampleManager.sample("/music1.mp3")
    startsound = SamplePlayer(ac1, f_startsound)
    g1 = Gain(ac1, 2, 0.1)
    g1.addInput(startsound)
    ac1.out.addInput(g1)
    
    lucky38 = loadImage("lucky38.png")                                                       #импорт картинок башенок
    arc_ = loadImage("arc.png")
    tower = loadImage("tower.png")
    column_1 = loadImage("column_1.png")
    column_2 = loadImage("column_2.png")
    bridge = loadImage("bridge.png")
    lucky38_d = loadImage("lucky38_destroyed.png")                                           #импорт картинок разрушенных башенок
    arc__d = loadImage("arc_destroyed.png")
    tower_d = loadImage("tower_destroyed.png")
    column_1_d = loadImage("column_1_destroyed.png")
    column_2_d = loadImage("column_2_destroyed.png")
    bridge_d = loadImage("bridge_destroyed.png")
    
    silo = loadImage("silo.png")
    
    crosshair = loadImage("crosshair.png")                                                   #импорт прочего         
    filter_ = loadImage("filter.png")
    pause = loadImage("pause.png")
    
    
    direction = [-1, 1]       #случайное стартовое направление
    for x in range(1,100):
        rand_start_x.append(random.randint(150, width-150))
        rand_angle.append(random.random()*random.choice(direction))
        rand_step.append(random.random())
        #RocketArray.append(Rocket(0, 0, 0, True))               
    RocketArray.append(Rocket(rand_start_x[50], rand_angle[50], rand_step[50], True, d_draw_trails, d_exp_radius_tolerance))  
    #MissileArray.append(Missile(500, 500, d_draw_trails))
    global_rocket_count = global_rocket_count+1
    
    score = 0
    
    time.gmtime(0)
    time.time()
    time.sleep(1)
    ac1.start()
def mousePressed(): 
    global mouse_click_count, d_draw_trails_p, missile, pause, paused, game_over
    if mouseX < width-60 and mouseY > 60 and game_over==False:
        MissileArray.append(Missile(mouseX, mouseY, True, d_draw_trails_p, d_player_rocket_speed))
        mouse_click_count = mouse_click_count+1
    elif paused==False and mouseX>width-60 and mouseY<60 and game_over==False:            #пауза в игре
        tint (128)
        image(pause, width - 60, 10)  
        noTint()
        paused=True
        filter(BLUR, 5)
        filter(GRAY)
        fill(255,255,255)
        stroke(255,255,255)
        textSize(48)
        text("P    A    U    S    E    D", width/2-200, 300)
        fill(200,200,200)
        stroke(200,200,200)
        textSize(20)
        text("Click Pause to continue.", width/2-100, 325)
        fill(237,204,17)
        stroke(237,204,17)
        cursor()
        noLoop()
    elif paused==True:
        paused = False
        filter(BLUR, 0)
        filter(GRAY)
        noCursor()
        loop()
    if game_over==True:
        exit()
    
    
    
def draw():
    
    
    global d_max_rocket_count, d_draw_trails, d_draw_trails_p, d_exp_radius_tolerance, d_difficulty_factor
    
    global rocket, missile
    global lucky38, arc_, tower, column_1, column_2, bridge, silo
    global lucky38_d, arc__d, tower_d, column_1_d, column_2_d, bridge_d
    global crosshair, font, font_credits, pause
    global global_rocket_count, game_over, mouse_click_count, score
    
    background(39,37,30)                        #фон (темно-янтарный)
    tint(255, 128)                              #прозрачность следующей картинки 50%
    image(filter_, 0, 0, width, height)         #текстура ЭЛТ экрана
    noTint()                                    #прозрачность следующей картинки 100%
    image(pause, width - 60, 10)                #пауза (иконка)
    
    
    
    image(silo, width/2-75, height-120)
    
    #ОТРИСОВКА БАШЕНОК через switch
    if destroyed[0] == False:
        image(arc_, 70, height-220)
    elif destroyed[0] == True:
        image(arc__d, 70, height-220)
    if destroyed[1] == False:
        image(tower, 70+125, height-220)
    elif destroyed[1] == True:
        image(tower_d, 70+125, height-220)
    if destroyed[2] == False:
        image(column_1, 70+125*2, height-220)
    elif destroyed[2] == True:
        image(column_1_d, 70+125*2, height-220)
    if destroyed[3] == False:
        image(bridge, 70+125*3, height-220)
    elif destroyed[3] == True:
        image(bridge_d, 70+125*3, height-220)
    if destroyed[4] == False:
        image(column_2, width-180-125*3, height-220)
    elif destroyed[4] == True:
        image(column_2_d, width-180-125*3, height-220)
    if destroyed[5] == False:
        image(arc_, width-180-125*2, height-220)
    elif destroyed[5] == True:
        image(arc__d, width-180-125*2, height-220)
    if destroyed[6] == False:
        image(lucky38, width-180-125, height-220)
    elif destroyed[6] == True:
        image(lucky38_d, width-180-125, height-220)
    if destroyed[7] == False:
        image(tower, width-180, height-220)
    elif destroyed[7] == True:
        image(tower_d, width-180, height-220)
    
    fill(237,204,17)
    stroke(237,204,17)
    
    #геймовер
    if game_over==True:
        textSize(60)
        filter(BLUR, 5)
        fill(255,255,255)
        stroke(255,255,255)
        text("G   A   M   E       O   V   E   R", width/2-325, 300)
        fill(200,200,200)
        stroke(200,200,200)
        textSize(20)
        text("Any click to exit game.", width/2-100, 325)
        fill(237,204,17)
        stroke(237,204,17)
        filter(GRAY)
        noLoop()
    for i in range (0, len(RocketArray)):                    #отрисовка массива ракет
        RocketArray[i].draw_()
        if RocketArray[i].counter == False:
            global_rocket_count = global_rocket_count-1
            RocketArray.pop(i)
        if global_rocket_count < d_max_rocket_count:
            RocketArray.append(Rocket(rand_start_x[random.randint(0,98)], rand_angle[random.randint(0,98)], rand_step[random.randint(0,98)], True, d_draw_trails, d_exp_radius_tolerance))   #инициализация массива классов 
                                    #(случайная стартовая позиция по ОХ, случайный угол*случайное направление, случайная скорость)
            global_rocket_count = global_rocket_count+1
    for j in range (0, mouse_click_count):
        if MissileArray[j].counter == True:
            strokeWeight(1)
            MissileArray[j].draw_()
            strokeWeight(2)
    #усложняем игру каждые 10 сбитых ракет и вводим коэффициент сложности 
    
    if score >= 1000 and score < 2000 and check_once[0] == True:
        d_max_rocket_count = d_max_rocket_count+3
        d_difficulty_factor = 1.1
        check_once[0] = False
    if score >= 2000 and score < 3000 and check_once[1] == True:
        d_max_rocket_count = d_max_rocket_count+3
        d_difficulty_factor = 1.2
        check_once[1] = False
    if score >= 3000 and score < 5000 and check_once[2] == True:
        d_max_rocket_count = d_max_rocket_count+4
        d_difficulty_factor = 1.3
        check_once[2] = False
    if score >= 5000 and score < 7500 and check_once[3] == True:
        d_max_rocket_count = d_max_rocket_count+5
        d_difficulty_factor = 1.5
        check_once[3] = False
    if score >= 7500 and score < 10000 and check_once[4] == True:
        d_max_rocket_count = d_max_rocket_count+5
        d_difficulty_factor = 1.7
        check_once[4] = False
    if score >= 10000 and score < 15000 and check_once[5] == True:
        d_max_rocket_count = d_max_rocket_count+5
        d_difficulty_factor = 1.8
        check_once[5] = False
    if score >= 15000 and score < 20000 and check_once[6] == True:
        d_max_rocket_count = d_max_rocket_count+3
        d_difficulty_factor = 2
        check_once[6] = False
    if score >= 20000 and score < 25000 and check_once[7] == True:
        d_max_rocket_count = d_max_rocket_count+5
        d_difficulty_factor = 3
        check_once[7] = False
    if score >= 25000 and score < 30000 and check_once[8] == True:
        d_max_rocket_count = d_max_rocket_count+3
        d_difficulty_factor = 3.5
        check_once[8] = False
    #хардкор-режим
    if score >= 30000 and check_once[9] == True:
        d_max_rocket_count = d_max_rocket_count+25
        d_difficulty_factor = 10
        check_once[9] = False
    #print len(current_exp_x)
    textFont(font)
    textSize(24)
    text("Score: ", 20, 30)
    text(int(score), 100, 30)
    
    textSize(18)
    #текущая сложность:
    if check_once[0] == True:
        text("Very Easy", 20, 50)
    elif check_once[0] == False and check_once[1] == True:
        fill(255,231,10)
        stroke(255,231,10)
        text("Easy", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)          
    if check_once[1] == False and check_once[2] == True:
        fill(255,243,134)
        stroke(255,243,134)
        text("Apprentice", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[2] == False and check_once[3] == True:
        fill(255,255,255)
        stroke(255,255,255)
        text("Intermediate", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[3] == False and check_once[4] == True:
        fill(250,171,0)
        stroke(250,171,0)
        text("Hard", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[4] == False and check_once[5] == True:
        fill(250,84,0)
        stroke(250,84,0)
        text("Harder", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[5] == False and check_once[6] == True:
        fill(180,6,0)
        stroke(180,6,0)
        text("Very Hard", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[6] == False and check_once[7] == True:
        fill(141,1,141)
        stroke(141,1,141)
        text("INSANE", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[7] == False and check_once[8] == True:
        fill(0,215,255)
        stroke(0,215,255)
        text("IMPOSSIBLE", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[8] == False and check_once[9] == True:
        fill(155,122,91)
        stroke(155,122,91)
        text("NIGHTMARE", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    if check_once[9] == False:
        fill(227,19,0)
        stroke(227,19,0)
        text("A P O C A L Y P S E", 20, 50)
        fill(237,204,17)
        stroke(237,204,17)
    #print score

        
            
    if destroyed[0] == True and destroyed[1] == True and destroyed[2] == True and destroyed[3] == True and destroyed[4] == True and destroyed[5] == True and destroyed[6] == True and destroyed[7] == True:
        game_over = True
        
    #print 'Towers:', destroyed [0], destroyed [1], destroyed [2], destroyed [3], destroyed [4], destroyed [5], destroyed [6], destroyed [7], '\t Game Over:', game_over
    image(crosshair, mouseX-15, mouseY-15)      #перекрестье курсосра
    fill(255,255,255, 128)
    stroke(255,255,255, 128)
    textSize(12)
    text("ROCKET COMMANDER", 10, height-30)
    fill(200,200,200, 100)
    stroke(200,200,200, 100)
    text("A game by Dmitry Ryazantsev", 10, height-16)
    fill(237,204,17)
    stroke(237,204,17)
        
def stop():
    ac1.stop()
            
    
