# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 17:37:04 2022

@author: Alfred
"""
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QBrush
import random
import sys
import os


MAP_SIZE = 300
WALL_NUM = 5
WALL_SIZE = 30
DOT_NUM = 60
ENERMY_NUM = 2
CHARACTER_RAD = 10

FRESH_RATE = 10


class UI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.screen = QLabel()
        self.setCentralWidget(self.screen)
        
        start_menu = QAction('Start', self)
        start_menu.triggered.connect(self.start)
        self.menuBar().addAction(start_menu)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.timeout.connect(self.screen_fresh)
        
        self.start()
        
    def start(self):
        self.timer.stop()
        
        self.score = 0
        self.map = Map()
        
        self.Bean = self.map.generate(Bean)
        self.Enermies = [self.map.generate(Enermy) for i in range(ENERMY_NUM)]
        
        self.timer.start(FRESH_RATE)
        
    def game_over(self, pattern):
        self.timer.stop()
        if pattern == 'win':
            self.statusBar().showMessage('Congratulations! You win!')
        else:
            self.statusBar().showMessage('Oops, you lost. Come on, try again!')
    
    def move(self):
        if self.map.is_valid(self.Bean.steped()):
            self.Bean.move()
            
        for enermy in self.Enermies:
            enermy.get_step()
            if self.map.is_valid(enermy.steped()):
                enermy.move()
            else:
                enermy.step_count = 0
            if enermy.draw_touched(self.Bean):
                return self.game_over('lost')
        
        def eat_dot():
            def eaten(dot):
                dot.valid = False
                
            s = 0
            for dot in self.map.dots:
                if dot.valid and dot.draw_touched(self.Bean):
                    eaten(dot)
                    s += 1
            return s
        self.score += eat_dot()
        if self.score == DOT_NUM:
            return self.game_over('win')
            
        msg = 'Eaten: {eaten} Remain: {remain}'
        self.statusBar().showMessage(
            msg.format(eaten=self.score, remain=DOT_NUM - self.score)
        )
        
    def screen_fresh(self):
        self.screen.setPixmap(self.map.paint(self.Bean, self.Enermies))
        
    def keyPressEvent(self, ev):
        if self.timer.isActive():
            self.Bean.get_step(ev.key())
        super().keyPressEvent(ev)
        
    def keyReleaseEvent(self, ev):
        self.Bean.step = (0, 0)
        super().keyReleaseEvent(ev)
        

class Map():
    
    def __init__(self):
        self.pixmap = QPixmap(MAP_SIZE, MAP_SIZE)
        
        self.walls = []
        for i in range(WALL_NUM):
            self.walls.append(self.generate_wall())
        self.draw_walls()  

        self.dots = [self.generate(Dot) for i in range(DOT_NUM)]
                
    def generate(self, Obj):
        obj = Obj(Object.random_center())
        if self.is_valid(obj):
            return obj
        return self.generate(Obj)
    
    def generate_wall(self):
        wall = Wall(
            Object.random_center(),
            random.randint(0, WALL_SIZE), random.randint(0, WALL_SIZE)
        )
        if self.is_valid(wall):
            return wall
        return self.generate_wall()
    
    def is_valid(self, obj):
        if not obj.is_on_map():
            return False
        for wall in self.walls:
            if not obj.is_not_on_wall(wall):
                return False
        return True

    def draw_walls(self):
        def draw_wall(wall):
            painter.drawRect(
                *wall.draw_position(),
                wall.draw_length * 2, wall.draw_width * 2
            )
        
        painter = QPainter(self.pixmap)
        painter.setBrush(QBrush(Qt.black))
        painter.drawRect(0, 0, MAP_SIZE, MAP_SIZE)
        painter.setPen(Qt.blue)
        painter.setBrush(QBrush(Qt.blue))
        for wall in self.walls:
            draw_wall(wall)
            
    def draw_dots(self, painter):
        def draw_dot(dot):
            if dot.valid:
                painter.drawPoint(*dot.center)
                
        painter.setPen(Qt.yellow)
        for dot in self.dots:
            draw_dot(dot)
    
    @staticmethod
    def draw_Bean(painter, Bean):
        Bean.draw(painter)
        
    @staticmethod
    def draw_Enermy(painter, enermy):
        enermy.draw(painter)
        # painter.setPen(Qt.red)
        # painter.drawEllipse(
        #     *enermy.draw_position(), enermy.rad * 2, enermy.rad * 2
        # )

    def paint(self, Bean, Enermies):
        pixmap = self.pixmap.copy(0, 0, MAP_SIZE, MAP_SIZE)
        painter = QPainter(pixmap)
        self.draw_dots(painter)
        self.draw_Bean(painter, Bean)
        for enermy in Enermies:
            self.draw_Enermy(painter, enermy)
        return pixmap


class Object():
    
    @staticmethod
    def random_center():
        return random.randint(0, MAP_SIZE), random.randint(0, MAP_SIZE)
    
    def __init__(
            self, center,
            draw_length, draw_width,
            occupied_length, occupied_width
        ):
        
        self.center = center
        self.draw_length = draw_length
        self.draw_width = draw_width
        self.occupied_length = occupied_length
        self.occupied_width = occupied_width
        
    def is_on_map(self):
        x, y = self.center
        L = x - self.occupied_length
        R = x + self.occupied_length
        U = y - self.occupied_width
        D = y + self.occupied_width
        if L < 0 or U < 0 or R > MAP_SIZE or D > MAP_SIZE:
            return False
        return True
    
    def is_not_on_wall(self, wall):
        if wall.draw_touched(self):
            return False
        return True
    
    def draw_position(self):
        x, y = self.center
        return (x - self.draw_length, y - self.draw_width)
    
    def draw_touched(self, obj):
        x1, y1 = self.center
        x2, y2 = obj.center
        length = self.draw_length + obj.draw_length
        width = self.draw_width + obj.draw_width
        return abs(x1 - x2) < length and abs(y1 - y2) < width
    
    def occupied_touched(self, obj):
        x1, y1 = self.center
        x2, y2 = obj.center
        length = self.occupied_length + obj.occupied_length
        width = self.occupied_width + obj.occupied_width
        return abs(x1 - x2) < length and abs(y1 - y2) < width
    
    
class Dot(Object):
    
    def __init__(self, center):
        self.valid = True
        super().__init__(center, 0, 0, 1, 1)
        
        
class Wall(Object):
    
    def __init__(self, center, length, width):
        super().__init__(
            center,
            length, width,
            length + CHARACTER_RAD + 1, width + CHARACTER_RAD + 1
        )

    def is_on_map(self):
        x, y = self.center
        L = x - self.occupied_length
        R = x + self.occupied_length
        U = y - self.occupied_width
        D = y + self.occupied_width
        if L < CHARACTER_RAD or U < CHARACTER_RAD:
            return False
        if R > MAP_SIZE - CHARACTER_RAD or D > MAP_SIZE - CHARACTER_RAD:
            return False
        return True
    
    def is_not_on_wall(self, wall):
        if wall.occupied_touched(self):
            return False
        return True


class Character(Object):
    steps = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }
    def __init__(self, center, rad):
        self.rad = rad
        self.face = 'R'
        self.step = (0, 0)
        super().__init__(center, rad, rad, rad, rad)
        
    def steped_center(self):
        return tuple(x + y for x, y in zip(self.step, self.center))
    
    def steped(self):
        return Character(self.steped_center(), self.rad)
    
    def move(self):
        self.center = self.steped_center()
        
        
class Bean(Character):
    
    def __init__(self, center):
        super().__init__(center, CHARACTER_RAD)
        self.angle = 0
        
    def draw(self, painter):
        painter.setPen(Qt.yellow)
        painter.setBrush(QBrush(Qt.yellow))
        painter.drawEllipse(*self.draw_position(), self.rad * 2, self.rad * 2)
        
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        
        rate = 3
        def angle():
            total = (60 - rate * self.angle) *16
            start = total / 2
            if self.face == 'R':
                return -start, total 
            if self.face == 'U':
                return -start + 90 * 16, total 
            if self.face == 'L':
                return -start + 180 * 16, total 
            if self.face == 'D':
                return -start + 270 * 16, total 
        painter.drawPie(
            *self.draw_position(), self.rad * 2 + 1, self.rad * 2 + 1, *angle()
        )
        self.angle = (self.angle + 1) % (60 // rate)
        
    def get_step(self, key):
        def step():
            if key == Qt.Key_Up:
                return 'U'
            if key == Qt.Key_Down:
                return 'D'
            if key == Qt.Key_Left:
                return 'L'
            if key == Qt.Key_Right:
                return 'R'
            return None
        self.face = step()
        self.step = self.steps.get(self.face, None)

        
class Enermy(Character):
    
    def __init__(self, center):
        self.step_count = 0
        super().__init__(center, CHARACTER_RAD)
        
    def get_step(self):
        if self.step_count > 0:
            return
        self.face = random.choice(list(self.steps.keys()))
        self.step = self.steps[self.face]
        self.step_count = random.randint(1, MAP_SIZE // 2)
        
    def move(self):
        super().move()
        if self.step_count == 1:
            self.step = (0, 0)
        self.step_count += -1
        
    def draw(self, painter):
        path = '/'.join([os.getcwd(), 'enermy.jpg'])
        print(path)
        p = QPixmap(path)
        painter.drawPixmap(
            *self.draw_position(), p, 0, 0, self.rad * 2, self.rad * 2
        )
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        x, y = self.draw_position()
        def bias():
            if self.face == 'L':
                return 4, 5
            if self.face == 'R':
                return 5, 5
            if self.face == 'U':
                return 5, 3
            if self.face == 'D':
                return 5, 6
        bx, by = bias()
        painter.drawEllipse(x + bx, y + by, 2, 2)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec_()
