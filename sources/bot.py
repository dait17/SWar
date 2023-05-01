import random

import pygame

from spaceship import Spaceship
from gameTools import *
from game import Game
from attackSystem import AttackSystem as Att


class Bots:
    def __init__(self):
        pass

    @staticmethod
    def getBot(botName:str):
        botName = botName.upper()
        bot = None
        if botName == 'ALIEN':
            bot = BotAlien()
        if bot is not  None:
            bot.spaceship.setShowHp(True, True)
        return bot

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
        self._pointRect =None

        self._pointRectX = None
        self._pointRectY = None

    def _loadShip(self, shipPath):
        data = HandleJson.readFile(shipPath)
        il = self._loadImgList(data.get('imgPathList'))
        sp = Spaceship(il,[-100,-100],data.get('size'), data.get('vel'), data.get('hp'), False)
        return sp

    def _loadImgList(self, pathList:list):
        il = []
        for p in pathList:
            p = Path.getPath(p)
            if os.path.exists(p):
                il.append(pygame.image.load(p).convert_alpha())
        return il

    def _setPointRect(self, point:list):
        rect = pygame.Rect(0,0,self.spaceship.vel,self.spaceship.vel)
        self._pointRect = rect.copy()
        self._pointRect.center = point

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

    def __moveX(self, sRect, twoAxis:bool=False):
        hadMove = True
        if sRect.centerx < self._pointRect.centerx:
            self.spaceship.rect.centerx += self.spaceship.vel
        elif sRect.centerx > self._pointRect.centerx:
            self.spaceship.rect.centerx -= self.spaceship.vel
        else:
            hadMove = False

        if hadMove and not twoAxis:
            return

        if sRect.centery < self._pointRect.centery:
            self.spaceship.rect.centery += self.spaceship.vel
        elif sRect.centery > self._pointRect.centery:
            self.spaceship.rect.centery -= self.spaceship.vel

    def __moveY(self, sRect,twoAxis:bool=False):
        hadMove = True
        if sRect.centery < self._pointRect.centery:
            self.spaceship.rect.centery += self.spaceship.vel
        elif sRect.centery > self._pointRect.centery:
            self.spaceship.rect.centery -= self.spaceship.vel
        else:
            hadMove = False
        if hadMove and not twoAxis:
            return
        if sRect.centerx < self._pointRect.centerx:
            self.spaceship.rect.centerx += self.spaceship.vel
        elif sRect.centerx > self._pointRect.centerx:
            self.spaceship.rect.centerx -= self.spaceship.vel

    def _moveToPoint(self, X:bool=True, Y: bool=False):
        # print(self._pointRect.center)
        if self._moving:
            sRect = pygame.Rect(0, 0, self.spaceship.vel, self.spaceship.vel)
            sRect.center = self.spaceship.rect.center
            if not sRect.colliderect(self._pointRect):
                if X and Y:
                    self.__moveX(sRect, True)
                elif X:
                    self.__moveX(sRect)
                elif Y:
                    self.__moveY(sRect)
                else:
                    self.__moveY(sRect, True)

            else:
                self._moving = False

    def _shot(self):
        if self.bullets is None:
            return
        shot = random.choice([True, False])
        if shot and self.bullets.readyShoot():
            bl = self.bullets.getBullets(self.spaceship.getBulletPos())
            Game.ExtendEnemyBullet(bl)
            self.spaceship.shotEffect(self.bullets.recoil)


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
            self._moveToPoint()
        elif  self.movementType=="2-D":
            self._moveToPoint(True, True)
        elif self.movementType=="D-1":
            self._moveToPoint(False, True)
        elif  self.movementType=="D-2":
            self._moveToPoint(False, False)
        else:
            self._moveToPoint()

    def _handleMove(self):
        self._move()
        if not self._moving and self._movebyPoint:
            self._pointId += 1
            self.setPoint(self.getCurPoint())


