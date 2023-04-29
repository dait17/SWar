import pygame.time

from gameTools import *
from game import Game
import random


class Items:
    def __init__(self, dropRate:dict):
        self._dropRate = dropRate
        self._timer = pygame.time.get_ticks()+self._getRandomTime(2000,15000)
        self._itemsList = self._createItemList()

    def _getRandomTime(self, start,end):
        return random.randint(start, end)

    def _nextTime(self):
        self._timer += self._getRandomTime(5000,10000)

    def _createBLU(self, dropRate, pos):
        dr = int(dropRate*10)
        il = []
        for i in range(dr):
            il.append(ItemBulletLevelUp(pos))
        return il

    def _createItem(self, ItemClass, dropRate):
        dr = int(dropRate * 10)
        il = []
        for i in range(dr):
            il.append(ItemClass(self._getRandomPos()))
        return il

    def _getRandomPos(self):
        x = random.randint(20, Screen.sRect.width-20)
        return x,-60

    def _createItemList(self):
        l = []
        l.extend(self._createItem(ItemBulletLevelUp, self._dropRate.get('levelUp')))
        l.extend(self._createItem(ItemChangeShip, self._dropRate.get('changeShip')))
        return l

    def _getItem(self):
        return random.choice(self._itemsList)

    def _handleAutoDropItem(self):
        if pygame.time.get_ticks()-self._timer>=0:
            Game.AddItem(self._getItem())
            self._nextTime()
            self._itemsList = self._createItemList()

    def _dropByBotDefeat(self):
        if Game.EventBotDefeat:
            Game.AddItem(ItemBulletLevelUp(Game.EventBotDefeatPos))

    def _handleDropItem(self):
        self._handleAutoDropItem()
        # self._dropByBotDefeat()

    def setItemBulletLevelUp(self, pos):
        Game.AddItem(ItemBulletLevelUp(pos))

    def setItemChangeShip(self, pos):
        Game.AddItem(ItemChangeShip(pos))

    def update(self):
        self._handleDropItem()


class IItem:
    def __init__(self, pos:list):
        self._vel = 1

        self._imgList = []
        self._size = [50,50]
        self._rect = None
        self.curRect = None
        self._setupRect(pos)

        self._imgId = 0
        self._curImg = None

        self.enable = True
        self._posUpdating = True
        self._imgSizeUpdating = True

        ## Effect parameter
        # changeImg
        self._eCIV = 0.1
        # rotateImg
        self._eRIV = 1
        self._curD = 0
        # Heartbeat
        self._eHbA = 0.005
        self._eHbV = 0
        self._eHbX = 0
        self._eHbDMax = 20

    def _setupRect(self, pos):
        self._rect = pygame.Rect(0,0, self._size[0], self._size[1])
        self._rect.center = pos
        self.curRect = self._rect.copy()

    def _getImgById(self):
        try:
            img = self._imgList[int(self._imgId)]
            return img
        except Exception:
            return pygame.Surface(self._size)

    def _getImg(self, img):
        try:
            return pygame.transform.smoothscale(img, self.curRect.size)
        except Exception:
            return None

    def _movement(self):
        self._rect.y += self._vel
        if self._rect.top>Screen.sRect.bottom:
            self.enable = False

    def _draw(self):
        Screen.blit(self._curImg,self.curRect.center)

    def _effectChangeImg(self):
        self._imgId += self._eCIV
        if self._imgId>=len(self._imgList):
            self._imgId = 0
        self._curImg = self._getImgById()

    def _effectRotateImg(self):
        self._curD += self._eRIV
        if self._curD>=360:
            self._curD = 0
        try:
            self._curImg = pygame.transform.rotate(self._getImgById(), self._curD)
        except Exception as e:
            print(e)

    def _effectHeartbeat(self):
        self._eHbV += self._eHbA
        self._eHbX += self._eHbV
        if 0<=self._eHbX<=self._eHbDMax/2:
            self.curRect.width = self._rect.width + self._eHbX
            self.curRect.height = self._rect.height + self._eHbX
        elif self._eHbDMax/2<self._eHbX<self._eHbDMax:
            self.curRect.width = self._rect.width + (self._eHbDMax - self._eHbX)
            self.curRect.height = self._rect.height + (self._eHbDMax - self._eHbX)
        else:
            self._eHbV = 0
            self._eHbX = 0
            self.curRect.size = self._rect.size
        self.curRect.center = self._rect.center
        self._curImg = self._getImgById()

    def _effect(self):
        pass

    def _updatePos(self):
        if self._posUpdating:
            self.curRect.center = self._rect.center

    def _updateImgSize(self):
        if self._imgSizeUpdating:
            self._curImg = self._getImg(self._curImg)

    def _collide(self, player):
        pass

    def _handleCollide(self):
        for player in Game.playerList:
            if self.curRect.colliderect(player.spaceship.getCurRect()):
                self._collide(player)
                self.enable = False
                break

    def update(self):
        if self.enable:
            self._movement()
            self._effect()
            self._updatePos()
            self._updateImgSize()
            self._handleCollide()
            self._draw()

# ***************************************************************************


class ItemBulletLevelUp(IItem):
    def __init__(self, pos:list):
        super(ItemBulletLevelUp, self).__init__(pos)
        self._setupImg()

    def _setupImg(self):
        self._imgList = self._getImgList()
        self._curImg = self._getImgById()

    def _getImgList(self):
        mp = '..\\assets\\items\\energy\\'
        filesP = Path.getFiles(mp)
        imgList = []
        for p in filesP:
            img = Image.load(mp+p)
            if img is not None:
                imgList.append(img)
        return imgList

    def _effect(self):
        self._effectChangeImg()
        self._effectRotateImg()

    def _collide(self, player):
        player.bullets.levelUP()

# ***************************************************************************


class ItemChangeShip:
    def __init__(self, pos):
        self._item = self._getItem(pos)

    def _getItem(self, pos):
        return ItemShip(pos, self._choiceShip())

    def _choiceShip(self):
        mp = '..\\assets\\Ship\\'
        pathList = Path.getFiles(mp)
        path = random.choice(pathList)
        return mp+path

    def update(self):
        self._item.update()

# ***************************************************************************


class ItemShip(IItem):
    def __init__(self, pos, shipPath):
        super(ItemShip, self).__init__(pos)
        self._shipSize = None
        self._shipVel = None
        self._maxHp = None

        self._loadShip(shipPath)

    def _loadShip(self, shipPath):
        data = HandleJson.readFile(shipPath)
        self._shipVel = data.get('vel')
        self._maxHp = data.get('maxHp')
        self._shipSize = data.get('size')

        imgPathList = data.get('imgPathList')
        self._setImgList(Image.loadImgList(imgPathList))

    def _setImgList(self, imgList):
        self._imgList = imgList
        self._imgId = 0
        self._curImg = self._getImgById()

    def _effect(self):
        self._effectHeartbeat()

    def _collide(self, player):
        player.setShip(self._imgList, self._shipSize, self._shipVel, self._maxHp)




if __name__ == '__main__':
    # i = ItemBulletLevelUp([200,0])
    # i = ItemShip([200,0], "..\\assets\\Ship\\ship1.json")
    i = ItemChangeShip([200,0])
    # i.setImgList(Image.loadImgList(HandleJson.readFile('..\\assets\\Ship\\ship1.json').get('imgPathList')))
    Game.setFrame(i)
    Game.run()



















