from bulletFireBall import FireBall


class AttackSystem:
    def __init__(self):
        self.bulletName = 'FireBal'
        self.bullets = None
        self._setBullets()

    def _setBullets(self):
        if self.bulletName.upper() == 'FIREBALL':
            self.bullets = FireBall()

    def getBullets(self, pos):
        return self.bullets.getBullets(pos)

    def setBullets(self, name: str):
        self.bulletName = name
        self._setBullets()
