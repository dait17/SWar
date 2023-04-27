from game import Game
from player import Player
from bot import BotAlien
from map import SetPointList


G = Game()

G.setBackground('..\\assets\\img_background\\bg2.jpg')

player = Player()

eList = []
for i in range(6):
    e = BotAlien()
    e.spaceship.setShowHp(True, True)
    eList.append(e)

SetPointList.chaining(eList, [60,60], [[200, 300], [500, None], [1200, 100]], [100, -200])

# enemy = BotAlien()
# enemy.spaceship.setShowHp(True, True)
# enemy.setPointList([[200,300], [600,None], [1000, 100]])



G.AddPlayer(player)
# G.AddEnemy(enemy)
G.ExtendEnemy(eList)


G.run()









