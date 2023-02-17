# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 23:04:48 2022

@author: Alfred
"""
import random

class Points(list):
    
    def __init__(self, length=0):
        self.length = length
        super().__init__()
        
    def append(self, point):
        if len(self) >= self.length:
            self.pop(0)
        super().append(point)


class Snake():
    
    def __init__(self, x, y):
        self.header = Header(x, y)
        self.points = Points()
        self.points.length = 1
    

class Header():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    @staticmethod
    def add(x, y):
        return (x + y) % 75
        
    def move(self, direct):
        if direct == 'U':
            self.y = self.add(self.y, -1)
            return
        if direct == 'D':
            self.y = self.add(self.y, 1)
            return
        if direct == 'L':
            self.x = self.add(self.x, -1)
            return
        if direct == 'R':
            self.x = self.add(self.x, 1)
            return
        
    def occupied(self):
        return self.x, self.y


class Map():
    
    def __init__(self):
        snake = random.randint(0, 75 - 1), random.randint(0, 75 - 1)
        food = random.randint(0, 75 - 1), random.randint(0, 75 - 1)
        print(snake, food)
        self.snake = Snake(*snake)
        self.food = food
        self.direct = random.choice(['U', 'D', 'L', 'R'])
    
    def move(self):
        self.snake.header.move(self.direct)
        
        if self.snake.header.occupied() in self.snake.points:
            return False
        
        if self.snake.header.occupied() == self.food:
            self.snake.points.length += 1
            self.food = random.randint(0, 75 - 1), random.randint(0, 75 - 1)
            print(self.food)
        self.snake.points.append(self.snake.header.occupied())
        return True
    
    def get_direct(self, direct):
        if not direct:
            return
        if self.direct == 'U' and direct == 'D':
            return
        if self.direct == 'D' and direct == 'U':
            return
        if self.direct == 'L' and direct == 'R':
            return
        if self.direct == 'R' and direct == 'L':
            return
        self.direct = direct
        

from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QBrush
import sys
class Game(QMainWindow):
    
    def __init__(self):
        super().__init__()
            
        self.pixmap = QPixmap(75 * 4, 75 * 4)
        painter = QPainter(self.pixmap)
        painter.setBrush(QBrush(Qt.black))
        painter.drawRect(0, 0, 75 * 4, 75 * 4)
        
        self.map = Map()
        
        self.label = QLabel()
        self.setCentralWidget(self.label)
        
        start_menu = QAction('Start', self)
        start_menu.triggered.connect(self.start)
        self.menuBar().addAction(start_menu)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.timeout.connect(
            lambda: self.label.setPixmap(self.paint())
        )
        
        self.start()
        
    def start(self):
        self.timer.start(40)
        
    def move(self):
        if not self.map.move():
            self.timer.stop()
        
    def paint(self):
        pixmap = self.pixmap.copy(0, 0, 75 * 4, 75 * 4)
        painter = QPainter(pixmap)
        
        painter.setPen(Qt.yellow)
        x, y = self.map.food
        painter.drawRect(x * 4, y * 4, 4, 4)
        for point in self.map.snake.points:
            x, y = point
            painter.drawRect(x * 4, y * 4, 4, 4)
        return pixmap
        
    def keyPressEvent(self, ev):
        key = ev.key()
        def direct():
            if key == Qt.Key_Up:
                return 'U'
            if key == Qt.Key_Down:
                return 'D'
            if key == Qt.Key_Left:
                return 'L'
            if key == Qt.Key_Right:
                return 'R'
            return None
        self.map.get_direct(direct())
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Game()
    window.show()
    app.exec_()
    