import pygame


class SBullet:
    def __init__(self, img,size, vel, durability, dmg):
        self.img = img
        self.rect = self._getRect(size)
        self.vel = vel
        self.durability = durability
        self.dmg = dmg
        self.screen = pygame.display.get_surface()

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