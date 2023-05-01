import random

import pygame

from spaceship import Spaceship
from gameTools import *
from game import Game
from attackSystem import AttackSystem as Att
from sound import Sound


class Bots:
    def __init__(self):
        pass

    @staticmethod
    def getBot(botName: str):
        botName = botName.upper()
        bot = None
        if botName == 'ALIEN':
            bot = BotAlien()
        elif botName == 'DRAGDOLL':
            bot = BotDragDoll()
        elif botName == 'BOSS1':
            bot = Boss1()
        if bot is not None:
            bot.spaceship.setShowHp(True, True)
        return bot

    @staticmethod
    def getGroupBot(botName, quantity: int):
        gb = []
        for _ in range(quantity):
            gb.append(Bots.getBot(botName))
        return gb


class BBot:
    def __init__(self):
        self.spaceship = None
        self.bullets = None

        self._moving = False
        self._pointRect = None

        self._timeShot = pygame.time.get_ticks() + random.randint(2000,10000)


    def _loadShip(self, shipPath):
        data = HandleJson.readFile(shipPath)
        il = self._loadImgList(data.get('imgPathList'))
        sp = Spaceship(il, [-100, -100], data.get('size'), data.get('vel'), data.get('hp'), False)
        sp.setExplosionSound(Sound.botExplosionSound)
        return sp

    def _loadImgList(self, pathList: list):
        il = []
        for p in pathList:
            p = Path.getPath(p)
            if os.path.exists(p):
                il.append(pygame.image.load(p).convert_alpha())
        return il

    def _setPointRect(self, point: list):
        rect = pygame.Rect(0, 0, self.spaceship.vel * 2, self.spaceship.vel * 2)
        self._pointRect = rect.copy()
        self._pointRect.center = point

    def setPoint(self, point: list):
        self._setPointRect(point)
        self._moving = True

    def __moveX(self, sRect, twoAxis: bool = False):
        hadMove = True
        if not (
                self._pointRect.left < sRect.centerx < self._pointRect.right) and sRect.centerx < self._pointRect.centerx:
            self.spaceship.rect.centerx += self.spaceship.vel
        elif not (
                self._pointRect.left < sRect.centerx < self._pointRect.right) and sRect.centerx > self._pointRect.centerx:
            self.spaceship.rect.centerx -= self.spaceship.vel
        else:
            hadMove = False

        if hadMove and not twoAxis:
            return

        if not (
                self._pointRect.top < sRect.centery < self._pointRect.bottom) and sRect.centery < self._pointRect.centery:
            self.spaceship.rect.centery += self.spaceship.vel
        elif not (
                self._pointRect.top < sRect.centery < self._pointRect.bottom) and sRect.centery > self._pointRect.centery:
            self.spaceship.rect.centery -= self.spaceship.vel

    def __moveY(self, sRect, twoAxis: bool = False):
        hadMove = True
        if not (
                self._pointRect.top < sRect.centery < self._pointRect.bottom) and sRect.centery < self._pointRect.centery:
            self.spaceship.rect.centery += self.spaceship.vel
        elif not (
                self._pointRect.top < sRect.centery < self._pointRect.bottom) and sRect.centery > self._pointRect.centery:
            self.spaceship.rect.centery -= self.spaceship.vel
        else:
            hadMove = False
        if hadMove and not twoAxis:
            return
        if not (
                self._pointRect.left < sRect.centerx < self._pointRect.right) and sRect.centerx < self._pointRect.centerx:
            self.spaceship.rect.centerx += self.spaceship.vel
        elif not (
                self._pointRect.left < sRect.centerx < self._pointRect.right) and sRect.centerx > self._pointRect.centerx:
            self.spaceship.rect.centerx -= self.spaceship.vel

    def _moveToPoint(self, X: bool = True, Y: bool = False):
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
        sList = [True]
        sList.extend(False for _ in range(100))
        shot = random.choice(sList)
        cur = pygame.time.get_ticks()
        if Screen.sRect.colliderect(self.spaceship.getCurRect()) and cur-self._timeShot>=0 and shot and self.bullets.readyShoot():
            bl = self.bullets.getBullets(self.spaceship.getBulletPos())
            Game.ExtendEnemyBullet(bl)
            self.spaceship.shotEffect(self.bullets.recoil)
            self._timeShot = pygame.time.get_ticks()+random.randint(8000,20000)
            Sound.enemyShotSound_play()


