"""
**************************************************************************************************************************************************************************************************************************************

Группа: 3431101/000001
Рязанцев Дмитрий Леонидович

**************************************************************************************************************************************************************************************************************************************
"""







"""
///////////////////////////////////////////DEFINES/////////////////////////////////////////////////
"""
#Настройки игры
d_max_rocket_count = 15                  #макс. количество ракет на карте (в 1 тик)
d_exp_radius_tolerance = 40              #радиус взрыва ракет игрока (влияет на сложность)

#Настройки графики
d_draw_trails = True                     #отрисовка хвостов ракет
d_draw_trails_p = True                   #отрисовка хвостов ракет игрока

"""
///////////////////////////////////////////DEFINES/////////////////////////////////////////////////
"""

import time
import random

game_over = False

global_rocket_count = 0       #текущее количество вражеских ракет на карте
mouse_click_count = 0         #количество нажатий ЛКМ

destroyed = [False, False, False, False, False, False, False, False]                      #массив bool с состоянием башенок (1-8)

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
    #index = 0                 #номер в массиве текущих взрывов
    
    def __init__(self, target_x, target_y, counter, draw_trails):
        self.target_x = target_x         #координата ОХ цели
        self.target_y = target_y         #координата ОУ цели
        self.start_x = width/2           #координата точки запуска
        self.start_y = height-20   
        self.ox = self.start_x           #текущие координаты
        self.oy = self.start_y
        self.speed = 4                   #скорость по гипотенузе
        self.draw_trails = draw_trails   #чек отрисовки хвостов
        self.a = atan(float((float(-self.target_y)+float(self.start_y))/(float(self.target_x)-float(self.start_x))))     #угол между траекторией полета и осью ОХ (вычисляется через тангенс)
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
            current_exp_x.append(self.target_x)
            current_exp_y.append(self.target_y)
            #self.index = current_exp_x(self.target_x)
            
            #анимация взрыва
            if self.start_scale<150 and self.check == False:
                self.start_scale=self.start_scale+4
                self.removetrace = True
            elif self.start_scale>=30 and self.check == True:
                self.start_scale=self.start_scale-2
            elif self.start_scale<30 and self.check == True and self.start_scale>=0:
                current_exp_x.remove(self.target_x)
                current_exp_y.remove(self.target_y)
                self.start_scale=self.start_scale-1
                if self.start_scale <= 9:
                    self.counter=False
            else:
                self.check = True
            circle(self.ox, self.oy, self.start_scale)

class Rocket(object):
    
    removetrace = False       #чек на линии после столкновения
    start_scale = 10          #i
    check = False             #чек на сужение после взрыва
    explode = False           #переменная для взрыва
    
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
            self.oy = self.oy+self.step*1.5+0.5
            self.ox = self.ox+self.angle
            ellipse (self.ox, self.oy, 5, 5)
        elif self.oy > height or self.ox<-150 or self.ox>width+150:
            self.explode = True
        for o in range (0, len(current_exp_x)):
            if self.ox > current_exp_x[o]-d_exp_radius_tolerance and self.ox < current_exp_x[o]+d_exp_radius_tolerance and self.oy > current_exp_y[o]-d_exp_radius_tolerance and self.oy < current_exp_y[o]+d_exp_radius_tolerance:
                self.explode = True
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
    global lucky38, arc_, tower, column_1, column_2, bridge
    global lucky38_d, arc__d, tower_d, column_1_d, column_2_d, bridge_d
    global crosshair, filter_, global_rocket_count
    
    
    size(1440, 900)
    smooth()
    noCursor()
    strokeWeight(2)
    
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
    
    crosshair = loadImage("crosshair.png")                                                   #импорт прочего         
    filter_ = loadImage("filter.png")
    
    
    direction = [-1, 1]       #случайное стартовое направление
    for x in range(1,100):
        rand_start_x.append(random.randint(150, width-150))
        rand_angle.append(random.random()*random.choice(direction))
        rand_step.append(random.random())
        #RocketArray.append(Rocket(0, 0, 0, True))               
    RocketArray.append(Rocket(rand_start_x[50], rand_angle[50], rand_step[50], True, d_draw_trails, d_exp_radius_tolerance))  
    #MissileArray.append(Missile(500, 500, d_draw_trails))
    global_rocket_count = global_rocket_count+1
    time.gmtime(0)
    time.time()
    time.sleep(1)
    
def mouseClicked(): 
    global mouse_click_count, d_draw_trails_p, missile
    MissileArray.append(Missile(mouseX, mouseY, True, d_draw_trails_p))
    mouse_click_count = mouse_click_count+1
    
    
    
def draw():
    frameRate(60) 
    
    global d_max_rocket_count, d_draw_trails, d_draw_trails_p, d_exp_radius_tolerance
    
    global rocket, missile
    global lucky38, arc_, tower, column_1, column_2, bridge
    global lucky38_d, arc__d, tower_d, column_1_d, column_2_d, bridge_d
    global crosshair
    global global_rocket_count, game_over, mouse_click_count
    
    background(39,37,30)                        #фон (темно-янтарный)
    tint(255, 128)                              #прозрачность следующей картинки 50%
    image(filter_, 0, 0, width, height)         #текстура ЭЛТ экрана
    noTint()                                    #прозрачность следующей картинки 100%
    
    
    
    
    
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
        
            
    if destroyed[0] == True and destroyed[1] == True and destroyed[2] == True and destroyed[3] == True and destroyed[4] == True and destroyed[5] == True and destroyed[6] == True and destroyed[7] == True:
        game_over = True
        
    #print 'Towers:', destroyed [0], destroyed [1], destroyed [2], destroyed [3], destroyed [4], destroyed [5], destroyed [6], destroyed [7], '\t Game Over:', game_over
    image(crosshair, mouseX-15, mouseY-15)      #перекрестье курсосра
        

            
    
