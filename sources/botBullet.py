import random

from bullets import *


class BotBullet1(Bullets):
    def __init__(self):
        super(BotBullet1, self).__init__()
        self.cooldownTime = random.randint(1000, 3000)
        self.recoil = 30
        self.levelMax = 3
        self.imgPath = '..\\assets\\img_bullet\\slime.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 30
        self.size = [30, 30]
        self.vel = 2
        self.dmd = 40
        self.durability = 1

    def getBullets(self, pos):
        bl = []
        degree = self._start_degree()
        for i in range(self.level):
            bullet = Bullet(self.img, pos, degree, self.size, self.vel, self.durability, self.dmd)
            bl.append(bullet)
            degree += self.d_degree
        self.time = pygame.time.get_ticks()
        return bl

    def readyShoot(self):
        return pygame.time.get_ticks() - self.time > self.cooldownTime

    def _start_degree(self):
        return -(180 + (self.level - 1) * self.d_degree / 2)


# ***************************************************************************


class BotSpecialBullet1(Bullets):
    def __init__(self):
        super(BotSpecialBullet1, self).__init__()
        self.cooldownTime = random.randint(1000, 3000)
        self.recoil = 30
        self.levelMax = 6
        self.imgPath = '..\\assets\\img_bullet\\shuriken.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 32
        self.size = [30, 30]
        self.vel = 4
        self.dmd = 40
        self.durability = 1

    def getBullets(self, pos):
        bl = []
        degree = self._start_degree()
        for i in range(self.level * 2 - 1):
            bullet = Bullet(self.img, pos, degree, self.size, self.vel, self.durability, self.dmd)
            bullet.setEffect(True, 10)
            bl.append(bullet)
            degree += self.d_degree
        self.time = pygame.time.get_ticks()
        return bl

    def readyShoot(self):
        return pygame.time.get_ticks() - self.time > self.cooldownTime

    def _start_degree(self):
        return -(180 + (self.level * 2 - 2) * self.d_degree / 2)


if __name__ == '__main__':
    from game import Game
    from player import Player

    bullets = BotSpecialBullet1()

    Game.playing = True
    Game.AddPlayer(Player())
    Game.ExtendEnemyBullet(bullets.getBullets([400, 400]))

    Game.run()
