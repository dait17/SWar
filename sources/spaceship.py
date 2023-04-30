import pygame
from game import Game as G
from messageBox import MessageBox


class Spaceship:
    def __init__(self, imgList:list, pos:list, size:list, vel, maxHp, directionUp):
        self.directionUp = directionUp

        self.rect = self._initRect(pos, size)
        self._curRect = self.rect.copy()
        self.imgList = self._fixImg(imgList)
        self.imgId = 0
        self.vel = vel
        self.maxHp = maxHp
        self.hp = self.maxHp
        self.hpUpPos = True

        self.screen = pygame.display.get_surface()

        self._point = None
        self._movePoint = False

        self.showHpBox = False
        self._showHpBoxCustom = False
        self._hpBoxCustom = None
        self.enable = True
        self.visible = True

        # swinging effect
        self._swingingSetting = False
        self._swingingTime = 0
        self.ampMax = 10 # amplitude - bien do dao dong
        self._Xamp = 0
        self._Aamp = 0.005
        self._Vamp = self._Aamp

        # shot effect
        self.shoting = False
        self._recoil = 0
        self._Arecoil = 1
        self._Vrecoil = self._Arecoil
        self._Xrecoil = 0

        # Wavering
        self.wavering = False
        self._AmpW = 5
        self._AW = 0.5
        self._VW = self._AW
        self._XW = 0

    def changeShip(self, imgList, size, vel, maxHp):
        self.imgList = self._fixImg(imgList)
        self.imgId = 0

        self.rect = self._initRect(self.rect.center, size)
        self.vel = vel
        curHp = round(self.hp/self.maxHp)*maxHp
        self.maxHp = maxHp
        self.hp = curHp

    def setSize(self, size):
        center = self.rect.center
        self.rect.size = size
        self.rect.center = center

    def shotEffect(self, recoil):
        self.shoting = True
        self._recoil = recoil

    def _sChange(self, rect, d, changeX, changeY):
        if changeX:
            rect.x += d
        if changeY:
            rect.y += d

    def _effectChangePos(self, amp, ampMax, a, v,changeX:bool=False, changeY:bool=True):
        amp += v
        newRect = self.rect.copy()
        if int(amp) <= ampMax//2:
            v += a
            self._sChange(newRect, amp, changeX, changeY)
            # newRect.y += amp
        elif ampMax//2 < int(amp) <= ampMax:
            v -= a
            self._sChange(newRect, ampMax - amp, changeX, changeY)
            # newRect.y += ampMax - amp
        else:
            v = a
            amp = 0
        return amp,v,newRect

    def _swingingEffect(self):
        self._Xamp, self._Vamp, newRect = self._effectChangePos(self._Xamp, self.ampMax, self._Aamp, self._Vamp)
        return newRect

    def _recoilEffect(self):
        self._Xrecoil, self._Vrecoil, newRect = self._effectChangePos(self._Xrecoil, self._recoil, self._Arecoil, self._Vrecoil)
        if self._Xrecoil==0:
            self.shoting = False
        return newRect

    def _waveringEffect(self):
        self._XW, self._VW, newRect = self._effectChangePos(self._XW,self._AmpW, self._AW, self._VW, True)
        if self._XW==0:
            self.wavering = False
        return newRect

    def _effect(self):
        newRect = self.rect.copy()
        if self.shoting:
            self._swingingSetting = False
            newRect = self._recoilEffect()
        elif self.wavering:
            self._swingingSetting = False
            newRect = self._waveringEffect()
        else:
            if not self._swingingSetting:
                self._swingingTime = pygame.time.get_ticks()
                self._swingingSetting = True
            if pygame.time.get_ticks()-self._swingingTime>=500:
                newRect = self._swingingEffect()

        self._curRect = newRect

    def _initRect(self, pos, size):
        rect = pygame.Rect(0,0,size[0], size[1])
        rect.center = pos
        return rect

    def beShot(self, dmg):
        self.wavering = True
        self.hp -= dmg
        if self.hp<=0:
            self.enable = False

    def health(self, value):
        self.hp += value
        if self.hp>self.maxHp:
            self.hp = self.maxHp

    def _fixImg(self, imgList):
        il = []
        for img in imgList:
            if type(img) is pygame.Surface:
                il.append(img)
        if len(il)==0:
            il.append(pygame.Surface(self.rect.size))
        return il

    def getCurRect(self):
        return self._curRect

    def _getHpBox(self):
        box = pygame.Rect(0,0,self.rect.height, 4)
        if self.hpUpPos:
            box.topleft = self.rect.topleft
            box.y -= 6
        else:
            box.bottomleft = self.rect.bottomleft
            box.y += 6
        return box

    def _getHpRect(self, hpBox:pygame.Rect):
        rect = hpBox.copy()
        rect.width = (self.hp/self.maxHp)*hpBox.width
        return rect

    def _getImg(self, id):
        return pygame.transform.smoothscale(self.imgList[int(id)], self.rect.size)

    def _handleImgId(self):
        self.imgId += 0.02
        if self.imgId>=len(self.imgList):
            self.imgId = 0

    def setShowHp(self, value:bool, upPos:bool=True):
        self.showHpBox = value
        self.hpUpPos = upPos

    def setShoHpCustom(self,rect):
        self._showHpBoxCustom = True
        self._hpBoxCustom = rect

    def _showHp(self):
        if self.showHpBox:
            hpBpx = self._getHpBox()
            pygame.draw.rect(self.screen, (255,255,255), hpBpx, 1,4)
            pygame.draw.rect(self.screen, (255,0,0), self._getHpRect(hpBpx))
        elif self._showHpBoxCustom:
            MessageBox.show('Hp: ', '', [self._hpBoxCustom.left-30,self._hpBoxCustom.top], size=18)
            pygame.draw.rect(self.screen, (255, 255, 255), self._hpBoxCustom, 1, 6)
            pygame.draw.rect(self.screen, (255, 0, 0), self._getHpRect(self._hpBoxCustom), border_radius=6)

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def gotoPos(self, pos):
        self.rect.center = pos

    def _draw(self):
        if self.visible:
            self.screen.blit(self._getImg(self.imgId), self._curRect)
            self._handleImgId()
            self._showHp()

    def getBulletPos(self):
        x = self.rect.centerx
        if self.directionUp:
            y = self.rect.top+5
        else:
            y = self.rect.bottom-5

        return [x,y]

    def setMovePoint(self, point):
        self._movePoint = True
        self._point = point

    def _moveToPoint(self):
        if self._movePoint:
            if self.rect.x<self._point[0]:
                if self.rect.x+self.vel>=self._point[0]:
                    self.rect.x = self._point[0]
                else:
                    self.rect.x += self.vel

            elif self.rect.x>self._point[0]:
                if self.rect.x-self.vel<=self._point[0]:
                    self.rect.x = self._point[0]
                else:
                    self.rect.x -= self.vel

            elif self.rect.y < self._point[1]:
                if self.rect.y + self.vel >= self._point[1]:
                    self.rect.y = self._point[1]
                else:
                    self.rect.y += self.vel

            elif self.rect.y > self._point[1]:
                if self.rect.y - self.vel <= self._point[1]:
                    self.rect.y = self._point[1]
                else:
                    self.rect.y -= self.vel
            else:
                self._movePoint = False

    def ensuringInScreen(self):
        if not self._movePoint:
            if self.rect.left<G.srect.left:
                self.rect.left = G.srect.left
            elif self.rect.right>G.srect.right:
                self.rect.right = G.srect.right
            if self.rect.top<G.srect.top:
                self.rect.top = G.srect.top
            elif self.rect.bottom>G.srect.bottom:
                self.rect.bottom = G.srect.bottom

    def update(self):
        if self.enable:
            self._effect()
            self._draw()
            self._moveToPoint()



if __name__ == '__main__':
    from test import Test
    T = Test()
    S = Spaceship([], [400,600], [50,50],12,100,True)
    S.setShowHp(True, True)

    T.add(S)

    T.run()




