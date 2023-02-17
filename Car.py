# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:39:57 2023

@author: Alfred
"""
import os
from math import sin, sqrt, radians, degrees, copysign, acos
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
        self.car = (500, 35)
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
        self.car = (130, 585)
        R = 7.5 / 4.5 * length
        r = (7.5 - 3.5) / 4.5 * length
        # KW = 250.6 / 170.6 * width
        # KL = 770.95 / 447.3 * length
        # H = R + R / 1.414 + 5
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
        # pygame.draw.rect(
        #     self.surface, (255,255,0), pygame.Rect(0, S + 5, size_x, 5)
        # )
        # pygame.draw.rect(
        #     self.surface, (255,255,0), pygame.Rect(length, S + 10, 5, KW)
        # )
        # pygame.draw.rect(
        #     self.surface, (255,255,0), pygame.Rect(length + KL + 5, S + 10, 5, KW)
        # )
        # pygame.draw.rect(
        #     self.surface, (255,255,0), pygame.Rect(length, S + 10 + KW, KL + 10, 5)
        # )
        

class Tier():
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.surface = pygame.Surface((10, 5), pygame.SRCALPHA)
        self.surface.set_colorkey((0,0,0))
        self.surface.fill((0,255,255))

    def update(self, position):
        self.position += position


class Car():
    
    def __init__(self, x=0, y=0, angle=0.0, steer=0.0):
        self.middle = 75
        self.width = 50
        
        self.fleft = Tier(x, y)
        self.rleft = Tier(x - self.middle, y)
        self.fright = Tier(x, y + self.width)
        self.rright = Tier(x - self.middle, y + self.width)
        
        self.speed = 0
        self.acceleration = 0
        self.angle = angle
        self.steer = steer
        
        self.gear = 'D'
        
    @property
    def center(self):
        return (self.fleft.position+self.rleft.position) / 2 + (self.rright.position - self.rleft.position) / 2
        
    def update(self, dt):        
        def position(turning_radius, aids=0):
            speed = copysign(angular_velocity * turning_radius, self.speed)
            velocity = Vector2(speed, 0.0)
            return velocity.rotate(-self.angle + aids) * dt
        def positionR(turning_radius, aids=0):
            speed = copysign(angular_velocity * turning_radius, self.speed)
            velocity = Vector2(speed, 0.0)
            return velocity.rotate(-self.angle + aids -180) * dt
        
        def gear_D_R(turning_radius):
            # fleft
            self.fleft.update(self.velocity.rotate(-self.angle - self.steer) * dt)
            
            # rleft
            turning_radius = sqrt(turning_radius ** 2 - self.middle ** 2)
            self.rleft.update(position(turning_radius))
            
            # rright
            turning_radius -= self.width
            self.rright.update(position(turning_radius))
            
            # fright
            _turning_radius = sqrt(turning_radius ** 2 + self.middle ** 2)
            angle = degrees(acos(turning_radius / _turning_radius))
            turning_radius = _turning_radius
            self.fright.update(position(turning_radius, angle))
        
        def gear_D_L(turning_radius):
            # fright
            self.fright.update(self.velocity.rotate(-self.angle - self.steer) * dt)
            
            # rright
            turning_radius = sqrt(turning_radius**2 - self.middle**2)
            self.rright.update(position(turning_radius))
            
            # rleft
            turning_radius -= self.width
            self.rleft.update(position(turning_radius))
            
            # fleft
            _turning_radius = sqrt(turning_radius**2 + self.middle**2)
            angle = degrees(acos(turning_radius / _turning_radius))
            turning_radius = _turning_radius
            self.fleft.update(position(turning_radius, -angle))
            
        def gear_R_R(turning_radius):
            # fleft
            self.fleft.update(positionR(turning_radius, -self.steer))
            
            # rleft
            turning_radius = sqrt(turning_radius ** 2 - self.middle ** 2)
            self.rleft.update(positionR(turning_radius))
            
            # rright
            turning_radius -= self.width
            self.rright.update(positionR(turning_radius))
            
            # fright
            _turning_radius = sqrt(turning_radius ** 2 + self.middle ** 2)
            angle = degrees(acos(turning_radius / _turning_radius))
            turning_radius = _turning_radius
            self.fright.update(positionR(turning_radius, angle))
        
        def gear_R_L(turning_radius):
            # fright
            self.fright.update(positionR(turning_radius, -self.steer))
            
            # rright
            turning_radius = sqrt(turning_radius**2 - self.middle**2)
            self.rright.update(positionR(turning_radius))
            
            # rleft
            turning_radius -= self.width
            self.rleft.update(positionR(turning_radius))
            
            # fleft
            _turning_radius = sqrt(turning_radius**2 + self.middle**2)
            angle = degrees(acos(turning_radius / _turning_radius))
            turning_radius = _turning_radius
            self.fleft.update(positionR(turning_radius, -angle))
            
        if self.steer == 0:
            angular_velocity = 0
            pos = self.velocity.rotate(-self.angle) * dt
            self.fleft.update(pos)
            self.rleft.update(pos)
            self.rright.update(pos)
            self.fright.update(pos)
        else:
            turning_radius = self.middle / sin(radians(self.steer))
            angular_velocity = self.speed / turning_radius
            if self.gear == 'D':
                if self.steer < 0:
                    gear_D_R(turning_radius)
                else:
                    gear_D_L(turning_radius)
            else:
                if self.steer < 0:
                    gear_R_R(turning_radius)
                else:
                    gear_R_L(turning_radius)    
        if self.gear == 'D':
            self.angle += degrees(angular_velocity) * dt
        else:
            self.angle -= degrees(angular_velocity) * dt
        self.angle = self.angle % 360
        self.speeding(dt)
        
    @property
    def velocity(self):
        if self.gear == 'R':
            return Vector2(-self.speed, 0)
        return Vector2(self.speed, 0)
    
    def speeding(self, dt):
        self.speed += self.acceleration * dt
        self.speed = max(0, min(20, self.speed))
        
    def steering(self, steer):
        self.steer += steer
        self.steer = max(-35, min(35, self.steer))
        
    def accelerating(self, acc):
        self.acceleration += acc
        self.acceleration = max(-20, min(3, self.acceleration))
        
    def draw(self, screen):
        # car
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect()
        position = (self.fleft.position+self.rleft.position) / 2
        position += (self.rright.position - self.rleft.position) / 2
        position -= (rect.width / 2, rect.height / 2)
        screen.blit(rotated, position)
        
        # fleft
        image = pygame.transform.rotate(
            self.fleft.surface , self.angle + self.steer
        )
        rect = image.get_rect(center=self.fleft.position)
        screen.blit(
            image, self.fleft.position - (rect.width / 2, rect.height / 2)
        )
        
        # rleft
        image = pygame.transform.rotate(self.rleft.surface , self.angle)
        rect = image.get_rect(center=self.rleft.position)
        screen.blit(
            image, self.rleft.position - (rect.width / 2, rect.height / 2)
        )
        
        # rright
        image = pygame.transform.rotate(self.rright.surface , self.angle)
        rect = image.get_rect(center=self.rright.position)
        screen.blit(
            image, self.rright.position - (rect.width / 2, rect.height / 2)
        )
        
        # fright
        image = pygame.transform.rotate(
            self.fright.surface , self.angle + self.steer
        )
        rect = image.get_rect(center=self.fright.position)
        screen.blit(
            image, self.fright.position - (rect.width / 2, rect.height / 2)
        )

    @property
    def image(self):
        if not hasattr(self, '_image'):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "car.png")
            self._image = pygame.image.load(image_path)
        return self._image
            
    def draw2(self, screen, trans):
        # trans = tuple(2*i for i in trans)
        # car
        rotated = pygame.transform.rotate(self.image, 90)
        screen.blit(rotated, -Vector2(32,64) + trans)
        
        # fleft
        image = pygame.transform.rotate(
            self.fleft.surface , self.steer + 90
        )
        rect = image.get_rect()
        screen.blit(
            image, Vector2(-50/2, -75/2) - (rect.width / 2, rect.height / 2) + trans
        )
        
        # rleft
        image = pygame.transform.rotate(self.rleft.surface , 90)
        rect = image.get_rect()
        screen.blit(
            image, Vector2(-50/2, 75/2) - (rect.width / 2, rect.height / 2) + trans
        )
        
        # rright
        image = pygame.transform.rotate(self.rright.surface , 90)
        rect = image.get_rect(center=self.rright.position)
        screen.blit(
            image, Vector2(50/2, 75/2) - (rect.width / 2, rect.height / 2) + trans
        )
        
        # fright
        image = pygame.transform.rotate(
            self.fright.surface , self.steer + 90
        )
        rect = image.get_rect(center=self.fright.position)
        screen.blit(
            image, Vector2(50/2, -75/2) - (rect.width / 2, rect.height / 2) + trans
        )
        
    
    def move(self, move):
        for tier in [self.fleft, self.rleft, self.rright, self.fright]:
            tier.position += move
    
    def rotate(self, angle):
        self.angle += angle
        
    def set_gear(self):
        if self.gear == 'D':
            self.gear = 'R'
        else:
            self.gear = 'D'


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        
        self.flag = 0

    def run(self, M):
        
        m = M()
        m2 = M()
        car = Car(*m.car)
        l = max(m.size)
        screen = pygame.display.set_mode(m.size)
        
        def flip(x):
            return Vector2(x.x, -x.y)
        while not self.exit:
            dt = self.clock.get_time() / 200

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

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
            # elif pressed[pygame.K_q]:
            #     car.rotate(1.2 * dt)
            # elif pressed[pygame.K_e]:
            #     car.rotate(-1.2 * dt)
            # elif pressed[pygame.K_BACKSPACE]:
            #     car.angle = 0
            
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
                car.steering(-10 * dt)
            elif pressed[pygame.K_LEFT]:
                car.steering(10 * dt)
            elif pressed[pygame.K_RETURN]:
                car.steer = 0
            
            if pressed[pygame.K_RCTRL]:
                car.gear = 'R'
            elif pressed[pygame.K_RSHIFT]:
                car.gear = 'D'

            # Logic
            car.update(dt)

            # Drawing
            screen.fill((0, 0, 0))
            
            image = pygame.transform.rotate(
                m2.surface , -car.angle + 90
            )
            x, y = m2.size
            angle = (- car.angle + 90) % 360
            if 0 <= angle and angle < 90:
                pt = Vector2(0, Vector2(x, 0).rotate(-car.angle + 90).y).rotate(car.angle - 90)
            if 90 <= angle and angle < 180:
                pt = Vector2(Vector2(x, 0).rotate(-car.angle + 90).x, Vector2(x, -y).rotate(-car.angle + 90).y).rotate(car.angle - 90)
                # pt = Vector2(Vector2(x, -y).rotate(-car.angle + 90).y, Vector2(x, 0).rotate(-car.angle + 90).x).rotate(car.angle - 90)
                # print(pt)
            if 180 <= angle and angle < 270:
                pt = Vector2(Vector2(x, -y).rotate(-car.angle + 90).x, Vector2(0, -y).rotate(-car.angle + 90).y).rotate(car.angle - 90)
            if 270 <= angle and angle < 360:
                pt = Vector2(Vector2(0, -y).rotate(-car.angle + 90).x, 0).rotate(car.angle - 90)
                
            # rect = orig_image.get_rect(center = (self.x, self.y))

# pivot = pygame_math.Vector2(self.x, self.y)

# p0 = (pygame.math.Vector2(rect.topleft) - pivot).rotate(-angle) + pivot
            # print(flip(-car.center+Vector2(m2.size[0]),0).rotate(-car.angle + 90))
            # print(-flip(car.center)+Vector2(m2.size[0],0))
            # print(pt)
            position = (-flip(car.center)+pt).rotate(-car.angle + 90)
            # print(position)
            screen.blit(
                image, flip(position) + m.size + (500,500)
            )
            
            car.draw2(screen, m.size)
            screen.blit(m.surface, (0,0))
            car.draw(screen)

            pygame.display.flip()
            self.clock.tick(self.ticks)
            
            if pressed[pygame.K_ESCAPE]:
                self.flag = 1
                break
            
        if self.flag == 1:
            self.flag = 0
            self.run(M)
        else:
            pygame.quit()
        
        
if __name__ == '__main__':
    game = Game()
    game.run(Map2)
