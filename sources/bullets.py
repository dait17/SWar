import pygame
from bullet import *
from abc import ABC, abstractmethod


class Bullets(ABC):
    def __init__(self, ):
        self.cooldownTime = 500 #ms
        self.imgPath = ''






