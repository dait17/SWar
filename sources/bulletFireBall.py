

from bullets import *
from test import Test


class FireBall(Bullets):
    def __init__(self):
        super(FireBall, self).__init__()
        self.levelMax = 9
        self.imgPath = '..\\assets\\img_bullet\\plasma.png'
        self.img = self._getImg(self.imgPath)
        self.d_degree = 6
        self.vel = 10
        self.dmd = 33
        self.durability = 1

    def getBullets(self, pos):
        bl = []
        degree = self._start_degree()

        for i in range(self.level):
            print(degree)
            bullet = Bullet(self.img, pos,degree, [20,20], self.vel, self.durability,self.dmd)
            bl.append(bullet)
            degree += self.d_degree
        return bl

    def _start_degree(self):
        return -(self.level-1)*self.d_degree/2

if __name__ == '__main__':
    T = Test()
    F = FireBall()
    F.setLevel(3)
    T.extend(F.getBullets([400,600]))
    # T.extend(F.getBullets([400,600]))
    T.run()
