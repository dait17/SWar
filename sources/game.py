import sys, os

import pygame
from gameTools import *


class Game:
    frame = None
    map = None
    playing = False
    enemyList = []
    bullEnemyList = []

    playerList = []
    bullPlayerList = []

    itemList = []

    screen = pygame.display.get_surface()
    srect = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60
    bg = None

    # Event
    EventBotDefeat = False
    EventBotDefeatPos = None

    def __init__(self):
        pass

    @staticmethod
    def setup():
        Game.map = None
        Game.enemyList = []
        Game.bullEnemyList = []

        Game.bullPlayerList = []

        Game.itemList = []

    @staticmethod
    def setFrame(frame):
        Game.frame = frame

    @staticmethod
    def setMap(map):
        Game.setup()
        Game.playing = True
        Game.map = map

    @staticmethod
    def drawBackground():
        if type(Game.bg) is pygame.Surface:
            Game.screen.blit(Game.bg, (0, 0))
        else:
            Game.screen.fill((255, 255, 255))

    @staticmethod
    def showSurface(sur, pos):
        if type(sur) is pygame.Surface:
            Game.screen.blit(sur, pos)

    @staticmethod
    def drawRect(rect, color=(0, 255, 0), width=0, border_radius=-1):
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
    def _removeShipDisable(orLs: list, ship):
        try:
            if not ship.spaceship.enable:
                Game._removeOB(orLs, ship)
        except Exception:
            return False
        return True

    @staticmethod
    def AddItem(*items):
        for item in list(items):
            Game.itemList.append(item)

    @staticmethod
    def AddPlayer(*player):
        Game._add(Game.playerList, *player)

    @staticmethod
    def AddEnemy(*enemy):
        Game._add(Game.enemyList, *enemy)

    @staticmethod
    def ExtendEnemy(enemyList):
        for e in enemyList:
            Game._add(Game.enemyList, e)

    @staticmethod
    def setPlayer(playerList):
        Game.playerList = playerList

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

    @staticmethod
    def blit(sur, rect):
        Game.screen.blit(sur, rect)

    @staticmethod
    def _updateFrame():
        if not Game.playing and Game.frame is not None:
            Game.frame.update()

    @staticmethod
    def _updateMap():
        if Game.playing and Game.map is not None:
            Game.map.update()
            if not Game.map.enable:
                Game.playing = False

    @staticmethod
    def _updateItem():
        for item in Game.itemList:
            item.update()
            Game._removeDisable(Game.itemList, item)

    @staticmethod
    def _updatePlayer():
        for p in Game.playerList:
            p.update()
            for e in Game.enemyList:
                if p.spaceship.getCurRect().colliderect(e.spaceship.getCurRect()):
                    p.spaceship.beShot(100)
                    p.spaceship.moveTo(0, 20, 20)
                    p.spaceship.noHit()
                    e.spaceship.beShot(100)
                    # e.spaceship.moveTo(0, -20, 20)
                    e.spaceship.noHit()
            Game._removeShipDisable(Game.playerList, p)

    @staticmethod
    def _updateEnemy():
        Game.EventBotDefeat = False
        Game.EventBotDefeatPos = None
        for e in Game.enemyList:
            e.update()
            pos = e.spaceship.getCurRect().center
            if Game._removeShipDisable(Game.enemyList, e):
                Game.EventBotDefeat = True
                Game.EventBotDefeatPos = pos

    @staticmethod
    def _updatePlayerBullet():
        for b in Game.bullPlayerList:
            b.update()
            for e in Game.enemyList:
                if b.collide(e.spaceship.rect):
                    e.spaceship.beShot(b.dmg)
            Game._removeDisable(Game.bullPlayerList, b)

    @staticmethod
    def _updateEnemyBullet():
        for b in Game.bullEnemyList:
            b.update()
            for p in Game.playerList:
                if b.collide(p.spaceship.getCurRect()):
                    p.spaceship.beShot(b.dmg)
            Game._removeDisable(Game.bullEnemyList, b)

    @staticmethod
    def update():
        if Game.playing:
            Game._updateMap()
            Game._updateItem()
            Game._updatePlayerBullet()
            Game._updateEnemyBullet()
            Game._updatePlayer()
            Game._updateEnemy()
        else:
            Game._updateFrame()

    @staticmethod
    def run():
        while True:
            Game.drawBackground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            Game.update()
            pygame.display.flip()
            Game.clock.tick(Game.fps)


if __name__ == '__main__':
    a = [2, 3, 4]
    # G = Game()
    # G.AddPlayer(2,3,4)
    # print(G.playerList)