class NormalBot(BBot):
    def __init__(self):
        super(NormalBot, self).__init__()
        self._movebyPoint = False
        self.pointList = []
        self._pointId = 0
        self.movementType = "1-D"
        self._rest = False
        self._restTime = 1000
        self._restTimer = 0

    def _setPoint(self, point):
        x = point[0]
        y = point[1]
        if not self._rest:
            self._pointId += 1
        elif pygame.time.get_ticks()-self._restTimer>=self._restTime:
            self._rest = False
        if x is None and y is None:
            self._moving = False
            self._rest = True
            self._restTimer = pygame.time.get_ticks()
        if x is None:
            self._moving = False
            return
        if y is None:
            self._moving = False
            return
        self._setPointRect(point)
        self._moving = True

    def setPointList(self, pointList: list):
        self.pointList = pointList
        if len(self.pointList) > 0:
            self._movebyPoint = True
            self._setPoint(self.getCurPoint())
            # self._setPointRect()
            self._moving = True

    def addPoint(self, *points):
        self.pointList.extend(list(points))

    def appendPoint(self, pointList):
        self.pointList.extend(pointList)

    def setAutomove(self):
        if len(self.pointList) > 0:
            self._movebyPoint = True
            self._setPoint(self.getCurPoint())
            # self._setPointRect(self.getCurPoint())
            self._moving = True

    def getCurPoint(self):
        if self._movebyPoint:
            if self._pointId >= len(self.pointList):
                self._pointId = 0
            return self.pointList[self._pointId]
        return [None, None]

    def _move(self):
        if self.movementType == "1-D":
            self._moveToPoint()
        elif self.movementType == "2-D":
            self._moveToPoint(True, True)
        elif self.movementType == "D-1":
            self._moveToPoint(False, True)
        elif self.movementType == "D-2":
            self._moveToPoint(False, False)
        else:
            self._moveToPoint()

    def _handleMove(self):
        self._move()
        if not self._moving and self._movebyPoint:
            # self._pointId += 1
            self._setPoint(self.getCurPoint())


class AutoBot(BBot):
    def __init__(self):
        super(AutoBot, self).__init__()
        self._area = self._getArea()
        self.movementType = "1-D"
        self._rest = False
        self._restRate = 0.5
        self._resting = False
        self._time = 0
        self._changeTypeMoveTime = pygame.time.get_ticks() + random.randint(5000, 15000)

    def setRest(self, value: bool = True, rate=0.5):
        self._rest = value
        self._restRate = rate

    def _getArea(self):
        area = Screen.sRect.copy()
        area.height = Screen.sRect.height * 5 // 8
        return area

    def _getRandomPoint(self):
        x = random.randint(self._area.left, self._area.right)
        y = random.randint(self._area.top, self._area.bottom)
        return [x, y]

    def _createRestListChoice(self):
        t = [True for _ in range(int(self._restRate * 10))]
        f = [False for _ in range(int((1 - self._restRate) * 10))]
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
                if pygame.time.get_ticks() - self._time >= 1000:
                    self._resting = False

    def _changeMoveType(self):
        if pygame.time.get_ticks() - self._changeTypeMoveTime >= 0:
            self.movementType = random.choice(['1-D', '2-D', 'D-1', 'D-2'])
            self._changeTypeMoveTime = pygame.time.get_ticks() + random.randint(3000, 10000)

    def _move(self):
        if self.movementType == "1-D":
            self._moveToPoint()
        elif self.movementType == "2-D":
            self._moveToPoint(True, True)
        elif self.movementType == "D-1":
            self._moveToPoint(False, True)
        elif self.movementType == "D-2":
            self._moveToPoint(False, False)
        else:
            self._moveToPoint()


