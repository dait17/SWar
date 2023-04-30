from bulletFireBall import FireBall, SuperBlue
from botBullet import BotBullet1, BotSpecialBullet1


class AttackSystem:
    def __init__(self):
        pass

    @staticmethod
    def getBullets(name:str):
        name = name.upper()
        if name=='FIREBALL':
            return FireBall()
        elif name=="SUPERBLUE":
            return SuperBlue()
        elif name=="BOTBULLET1":
            return BotBullet1()
        elif name=="BOTSPECIALBULLET1":
            return BotSpecialBullet1()



