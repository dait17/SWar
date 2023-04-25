import pygame
import math


class SBullet:
    def __init__(self, img,size, vel, durability, dmg):
        self.img = img
        self.rect = self._getRect(size)
        self.vel = vel
        self.durability = durability
        self.dmg = dmg
        self.screen = pygame.display.get_surface()
        self._sret = self.screen.get_rect()
        self.area = pygame.Rect(-50, -50, self._sret.width+50, self._sret.height+50)
        self.enable = True

    def _getRect(self, size):
        return pygame.Rect(0,0,size[0], size[1])

    def _getImg(self, size):
        if type(self.img) is pygame.Surface:
            return pygame.transform.smoothscale(self.img, size)
        return pygame.Surface(self.rect.size).convert_alpha()

    def _draw(self):
        self.screen.blit(self._getImg(self.rect.size), self.rect)

    def goto(self,x,y):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y


class Bullet(SBullet):
    def __init__(self,degree,img,size, vel, durability, dmg):
        super(Bullet, self).__init__(img,size, vel, durability, dmg)
        self.degree = degree
        self._d_pos = self._getD()

    def _getD(self):
        dx = self.vel * math.sin(self.degree * math.pi / 180)
        dy = abs(self.vel * math.cos(self.degree * math.pi / 180))
        if 0 < self.degree < 180:
            dy  = -dy
        return [dx,dy]

    def _movement(self):
        self.rect.x += self._d_pos[0]
        self.rect.y = self._d_pos[1]
        if not self.rect.colliderect(self.area):
            self.enable = False

    def collide(self):
        self.durability -= 1
        if self.durability <=0:
            self.enable = False

    def update(self):
        if self.enable:
            self._movement()
            self._draw()



    def get(self):
        print(self._getD())


if __name__ == '__main__':
    b = Bullet(10, None, [50,50], 2, 1, 35)
    b.get()





