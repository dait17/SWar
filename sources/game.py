import sys

import pygame


class Game:
    enemyList = []
    bullEnemyList = []

    playerList = []
    bullPlayerList = []

    screen = pygame.display.set_mode((1300, 750))
    srect = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60

    def __init__(self):
        pass

    def _loadBG(self):
        pass

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
        Game._add(Game.enemyList, *enemy)

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
        self._updatePlayerBullet()

    def run(self):
        while True:
            self.screen.fill((255, 255, 255))
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
