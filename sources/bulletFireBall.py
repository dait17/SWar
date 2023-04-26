import pygame

from bullets import *
from test import Test


class FireBall(Bullets):
    def __init__(self):
        super(FireBall, self).__init__()
        self.cooldownTime = 300
        self.levelMax = 9
        self.imgPath = '..\\assets\\img_bullet\\plasma.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 6
        self.size = [30,30]
        self.vel = 15
        self.dmd = 33
        self.durability = 1

    def getBullets(self, pos):
        bl = []
        degree = self._start_degree()
        for i in range(self.level):
            bullet = Bullet( self.img, pos, degree, self.size, self.vel, self.durability, self.dmd)
            bl.append(bullet)
            degree += self.d_degree
        self.time = pygame.time.get_ticks()
        return bl

    def readyShoot(self):
        return pygame.time.get_ticks()-self.time>self.cooldownTime

    def _start_degree(self):
        return -(self.level - 1) * self.d_degree / 2


