import pygame

from spaceship import Spaceship
from abc import ABC, abstractmethod
from handbleJson import *
from path import Path
from game import Game
from attackSystem import AttackSystem as Att
from messageBox import MessageBox as mb


class Bots:
    def __init__(self):
        pass

    @staticmethod
    def getBot(botName:str):
        botName = botName.upper()
        if botName == 'ALIEN':
            return BotAlien()

    @staticmethod
    def getGroupBot(botName, quantity:int):
        gb = []
        for _ in range(quantity):
            gb.append(Bots.getBot(botName))
        return gb


class BBot:
    def __init__(self):
        self.spaceship = None
        self.bullets = None

        self._moving = False

        self._pointRectX = None
        self._pointRectY = None

    def _loadShip(self, shipPath):
        data = readFile(shipPath)
        il = self._loadImgList(data.get('imgPathList'))
        return Spaceship(il,[-100,-100],data.get('size'), data.get('vel'), data.get('hp'), False)

    def _loadImgList(self, pathList:list):
        il = []
        for p in pathList:
            p = Path.getPath(p)
            if os.path.exists(p):
                il.append(pygame.image.load(p).convert_alpha())
        return il

    def _setPointRect(self, point:list):
        rect = pygame.Rect(0,0,self.spaceship.vel,self.spaceship.vel)

        self._pointRectY = rect.copy()
        self._pointRectY.width = Game.srect.width + 2000
        self._pointRectX = rect.copy()
        self._pointRectX.height = Game.srect.height + 2000
        if point[0] is not None:
            self._pointRectX.centerx = point[0]
            self._pointRectX.top = -1000
        else:
            self._pointRectX.centerx = self.spaceship.rect.centerx

        if point[1] is not None:
            self._pointRectY.centery = point[1]
            self._pointRectY.left = -1000
        else:
            self._pointRectY.centery = self.spaceship.rect.centery

    def setPoint(self, point:list):
        self._setPointRect(point)
        self._moving = True

    def _moveToPoint_1(self):
        if self._moving:
            sRect = pygame.Rect(0,0,self.spaceship.vel,self.spaceship.vel)
            sRect.center = self.spaceship.rect.center
            mb.show('sRect: ', sRect,[10,20])
            mb.show('pointX: ', self._pointRectX, [10,40])
            mb.show('pointY: ', self._pointRectY, [10,60])

            if not sRect.colliderect(self._pointRectX):
                if sRect.centerx<self._pointRectX.centerx:
                    self.spaceship.rect.centerx += self.spaceship.vel
                elif sRect.centerx>self._pointRectX.centerx:
                    self.spaceship.rect.centerx -= self.spaceship.vel

            elif not sRect.colliderect(self._pointRectY):
                if sRect.centery<self._pointRectY.centery:
                    self.spaceship.rect.centery += self.spaceship.vel
                else:
                    self.spaceship.rect.centery -= self.spaceship.vel
            else:
                self._moving = False

    def _moveToPoint_2(self):
        if self._moving:
            sRect = pygame.Rect(0,0,self.spaceship.vel,self.spaceship.vel)
            sRect.center = self.spaceship.rect.center
            mb.show('sRect: ', sRect,[10,20])
            mb.show('pointX: ', self._pointRectX, [10,40])
            mb.show('pointY: ', self._pointRectY, [10,60])

            moving = False

            if not sRect.colliderect(self._pointRectX):
                moving = True
                if sRect.centerx<self._pointRectX.centerx:
                    self.spaceship.rect.centerx += self.spaceship.vel
                elif sRect.centerx>self._pointRectX.centerx:
                    self.spaceship.rect.centerx -= self.spaceship.vel

            if not sRect.colliderect(self._pointRectY):
                moving = True
                if sRect.centery<self._pointRectY.centery:
                    self.spaceship.rect.centery += self.spaceship.vel
                else:
                    self.spaceship.rect.centery -= self.spaceship.vel
            self._moving = moving

    def showOrbit(self):
        if type(self._pointRectX) is pygame.Surface:
            Game.drawRect(self._pointRectX)
        if type(self._pointRectY) is pygame.Surface:
            Game.drawRect(self._pointRectY, (0,0,255))


class NormalBot(BBot):
    def __init__(self):
        super(NormalBot, self).__init__()
        self._movebyPoint = False
        self.pointList = []
        self._pointId = 0
        self.movementType = "1-D"

    def setPointList(self, pointList:list):
        self.pointList = pointList
        if len(self.pointList)>0:
            self._movebyPoint = True
            self._setPointRect(self.getCurPoint())
            self._moving = True

    def getCurPoint(self):
        if self._movebyPoint:
            if self._pointId>=len(self.pointList):
                self._pointId = 0
            return self.pointList[self._pointId]
        return [None, None]

    def _move(self):
        if self.movementType=="1-D":
            self._moveToPoint_1()
        elif  self.movementType=="2-D":
            self._moveToPoint_2()

    def _handleMove(self):
        self._move()
        if not self._moving and self._movebyPoint:
            self._pointId += 1
            self.setPoint(self.getCurPoint())


class BotAlien(NormalBot):
    def __init__(self):
        super(BotAlien, self).__init__()
        self.path = '..\\assets\\Bot\\alien.json'
        self.spaceship = self._loadShip(self.path)
        self.bullets = Att.getBullets("fireball")
        self.movementType = "2-D"

    def update(self):
        self.showOrbit()
        self.spaceship.update()
        self._handleMove()










