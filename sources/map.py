import pygame
import tkinter as tk
from tkinter import filedialog
from path import Path
import random
from bot import *
from game import Game


class MapTool:
    def __init__(self, mapPath):
        self.mapPath = mapPath

    @staticmethod
    def choiceFile(motherPath:str):
        root = tk.Tk()
        root.withdraw()
        motherPath = Path.getPath(motherPath)
        return filedialog.askopenfilename(initialdir=motherPath)

    @staticmethod
    def getPathAsset():
        return MapTool.choiceFile('..\\assets')


    @staticmethod
    def AddMap():
        pass


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







if __name__ == '__main__':
    tl = 0.5
    tli = int(0.8*10)
    t = [True]*tli
    f = [False]*(10-tli)
    l = t+f
    random.shuffle(l)
    print(l)
    print(random.choice(l))