class Boss(AutoBot):
    def __init__(self):
        super(Boss, self).__init__()
        self._velList = [3,4,5,6]
        self.setRest()
        self.bulletsList = []

    def _choiceBullets(self):
        if len(self.bulletsList)>0:
            newBullets =  random.choice(self.bulletsList)
            newBullets.time = pygame.time.get_ticks()
            return newBullets
        return None

    def _shot(self):
        if self.bullets is None:
            return
        shot = random.choice([True, False, False, False])
        if Screen.sRect.colliderect(self.spaceship.getCurRect()) and shot and self.bullets.readyShoot():
            bl = self.bullets.getBullets(self.spaceship.rect.center)
            Game.ExtendEnemyBullet(bl)
            self.spaceship.shotEffect(self.bullets.recoil)
            Sound.enemyShotSound_play()

    def _randomVel(self):
        return random.choice(self._velList)

    def _randomBulletLevel(self):
        if self.bullets is not None:
            levelMax = self.bullets.levelMax
            return random.randint(1, levelMax)
        return -1

    def _hanDleChangeVel(self):
        if self._resting:
            self.spaceship.vel = self._randomVel()

    def _handleChangeBulletLevel(self):
        if self._resting:
            self.bullets = self._choiceBullets()

    def _handleChangeBullet(self):
        if self._resting and self.bullets is not None:
            self.bullets.setLevel(self._randomBulletLevel())

    def _handleBoss(self):
        pass


# **********************************************************************


class Boss1(Boss):
    def __init__(self):
        super(Boss1, self).__init__()
        # self.setPoint([200,100])
        self.path = "..\\assets\\Bot\\boss1.json"
        self.spaceship = self._loadShip(self.path)
        self._velList = [i for i in range(max(self.spaceship.vel//2,2), self.spaceship.vel+5)]
        self.bulletsList = [Att.getBullets('BotSpecialBullet1'), Att.getBullets('BotBullet1')]
        self.bullets = self._choiceBullets()

    def _handleBoss(self):
        self._changeMoveType()
        self._autoMove()
        self._hanDleChangeVel()
        self._handleChangeBulletLevel()
        self._handleChangeBullet()

    def update(self):
        self._handleBoss()
        self._move()
        self._shot()
        self.spaceship.update()


# **********************************************************************


class BotDragDoll(AutoBot):
    def __init__(self):
        super(BotDragDoll, self).__init__()
        self.path = "..\\assets\\Bot\\dragdoll.json"
        self.spaceship = self._loadShip(self.path)
        self.spaceship.goto(random.randint(-200, Screen.sRect.width + 200), random.randint(-300, -20))
        self.bullets = Att.getBullets('BotBullet1')
        self.movementType = "D-2"
        self.setRest()
        self._dragdollBehav = False
        self._timeDragdoll = random.randint(20000, 40000)
        self._dragdollTime = pygame.time.get_ticks()

    def _handleBehaviour(self):
        if not self._dragdollBehav and pygame.time.get_ticks() - self._dragdollTime >= self._timeDragdoll:
            self._dragdollBehav = True
            self.setPoint([self.spaceship.rect.centerx, Screen.sRect.height + 1000])
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
        self.bullets.cooldownTime = random.randint(5000, 20000)
        self.spaceship.vel = 2
        # self.movementType = "2-D"
        self.movementType = "D-2"

    def update(self):
        self._shot()
        self.spaceship.update()
        self._handleMove()


if __name__ == '__main__':
    bot = Boss1()
    # bot.setPointList([[200,400]])
    Game.playing = True
    Game.AddEnemy(bot)

    Game.run()
