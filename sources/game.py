import sys, os

import pygame
from path import Path as P


class Game:
    enemyList = []
    bullEnemyList = []

    playerList = []
    bullPlayerList = []

    screen = pygame.display.set_mode((1300, 750))
    srect = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60
    bg = None

    def __init__(self):
        pass

    @staticmethod
    def _loadBG(path):
        path = P.getPath(path)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, Game.srect.size)
        return None

    @staticmethod
    def setBackground(path):
        Game.bg = Game._loadBG(path)

    def drawBackground(self):
        if type(Game.bg) is pygame.Surface:
            Game.screen.blit(Game.bg, (0,0))
        else:
            Game.screen.fill((255,255,255))

    @staticmethod
    def showSurface(sur, pos):
        if type(sur) is pygame.Surface:
            Game.screen.blit(sur,pos)

    @staticmethod
    def drawRect(rect, color=(0,255,0), width=0, border_radius = -1):
        pygame.draw.rect(Game.screen, color, rect, width, border_radius)

    @staticmethod
    def _add(orLs: list, *args):
        for ob in list(args):
            orLs.append(ob)

    @staticmethod
    def _extend(orLs: list, ls: list):
        for ob in ls:
            orLs.append(ob)

    @staticmethod
    def _removeOB(orLs: list, ob):
        try:
            orLs.remove(ob)
        except Exception:
            return False
        return True

    @staticmethod
    def _removeDisable(orLs: list, ob):
        try:
            if not ob.enable:
                Game._removeOB(orLs, ob)
        except Exception:
            return False
        return True

    @staticmethod
    def AddPlayer(*player):
        Game._add(Game.playerList, *player)

    @staticmethod
    def AddEnemy(*enemy):
        print(enemy)
        Game._add(Game.enemyList, *enemy)

    @staticmethod
    def ExtendEnemy(enemyList):
        for e in enemyList:
            Game._add(Game.enemyList, e)

    @staticmethod
    def AddPlayerBullet(*bullets):
        Game._add(Game.bullPlayerList, *bullets)

    @staticmethod
    def ExtendPlayerBullet(bullets):
        Game._extend(Game.bullPlayerList, bullets)

    @staticmethod
    def AddEnemyBullet(*bullets):
        Game._add(Game.bullEnemyList, *bullets)

    @staticmethod
    def ExtendEnemyBullet(bullets):
        Game._extend(Game.bullEnemyList, bullets)

    def _updatePlayer(self):
        for p in Game.playerList:
            p.update()

    def _updateEnemy(self):
        for e in Game.enemyList:
            e.update()

    def _updatePlayerBullet(self):
        for b in Game.bullPlayerList:
            b.update()
            Game._removeDisable(Game.bullPlayerList, b)

    def _updateEnemyBullet(self):
        for b in Game.bullEnemyList:
            b.update()
            Game._removeDisable(Game.bullEnemyList, b)

    def update(self):
        self._updatePlayer()
        self._updateEnemy()
        self._updatePlayerBullet()

    def run(self):
        while True:
            self.drawBackground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    a = [2, 3, 4]
    # G = Game()
    # G.AddPlayer(2,3,4)
    # print(G.playerList)
