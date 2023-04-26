import pygame, os
import math
from abc import ABC, abstractmethod
from path import Path as P


class Bullets(ABC):
    def __init__(self):
        self.cooldownTime = 500 #ms
        self.time = 0
        self.imgPath = ''
        self.img = None
        self.level = 1
        self.levelMax = 1

    def _controlLevel(self, level):
        if 1<=level<+self.levelMax:
            return level
        elif level<=0:
            return 1
        return self.levelMax

    def _getImg(self, imgPath):
        imgPath = P.getPath(imgPath)
        if os.path.exists(imgPath):
            return pygame.image.load(imgPath).convert_alpha()
        return None

    def levelUP(self):
        self.level = self._controlLevel(self.level+1)

    def setLevel(self, value:int):
        self.level = self._controlLevel(value)

    @abstractmethod
    def getBullets(self, pos:list):
        pass


class SBullet:
    def __init__(self, img, pos, degree,size, vel, durability, dmg):
        self.degree = degree
        self.rect = self._getRect(pos, size)
        self._x = self.rect.centerx
        self._y = self.rect.centery
        self.img = self._getImg(img)

        self.vel = vel
        self.durability = durability
        self.dmg = dmg
        self.screen = pygame.display.get_surface()
        self._sret = self.screen.get_rect()
        self.area = pygame.Rect(-50, -50, self._sret.width+50, self._sret.height+50)
        self.enable = True

    def _getRect(self, pos,size):
        rect = pygame.Rect(0,0,size[0], size[1])
        rect.center = pos
        return rect

    def _getImg(self, img):
        if type(img) is pygame.Surface:
            newImg  = pygame.transform.smoothscale(img, self.rect.size)
            newImg = pygame.transform.rotate(newImg, -self.degree)
            return newImg
        return pygame.Surface(self.rect.size).convert_alpha()

    def _draw(self):
        self.screen.blit(self.img, self.rect)

    def goto(self,x,y):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    def gotoPos(self, pos):
        self.rect.center = pos


class Bullet(SBullet):
    def __init__(self,img,pos, degree,size, vel, durability, dmg):
        super(Bullet, self).__init__(img, pos,degree,size, vel, durability, dmg)
        self.start = pos
        self.end = [0,0]
        self._d_pos = self._getD()


    def _getD(self):
        dx = self.vel * math.sin(self.degree * math.pi / 180)
        dy = abs(self.vel * math.cos(self.degree * math.pi / 180))
        if -90 <= self.degree <= 90:
            dy = -dy
        self.end = [self.start[0]+dx*1000, self.start[1]+dy*1000]
        return [dx,dy]

    def _movement(self):
        self._x += self._d_pos[0]
        self._y += self._d_pos[1]
        self.gotoPos([self._x, self._y])
        if not self.rect.colliderect(self.area):
            self.enable = False

    def collide(self):
        self.durability -= 1
        if self.durability <=0:
            self.enable = False

    def update(self):
        # pygame.draw.line(self.screen, (0,0,255), self.start, self.end)
        if self.enable:
            self._movement()
            self._draw()





