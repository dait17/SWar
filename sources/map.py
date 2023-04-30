import pygame
import tkinter as tk
from tkinter import filedialog
from path import Path
import random
from bot import *
from game import Game
from messageBox import MessageBox
from player import Player
from items import Items


class Map:
    def __init__(self, mapPath):
        Game.setPlayer([Player()])
        self.data = self._loadData(mapPath)
        self.background = self.getBackground()
        self.items = self._getItems()
        self.rounds = []
        self.roundId = 0
        self.curRound = None
        self._setupRound()
        self._win = None
        self._wTime = 0
        self._enableTime = 0
        self._trans = False
        self.enable = True

    def _loadImg(self, path):
        path = Path.getPath(path)
        try:
            return pygame.image.load(path)
        except Exception:
            pass
        return None

    def _getBackgrounds(self, pathList:list):
        bgs = []
        for p in pathList:
            img = self._loadImg(p)
            if img is not None:
                bgs.append(img)
        return bgs

    def getBackground(self):
        background = self.data.get('background')
        pathList = background.get('imgPathList')
        ops = background.get('ops')
        bgs = self._getBackgrounds(pathList)
        return Background(bgs, ops)

    def _loadData(self, path):
        path = Path.getPath(path)
        return readFile(path)

    def _setupRound(self):
        rounds = self.data.get('rounds')
        for i in range(0,4):
            round = Round(rounds.get(f'round{i+1}'))
            self.rounds.append(round)
        self.curRound = self.getCurRound(self.roundId)

    def getCurRound(self, id):
        if id>=4:
            return None
        return self.rounds[id]

    def _nextRound(self):
        self.roundId += 1
        cur = self.getCurRound(self.roundId)
        if cur is None:
            self._win = True

    def _handleRound(self):
        if len(Game.enemyList)==0:
            nbots = self.curRound.Next()
            if nbots is None:
                self._trans = True
                self._nextRound()
            else:
                Game.ExtendEnemy(nbots)

    def _won(self):
        if self._wTime==0:
            self._wTime = pygame.time.get_ticks()
        elif pygame.time.get_ticks()-self._wTime>=1000:
            MessageBox.show('You win!', '', Game.srect.center, (0,255,0), 36)
            if self._enableTime==0:
                self._enableTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self._enableTime>=3000:
                self.enable = False

    def _lose(self):
        if self._wTime==0:
            self._wTime = pygame.time.get_ticks()
        elif pygame.time.get_ticks()-self._wTime>=1000:
            MessageBox.show('Game Over!', '', Game.srect.center, (255,0,0), 36)
            if self._enableTime==0:
                self._enableTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self._enableTime>=3000:
                self.enable = False

    def update(self):
        self.background.update()
        if self._win is None:
            self._handleRound()
            self.items.update()
            if len(Game.playerList)==0:
                self._win = False
        elif self._win:
            self._won()
        else:
            self._lose()


    def _getItems(self):
        dropRate = self.data.get("items")
        return Items(dropRate)



class Background:
    def __init__(self, imgList, ops):
        self.imgList = imgList
        self.rectList = None
        self._xList = []
        self.ops = ops
        self.maxWidth = 0

        self._setup(self.imgList, ops)
        self.imgRect = None
        self._v = 0.1

    def _setup(self, imgList:list[pygame.Surface], ops:str):
        rl = []
        st = 0
        if ops.upper() == 'REPEAT':
            if len(imgList) == 1:
                newImg = imgList[0].copy()
                newImg = pygame.transform.flip(newImg, True, False)
                imgList.append(newImg)
            print(len(self.imgList))
        for img in imgList:
            rect = img.get_rect(y=0)
            rect.left = st
            rl.append(rect)
            self._xList.append(rect.x)
            st += rect.right-1
            self.maxWidth += rect.width-1
        self.rectList = rl

    def _updateRect(self):
        for i in range(len(self.rectList)):
            self._xList[i] -= self._v
            self.rectList[i].x = self._xList[i]
            if self.rectList[i].right < 0:
                self._xList[i] = self.maxWidth//len(self.rectList)

    def update(self):
        if len(self.imgList)>0:
            self._updateRect()
            for i in range(len(self.imgList)):
                Game.blit(self.imgList[i], self.rectList[i])
        else:
            Game.screen.fill((255,255,255))


class Round:
    def __init__(self,waveList:list[dict]):
        self.waveList = waveList
        self.waveCount = None
        self.curWave = None
        self._setup(waveList)

    def _setup(self, waveList:list):
        if len(waveList)>0:
            self.waveCount = len(waveList)
            self.curWave = 0

    def _createGroupBot(self, data:dict):
        try:
            botName = data.get('botName')
            quantity = data.get('quantity')
            groupType = data.get('groupType')
            distance = data.get('distance')
            bullet = data.get('bullet')
            bulletLevel = data.get('bulletLevel')
            startPoint = data.get('startPoint')
            pointList = data.get('pointList')
            gb = Bots.getGroupBot(botName, quantity)

            SetPointList.setPointList(gb, groupType, distance, pointList, startPoint)

            return gb

        except Exception:
            MessageBox.show('Lỗi: ', 'Không tạo được bot', [100,10])
            return []

    def getNormalBots(self, data:list):
        bots = []
        for d in data:
            bots.extend(self._createGroupBot(d))
        return bots

    def Next(self):
        bots = []
        if self.curWave is not None:
            if self.curWave>=self.waveCount:
                return None
            try:
                data = self.waveList[self.curWave]
                # print(data)
                bots.extend(self.getNormalBots(data.get('normalBot')))
                self.curWave += 1
                return bots
            except Exception:
                MessageBox.show('Lỗi: ', 'Không lấy được curWave', [100,30])
                return None
        else:
            return None


class SetPointList:

    def __init__(self):
        pass

    @staticmethod
    def _chainingDistance(startPoint, distance):
        dx, dy = distance
        stX, stY = startPoint
        if stY<0:
            dx = 0
            dy = -dy
        elif stX<0:
            dx = -dx
            dy = 0
        elif stX>Game.srect.width:
            dy = 0
        elif stY>Game.srect.height:
            dx = 0
        return dx, dy

    @staticmethod
    def chaining(bots:list[NormalBot], distance, pointList, startPoint):
        if len(bots)==0:
            return
        dx,dy = distance

        dx += bots[0].spaceship.rect.width
        dy += bots[0].spaceship.rect.height

        dx,dy = SetPointList._chainingDistance(startPoint, [dx,dy])
        x,y = startPoint
        for bot in bots:
            bot.setPointList(pointList)
            bot.spaceship.gotoPos([x,y])
            y += dy
            x += dx

    @staticmethod
    def setPointList(bots, groupType:str, distance, pointList, startPoint):
        groupType = groupType.upper()
        if groupType == "CHAINING":
            SetPointList.chaining(bots, distance, pointList, startPoint)






if __name__ == '__main__':
    map = Map(r"assets\map\map1.json")
    Game.setMap(map)
    Game.AddPlayer(Player())
    Game.run()
    # map = readFile(r'D:\Workspace\python_project\pygame_pr\SWar\assets\map\map1.json')
    # rounds = map.get('rounds')
    # rList = rounds.get('round1')
    # R = Round(rList)
    # player = Player()
    #
    # G = Game()
    # G.AddPlayer(player)
    #
    # G.setBackground('..\\assets\\img_background\\bg2.jpg')
    # bots = R.Next()
    # G.ExtendEnemy(bots)
    # MessageBox.show('rect: ', bots[0].spaceship.rect, [300,300])
    # G.run()



