# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:39:57 2023

@author: Alfred
"""
import os
from math import radians, degrees, sin, cos, tan, atan, sqrt
import pygame
from pygame.math import Vector2


def flip(x):
    return Vector2(x.x, -x.y)


class Map():
    
    def __init__(self, length=128, width=55):
        self.car = (500, 50)
        KW = 230.6 / 170.6 * width
        KL = 517.3 / 447.3 * length
        S = 670.95 / 447.3 * length
        H = 670.95 / 447.3 * length
        size_x = KW + S * 2 - 5
        size_y = 5 + S + 5 + KL + 5
        self.size = (size_x, size_y)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.set_colorkey((0,0,0))
        self.surface.fill((200,200,200))
        
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(0, 0, size_x, 5)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(0, S + 5, size_x, 5)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(H - 5, S + 5, 5, KL)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(H + KW, S + 5, 5, KL)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(H - 5, S + 5 + KL, KW + 10, 5)
        )
    
    
class Map2():
    
    def __init__(self, length=128, width=55):
        self.car = (400, 85)
        KW = 250.6 / 170.6 * width
        KL = 770.95 / 447.3 * length
        S = 335.9 / 447.3 * length
        size_x = length * 2 + KL + 5 * 2
        size_y = 5 + S + 5 + KW + 5
        self.size = (size_x, size_y)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.set_colorkey((0,0,0))
        self.surface.fill((200,200,200))
        
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(0, 0, size_x, 5)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(0, S + 5, size_x, 5)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(length, S + 10, 5, KW)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(length + KL + 5, S + 10, 5, KW)
        )
        pygame.draw.rect(
            self.surface, (255,255,0), pygame.Rect(length, S + 10 + KW, KL + 10, 5)
        )
        
        
class Map3():
    
    def __init__(self, length=128, width=55):
        self.car = (80, 630)
        R = 7.5 / 4.5 * length
        r = (7.5 - 3.5) / 4.5 * length
        size_x = 3 * R
        size_y = 2 * R - (R - R /1.414) - (r - r /1.414) + r - R + 2 * R
        self.size = (size_x, size_y)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.set_colorkey((0,0,0))
        self.surface.fill((200,200,200))
        
        pygame.draw.arc(
            self.surface, (255,255,0), pygame.Rect(R - 5 / 1.414, 5 /1.414, 2 * R, 2 * R), radians(90), radians(-135), 5
        )
        pygame.draw.arc(
            self.surface, (255,255,0), pygame.Rect(R * (2 - 1 /1.414) - r * (1 + 1/ 1.414) + r - R, 2 * R - (R - R /1.414) - (r - r /1.414) + r - R, 2 * R, 2 * R), radians(-90), radians(45), 5
        )
        pygame.draw.arc(
            self.surface, (255,255,0), pygame.Rect(2 * R - r - 5 /1.414, R - r + 5/1.414, 2 * r, 2 * r), radians(90), radians(-135), 5
        )
        pygame.draw.arc(
            self.surface, (255,255,0), pygame.Rect(R * (2 - 1 /1.414) - r * (1 + 1/ 1.414), 2 * R - (R - R /1.414) - (r - r /1.414), 2 * r, 2 * r), radians(-90), radians(45), 5
        )
        

class Tier():
    def __init__(self):
        self.surface = pygame.Surface((10, 5), pygame.SRCALPHA)
        self.surface.set_colorkey((0,0,0))
        self.surface.fill((0,255,255))

    def update(self, position):
        self.position += position


class Car():
    
    def __init__(self, x=0, y=0, angle=0.0, steer=0.0):
        # size
        self.middle = 75
        self.width = 50
        
        # control
        self.steer = steer
        self.steer_speed = 10
        self.gear = 'D'
        
        self.rotate_speed = 3
        
        # rright
        self._position = Vector2(x, y)
        
        # faster_rear
        self._speed = 0
        self.angle = angle
        self.acceleration = 0
        
        # tier
        self.tier = Tier()
        
    @property
    def speed(self):
        if self.gear == 'R':
            return -self._speed
        else:
            return self._speed
        
    def turning_radius(self, tier):
        if tier =='slower_rear':
            return self.middle / abs(tan(radians(self.steer)))
        if tier =='faster_rear':
            return self.turning_radius('slower_rear') + self.width

    @property
    def angular_velocity(self):
        if self.steer == 0:
            return 0
        return self.speed / self.turning_radius('faster_rear')
    
    def velocity(self, tier):
        if self.steer == 0:
            return flip(Vector2(self.speed, 0).rotate(self.angle))

        speed = self.angular_velocity * self.turning_radius(tier)
        return flip(Vector2(speed, 0).rotate(self.angle))

    def position(self, tier):
        if tier == 'rright':
            angle = 0
            length = 0
        if tier == 'rleft':
            angle = radians(self.angle + 90)
            length = self.width
        if tier == 'fright':
            angle = radians(self.angle)
            length = self.middle
        if tier == 'fleft':
            angle = radians(self.angle) + atan(self.width / self.middle)
            length = sqrt(self.width ** 2 + self.middle ** 2)
        if tier == 'car':
            return (
                self.position('fleft') + self.position('rright') + self.position('fright') + self.position('rleft')
            ) / 4
        return self._position + flip(Vector2(cos(angle), sin(angle)) * length)
    
    def move(self, move):
        self._position += move
        
    def rotate(self, dt):
        self.angle += self.rotate_speed * dt
        
    def update1(self, dt):
        if self.steer >= 0:
            tier = 'faster_rear'
        else:
            tier = 'slower_rear'
        self._position += self.velocity(tier) * dt
    
    def update2(self, dt):
        if self.steer > 0:
            angular_velocity = self.angular_velocity
        else:
            angular_velocity = -self.angular_velocity
        self.angle += degrees(angular_velocity) * dt
        self.angle = self.angle % 360
        self.speeding(dt)
    
    def speeding(self, dt):
        self._speed += self.acceleration * dt
        self._speed = max(0, min(20, self._speed))
        
    def steering(self, dt):
        self.steer += self.steer_speed * dt
        self.steer = max(-40, min(40, self.steer))
        
    def accelerating(self, acc):
        self.acceleration += acc
        self.acceleration = max(-20, min(3, self.acceleration))
        
    @property
    def image(self):
        if not hasattr(self, '_image'):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "car.png")
            self._image = pygame.image.load(image_path)
        return self._image

    def draw(self, screen):
        # car
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position('car') - (rect.width / 2, rect.height / 2))
        
        # fleft
        def angle(tier):
            if tier[0] == 'f':
                return self.angle + self.steer
            return self.angle
        for tier in ['fleft', 'rleft', 'rright', 'fright']:
            image = pygame.transform.rotate(self.tier.surface, angle(tier))
            rect = image.get_rect()
            screen.blit(
                image, self.position(tier) - (rect.width / 2, rect.height / 2)
            )
        

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")

    def run(self, M):
        clock = pygame.time.Clock()
        m = M()
        car = Car(*m.car)
        screen = pygame.display.set_mode(m.size)
        
        while pygame.QUIT not in map(lambda ev: ev.type, pygame.event.get()):
            dt = clock.get_time() / 200
            
            # User input
            pressed = pygame.key.get_pressed()
            
            # Super
            if pressed[pygame.K_w]:
                car.move((0, -1))
            elif pressed[pygame.K_a]:
                car.move((-1, 0))
            elif pressed[pygame.K_s]:
                car.move((0, 1))
            elif pressed[pygame.K_d]:
                car.move((1, 0))
            elif pressed[pygame.K_q]:
                car.rotate(3 * dt)
            elif pressed[pygame.K_e]:
                car.rotate(-3 * dt)
            elif pressed[pygame.K_BACKSPACE]:
                car.angle = 0
            
            # control
            if pressed[pygame.K_UP]:
                car.accelerating(1 * dt)
            elif pressed[pygame.K_DOWN]:
                car.accelerating(-1.2 * dt)
            elif pressed[pygame.K_SPACE]:
                car.accelerating(-10000)
            else:
                car.acceleration = 0

            if pressed[pygame.K_RIGHT]:
                car.steering(-dt)
            elif pressed[pygame.K_LEFT]:
                car.steering(dt)
            elif pressed[pygame.K_RETURN]:
                car.steer = 0
            
            if pressed[pygame.K_RCTRL]:
                car.gear = 'R'
            elif pressed[pygame.K_RSHIFT]:
                car.gear = 'D'

            # Logic
            car.update1(dt)
            screen.fill((0, 0, 0))
            screen.blit(m.surface, (0,0))
            car.draw(screen)
            car.update2(dt)
            
            pygame.display.flip()
            clock.tick(60)
            
            if pressed[pygame.K_ESCAPE]:
                self.run(M)
                break

        pygame.quit()
        
        
if __name__ == '__main__':
    game = Game()
    game.run(Map2)
