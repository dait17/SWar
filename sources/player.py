import pygame.image

from spaceship import Spaceship
from attackSystem import AttackSystem as Att
from gameTools import *
from game import Game


# from sound import Sound


class Player:
    def __init__(self):
        self.spaceship = self._shipInit('..\\assets\\Ship\\ship1.json')
        self.bullets = Att.getBullets("superblue")

    def _loadInfo(self, shipPath):
        return HandleJson.readFile(shipPath)

    def _loadImgList(self, listPath: list):
        img = []
        try:
            for path in listPath:
                img.append(Image.load(path))
        except Exception:
            pass
        return img

    def _shipInit(self, path):
        pos = [Game.srect.width // 2, Game.srect.height + 100]
        sp = self._setShip(path, pos.copy())
        # sp.setMovePoint([pos[0], pos[1]-250])
        sp.moveTo(0, -250, 6)

        hpRect = pygame.Rect(0, 0, 80, 20)
        hpRect.top = Screen.sRect.top + 20
        hpRect.right = Screen.sRect.right - 20
        sp.setShoHpCustom(hpRect)
        # sp.setExplosionSound(Sound.playerExplosionSound)
        return sp

    def _setShip(self, shipPath: str, pos):
        shipInfo = HandleJson.readFile(shipPath)
        imgList = self._loadImgList(shipInfo.get('imgPathList'))
        return Spaceship(imgList, pos, shipInfo.get('size'), shipInfo.get('vel'), shipInfo.get('hp'), True)

    def setShip(self, imgList, size, vel, maxHp):
        try:
            self.spaceship.changeShip(imgList, size, vel, maxHp)
        except Exception:
            pass

    def setBullets(self, bulletName):
        self.bullets = Att.getBullets(bulletName)
        self.bullets.setLevel(1)

    def _movementKey(self):
        keyPress = pygame.key.get_pressed()
        v = pygame.Vector2([0, 0])
        if keyPress[pygame.K_a]:
            v.x = -1
        elif keyPress[pygame.K_d]:
            v.x = 1
        if keyPress[pygame.K_w]:
            v.y = -1
        elif keyPress[pygame.K_s]:
            v.y = 1
        if v.length() > 1:
            return v.normalize()
        return v

    def _movement(self):
        v = self._movementKey()
        self.spaceship.rect.x += self.spaceship.vel * v.x
        self.spaceship.rect.y += self.spaceship.vel * v.y
        self.spaceship.ensuringInScreen()

    def _shoot(self):
        keyPress = pygame.key.get_pressed()
        if keyPress[pygame.K_SPACE] and self.bullets.readyShoot():
            bl = self.bullets.getBullets(self.spaceship.getBulletPos())
            Game.ExtendPlayerBullet(bl)
            self.spaceship.shotEffect(self.bullets.recoil)
            # Sound.shotSound_play()

    def update(self):
        self.spaceship.update()
        self._movement()
        self._shoot()
