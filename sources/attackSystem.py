from bulletFireBall import FireBall


class AttackSystem:
    def __init__(self):
        pass

    @staticmethod
    def getBullets(name:str):
        if name.upper()=='FIREBALL':
            return FireBall()