class AutoBot(BBot):
    def __init__(self):
        super(AutoBot, self).__init__()
        self._area = self._getArea()
        self.movementType = "1-D"
        self._rest = False
        self._restRate = 0.5
        self._resting = False
        self._time = 0
        self._changeTypeMoveTime = pygame.time.get_ticks()+random.randint(5000, 15000)

    def setRest(self, value:bool=True, rate = 0.5):
        self._rest = value
        self._restRate = rate

    def _getArea(self):
        area = Screen.sRect.copy()
        area.height = Screen.sRect.height*5//8
        return area

    def _getRandomPoint(self):
        x = random.randint(self._area.left, self._area.right)
        y = random.randint(self._area.top, self._area.bottom)
        return [x,y]

    def _createRestListChoice(self):
        t = [True for _ in range(int(self._restRate*10))]
        f = [False for _ in range(int((1-self._restRate)*10))]
        t.extend(f)
        return t

    def _getRest(self):
        return random.choice(self._createRestListChoice())

    def _autoMove(self):
        if not self._moving:
            if self._rest and not self._resting and not self._getRest():
                self._resting = True
                self._time = pygame.time.get_ticks()
            if not self._resting:
                randomPoint = self._getRandomPoint()
                self.setPoint(randomPoint)
            else:
                if pygame.time.get_ticks()-self._time>=1000:
                    self._resting = False

    def _changeMoveType(self):
        if pygame.time.get_ticks()-self._changeTypeMoveTime>=0:
            self.movementType = random.choice(['1-D', '2-D', 'D-1', 'D-2'])
            self._changeTypeMoveTime = pygame.time.get_ticks()+random.randint(3000, 10000)

    def _move(self):
        if self.movementType=="1-D":
            self._moveToPoint()
        elif self.movementType=="2-D":
            self._moveToPoint(True, True)
        elif self.movementType=="D-1":
            self._moveToPoint(False, True)
        elif self.movementType=="D-2":
            self._moveToPoint(False, False)
        else:
            self._moveToPoint()

# **********************************************************************


class BotDragDoll(AutoBot):
    def __init__(self):
        super(BotDragDoll, self).__init__()
        self.path = "..\\assets\\Bot\\dragdoll.json"
        self.spaceship = self._loadShip(self.path)
        self.bullets = Att.getBullets('BotBullet1')
        self.movementType = "D-2"
        self.setRest()
        self._dragdollBehav = False
        self._timeDragdoll = 30000
        self._dragdollTime = pygame.time.get_ticks()

    def _handleBehaviour(self):
        if not self._dragdollBehav and pygame.time.get_ticks()-self._dragdollTime>=self._timeDragdoll:
            self._dragdollBehav = True
            self.setPoint([self.spaceship.rect.centerx, Screen.sRect.height+1000])
            self.spaceship.vel += 5
            self.spaceship.setSize([40, 40])
            self.bullets = None

    def _handleMove(self):
        self._handleBehaviour()
        if not self._dragdollBehav:
            self._autoMove()
        else:
            if not Screen.sRect.colliderect(self.spaceship.rect):
                self.spaceship.enable = False

    def update(self):
        self._changeMoveType()
        self._handleMove()
        self._move()
        self._shot()
        self.spaceship.update()




# **********************************************************************


class BotAlien(NormalBot):
    def __init__(self):
        super(BotAlien, self).__init__()
        self.path = '..\\assets\\Bot\\alien.json'
        self.spaceship = self._loadShip(self.path)
        self.bullets = Att.getBullets("BotBullet1")
        # self.movementType = "2-D"
        self.movementType = "D-2"

    def update(self):
        self._shot()
        self.spaceship.update()
        self._handleMove()


if __name__ == '__main__':

    bot = BotDragDoll()
    # bot.setPointList([[200,400]])
    Game.playing = True
    Game.AddEnemy(bot)

    Game.run()









