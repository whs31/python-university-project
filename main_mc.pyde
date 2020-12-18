"""
///////////////////////////////////////////DEFINES/////////////////////////////////////////////////
"""
d_max_rocket_count = 35                  #макс. количество ракет на карте (в 1 тик)

#Графика
d_draw_trails = True                     #отрисовка хвостов ракет
"""
///////////////////////////////////////////DEFINES////////////////////////////////////////////////
"""

import time
import random

global_rocket_count = 0
game_over = False
destroyed = [False, False, False, False, False, False, False, False]                      #массив bool с состоянием башенок (1-8)
RocketArray = []              #массив ракет

rand_start_x = []
rand_angle = []
rand_step = []

class Rocket(object):
    
    removetrace = False       #чек на линии после столкновения
    start_scale = 10          #i
    check = False             #чек на сужение после взрыва
    
    def __init__(self, start_x, angle, step, counter, draw_trails):
        self.start_x = start_x                     #стартовая координата по ОХ
        self.ox = start_x                          #текущая координата ОХ
        self.oy = 0                                #текущая координата ОУ
        self.angle = angle                         #угол старта (изменение х от времени)
        self.step = step                           #скорость (изменение у от времени)
        self.counter = counter                     #счетчик текущих ракет на карте
        self.draw_trails = draw_trails             #настройка отрисовки трасеров
        
            #отрисовка 1 ракеты в случайной точке под случайным углом
    def draw_(self):
        if self.removetrace == False and self.draw_trails == True:
            line (self.start_x, 0, self.ox, self.oy)
        if self.oy <= height and self.ox>-150 and self.ox<width+150:
            self.oy = self.oy+self.step*1.5+0.5
            self.ox = self.ox+self.angle
            ellipse (self.ox, self.oy, 5, 5)
        else:
            #анимация взрыва
            if self.start_scale<76 and self.check == False:
                self.start_scale=self.start_scale+1
                self.removetrace = True
            elif self.start_scale>=30 and self.check == True:
                self.start_scale=self.start_scale-0.2
            elif self.start_scale<30 and self.check == True and self.start_scale>=0:
                self.start_scale=self.start_scale-0.5
                if self.start_scale <= 0:
                    self.counter=False
            else:
                self.check = True
            circle(self.ox, self.oy, self.start_scale)
            
            
            #ломаем башенку
            if self.ox>70 and self.ox<70+125:
                 destroyed[0] = True
            elif self.ox>70+125 and self.ox<70+125*2:
                 destroyed[1] = True
            elif self.ox>70+125*2 and self.ox<70+125*3:
                 destroyed[2] = True
            elif self.ox>70+125*3 and self.ox<70+125*4:
                 destroyed[3] = True
            elif self.ox>width-55-125*4 and self.ox<width-55-125*3:
                 destroyed[4] = True
            elif self.ox>width-55-125*3 and self.ox<width-55-125*2:
                 destroyed[5] = True
            elif self.ox>width-55-125*2 and self.ox<width-55-125:
                 destroyed[6] = True
            elif self.ox>width-55-125 and self.ox<width-55:
                 destroyed[7] = True
            #print(i, check)


    
global rocket            #класс 

def setup():
    global rocket
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
    RocketArray.append(Rocket(rand_start_x[50], rand_angle[50], rand_step[50], True, d_draw_trails))  
    global_rocket_count = global_rocket_count+1
    time.gmtime(0)
    time.time()
    time.sleep(1)
    

    
    
    
def draw():
    frameRate(60) 
    
    global d_max_rocket_count, d_draw_trails
    
    global rocket
    global lucky38, arc_, tower, column_1, column_2, bridge
    global lucky38_d, arc__d, tower_d, column_1_d, column_2_d, bridge_d
    global crosshair
    global global_rocket_count, game_over
    
    background(39,37,30)
    tint(255, 128)
    image(filter_, 0, 0, width, height)
    noTint()
    
    
    
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
        if global_rocket_count <= d_max_rocket_count:
            RocketArray.append(Rocket(rand_start_x[random.randint(0,98)], rand_angle[random.randint(0,98)], rand_step[random.randint(0,98)], True, d_draw_trails))   #инициализация массива классов 
                                    #(случайная стартовая позиция по ОХ, случайный угол*случайное направление, случайная скорость)
            global_rocket_count = global_rocket_count+1
        
    
    if destroyed[0] == True and destroyed[1] == True and destroyed[2] == True and destroyed[3] == True and destroyed[4] == True and destroyed[5] == True and destroyed[6] == True and destroyed[7] == True:
        game_over = True
        
    print (destroyed [0], destroyed [1], destroyed [2], destroyed [3], destroyed [4], destroyed [5], destroyed [6], destroyed [7], game_over)
        
        
        
            
    image(crosshair, mouseX-15, mouseY-15)
        #print t, x
            
    
