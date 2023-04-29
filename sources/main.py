from game import Game
from player import Player
from bot import BotAlien
from map import SetPointList
from frame import MainFrame, MapFrame



player = Player()
Game.AddPlayer(player)
Game.setFrame(MainFrame())
Game.run()












