import pygame

from bullets import *
from test import Test


class FireBall(Bullets):
    def __init__(self):
        super(FireBall, self).__init__()
        self.cooldownTime = 300
        self.recoil = 15
        self.levelMax = 9
        self.imgPath = '..\\assets\\img_bullet\\fireball1.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 6
        self.size = [30,30]
        self.vel = 20
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


class SuperBlue(Bullets):
    def __init__(self):
        super(SuperBlue, self).__init__()
        self.cooldownTime = 200
        self.recoil = 10
        self.levelMax = 7
        self.imgPath = '..\\assets\\img_bullet\\bl1.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 6
        self.size = [15,25]
        self.vel = 20
        self.dmd = 40
        self.durability = 1

    def getBullets(self, pos):
        bl = []
        if self.level==1:
            bl = self._getBL1(pos)
        elif self.level==2:
            bl = self._getBL2(pos)
        elif self.level==3:
            bl = self._getBL3(pos)
        elif self.level==4:
            bl = self._getBL4(pos)
        elif self.level==5:
            bl = self._getBL5(pos)
        elif self.level==6:
            bl = self._getBL6(pos)
        elif self.level==7:
            bl = self._getBL7(pos)

        self.time = pygame.time.get_ticks()
        return bl
        # bl = []
        # degree = self._start_degree()
        # for i in range(self.level):
        #     bullet = Bullet( self.img, pos, degree, self.size, self.vel, self.durability, self.dmd)
        #     bl.append(bullet)
        #     degree += self.d_degree
        # self.time = pygame.time.get_ticks()
        # return bl

    def _getBL1(self, pos):
        return [Bullet( self.img, pos, 0, self.size, self.vel, self.durability, self.dmd)]

    def _getBL2(self, pos, dx:int=20):
        x, y = pos
        b1 = Bullet( self.img, [x-dx,y], 0, self.size, self.vel, self.durability, self.dmd)
        b2 = Bullet( self.img, [x+dx,y], 0, self.size, self.vel, self.durability, self.dmd)
        return [b1,b2]

    def _getBL3(self, pos):
        bl = []
        d_degree = 6
        degree = self._start_degree(d_degree)
        x, y = pos
        x -= 10
        for i in range(3):
            bullet = Bullet( self.img, [x,y], degree, self.size, self.vel, self.durability, self.dmd)
            bl.append(bullet)
            degree += d_degree
            x += 10
        return bl

    def _getBL4(self, pos):
        bl = []
        x,y = pos
        bl.extend(self._getBL2(pos, 10))
        x -= 20
        bl.extend(self._getBLDiagonalDB(-10, [x,y], pos))
        return bl

    def _getBL5(self, pos):
        bl = []
        x,y = pos
        bl.extend(self._getBL1(pos))
        x -= 10
        bl.extend(self._getBLDiagonalDB(-6, [x,y], pos))
        x -= 5
        bl.extend(self._getBLDiagonalDB(-10, [x,y], pos))
        return bl

    def _getBL6(self, pos):
        bl = []
        x,y = pos
        bl.extend(self._getBL2(pos, 10))
        x -= 15
        bl.extend(self._getBLDiagonalDB(-12, [x,y], pos))
        x -= 5
        bl.extend(self._getBLDiagonalDB(-16, [x,y], pos))
        return bl

    def _getBL7(self, pos):
        bl = []
        x,y = pos
        bl.extend(self._getBL1(pos))
        bl.extend(self._getBL2(pos, 15))
        x -= 15
        bl.extend(self._getBLDiagonalDB(-14, [x,y], pos))
        x -= 5
        bl.extend(self._getBLDiagonalDB(-18, [x,y], pos))
        return bl

    def readyShoot(self):
        return pygame.time.get_ticks()-self.time>self.cooldownTime

    def _start_degree(self, d_degree):
        return -(self.level - 1) * d_degree / 2


if __name__ == '__main__':
    from game import Game
    from player import Player
    Game.playing = True
    player = Player()
    player.setBullets('superblue')
    player.bullets.setLevel(6)
    Game.AddPlayer(player)
    Game.run()
