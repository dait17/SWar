from game import Game
from player import Player
from bot import BotAlien


G = Game()

G.setBackground('..\\assets\\img_background\\bg2.jpg')

player = Player()
enemy = BotAlien()
enemy.setPointList([[200,300], [600,None], [1000, 100]])

G.AddPlayer(player)
G.AddEnemy(enemy)


G.run()









