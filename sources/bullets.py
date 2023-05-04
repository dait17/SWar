import pygame, os
import math
from abc import ABC, abstractmethod
from path import Path as P
from messageBox import MessageBox


class Bullets(ABC):
    def __init__(self):
        self.cooldownTime = 0  # ms
        self.recoil = 0
        self.time = pygame.time.get_ticks()
        self.imgPath = ''
        self.img = None
        self.level = 1
        self.levelMax = 1
        self.size = [20, 20]
        self.dmg = 40
        self.durability = 1
        self.vel = 10

    def _controlLevel(self, level):
        if 1 <= level < +self.levelMax:
            return level
        elif level <= 0:
            return 1
        return self.levelMax

    def _getImg(self, imgPath):
        imgPath = P.getPath(imgPath)
        if os.path.exists(imgPath):
            return pygame.image.load(imgPath).convert_alpha()
        return None

    def levelUP(self):
        self.level = self._controlLevel(self.level + 1)

    def setLevel(self, value: int):
        self.level = self._controlLevel(value)

    def _getBLDiagonalDB(self, degree, stPos, centerPos):
        x, y = stPos
        b1 = Bullet(self.img, [x, y], degree, self.size, self.vel, self.durability, self.dmg)
        x = centerPos[0] + centerPos[0] - x
        b2 = Bullet(self.img, [x, y], -degree, self.size, self.vel, self.durability, self.dmg)
        return [b1, b2]

    @abstractmethod
    def getBullets(self, pos: list):
        pass


class SBullet:
    def __init__(self, img, pos, degree, size, vel, durability, dmg):
        self.degree = degree
        self.rect = self._getRect(pos, size)
        self._x = self.rect.centerx
        self._y = self.rect.centery
        self.img = self._getImg(img)
        self.curImg = None

        self.vel = vel
        self.durability = durability
        self.dmg = dmg
        self.screen = pygame.display.get_surface()
        self._sret = self.screen.get_rect()
        self.area = pygame.Rect(0, 0, self._sret.width, self._sret.height)
        self.enable = True

        # Effect
        self._rotateEffect = False
        self._eRIV = 1
        self._curD = 0

    def __fit_rect_img(self, rect, img: pygame.Surface):
        new_width = rect.width
        new_height = rect.height
        if type(img) is pygame.Surface:
            img_rect = img.get_rect()
            new_height = int(img_rect.height * (rect.width / img_rect.width))
        return new_width, new_height

    def _getRect(self, pos, size):
        rect = pygame.Rect(0, 0, size[0], size[1])
        rect.center = pos
        return rect

    def _getImg(self, img):
        if type(img) is pygame.Surface:
            w, h = self.__fit_rect_img(self.rect, img)
            center = self.rect.center
            if h > self.rect.height * 4 / 3:
                h = self.rect.height * 4 / 3
            self.rect.size = [w, h]
            self.rect.center = center
            newImg = pygame.transform.smoothscale(img, self.rect.size)
            newImg = pygame.transform.rotate(newImg, -self.degree)
            self.__fit_rect_img(self.rect, newImg)

            return newImg
        return pygame.Surface(self.rect.size).convert_alpha()

    def _draw(self):
        self.screen.blit(self.curImg, self.rect)

    def goto(self, x, y):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    def _effectRotateImg(self):
        self._curD += self._eRIV
        if self._curD >= 360:
            self._curD = 0
        try:
            self.curImg = pygame.transform.rotate(self.img, self._curD)
        except Exception as e:
            print(e)

    def _effect(self):
        if self._rotateEffect:
            self._effectRotateImg()
        else:
            if self.img is not None:
                self.curImg = self.img.copy()

    def setEffect(self, rotaImg: bool = True, V=1):
        self._rotateEffect = rotaImg
        self._eRIV = V

    def gotoPos(self, pos):
        self.rect.center = pos


class Bullet(SBullet):
    def __init__(self, img, pos, degree, size, vel, durability, dmg):
        super(Bullet, self).__init__(img, pos, degree, size, vel, durability, dmg)
        self.start = pos
        self._d_pos = self._getD()

    def _getD(self):
        dx = self.vel * math.sin(self.degree * math.pi / 180)
        dy = abs(self.vel * math.cos(self.degree * math.pi / 180))
        if (-90 <= self.degree <= 90) or (-360 <= self.degree <= -270) or (270 <= self.degree <= 360):
            dy = -dy
        return [dx, dy]

    def _movement(self):
        self._x += self._d_pos[0]
        self._y += self._d_pos[1]
        self.rect.center = [self._x, self._y]
        if not self.rect.colliderect(self.area):
            self.enable = False

    def collide(self, rect: pygame.Rect):
        if self.rect.colliderect(rect):
            self.durability -= 1
            if self.durability <= 0:
                self.enable = False
            return True
        return False

    def update(self):
        if self.enable:
            self._movement()
            self._effect()
            self._draw()
