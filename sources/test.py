import sys

import pygame


class Test:
    obList = []

    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.srect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60

    def _loadBG(self):
        pass

    @staticmethod
    def add(*args):
        for ob in list(args):
            Test.obList.append(ob)

    @staticmethod
    def extend(ls):
        for ob in ls:
            Test.obList.append(ob)

    def removeOB(self, ob):
        try:
            self.obList.remove(ob)
        except Exception:
            return False
        return Test

    def removeDisable(self, ob):
        try:
            if not ob.enable:
                return self.removeOB(ob)
        except Exception:
            return False

    def update(self):
        for ob in self.obList:
            ob.update()
            self.removeDisable(ob)


    def run(self):
        while True:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.fps)

