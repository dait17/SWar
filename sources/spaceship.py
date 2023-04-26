import pygame


class Spaceship:
    def __init__(self, imgList:list, pos:list, size:list, vel, maxHp, directionUp):
        self.rect = self._initRect(pos, size)
        self.imgList = self._fixImg(imgList)
        self.imgId = 0
        self.vel = vel
        self.maxHp = maxHp
        self.hp = self.maxHp
        self.hpUpPos = True

        self.directionUp = directionUp
        self.screen = pygame.display.get_surface()

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

    def update(self):
        if self.enable:
            self._draw()


if __name__ == '__main__':
    from test import Test
    T = Test()
    S = Spaceship([], [400,600], [50,50],12,100,True)
    S.setShowHp(True, True)

    T.add(S)

    T.run()




