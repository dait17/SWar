import pygame
from game import Game
pygame.font.init()


class MessageBox:
    font = pygame.font.SysFont('comic sans', 14,True)

    def __init__(self):
        pass

    @staticmethod
    def show(mess:str, content, pos:list, color=(255,255,255), size:int=14):
        font = pygame.font.SysFont('comic sans', 14, True)
        sur = font.render(mess+str(content),True,color)
        Game.showSurface(sur, pos)


