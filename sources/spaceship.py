import pygame
from game import Game as G


class Spaceship:
    def __init__(self, imgList:list, pos:list, size:list, vel, maxHp, directionUp):
        self.directionUp = directionUp

        self.rect = self._initRect(pos, size)
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
        self.enable = True
        self.visible = True

    def _initRect(self, pos, size):
        rect = pygame.Rect(0,0,size[0], size[1])
        rect.center = pos
        return rect

    def _fixImg(self, imgList):
        il = []
        for img in imgList:
            if type(img) is pygame.Surface:
                if not self.directionUp:
                    img = pygame.transform.rotate(img,180)
                il.append(img)
        if len(il)==0:
            il.append(pygame.Surface(self.rect.size))
        return il

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

    def setShowHp(self, value:bool, upPos:bool):
        self.showHpBox = value
        self.hpUpPos = upPos

    def _showHp(self):
        if self.showHpBox:
            hpBpx = self._getHpBox()
            pygame.draw.rect(self.screen, (255,255,255), hpBpx, 1,4)
            pygame.draw.rect(self.screen, (255,0,0), self._getHpRect(hpBpx))

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def gotoPos(self, pos):
        self.rect.center = pos

    def _draw(self):
        if self.visible:
            self.screen.blit(self._getImg(self.imgId), self.rect)
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
            self._draw()
            self._moveToPoint()


if __name__ == '__main__':
    from test import Test
    T = Test()
    S = Spaceship([], [400,600], [50,50],12,100,True)
    S.setShowHp(True, True)

    T.add(S)

    T.run()




