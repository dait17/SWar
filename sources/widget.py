from gameTools import *
#from sound import Sound
pygame.font.init()


class Frame:
    def __init__(self, pos: list, size: list, bg=None):
        self.screen = pygame.display.get_surface()
        self.rect = self._getRect(pos, size)
        self._bg = self.getGb(bg)
        self._bntList = []
        self.enable = True

    def setDisable(self):
        self.enable = False

    def setEnable(self):
        self.enable = True

    def addBnt(self, bnt):
        self._bntList.append(bnt)

    def _drawBg(self):
        if type(self._bg) is pygame.Surface:
            self.screen.blit(self._bg, self.rect)
        else:
            self.screen.fill((255,255,255))

    def _updateBnt(self):
        for bnt in self._bntList:
            bnt.update()

    def update(self):
        if self.enable:
            self._drawBg()
            self._updateBnt()

    def _getRect(self, pos, size):
        rect = pygame.Rect(0, 0, size[0], size[1])
        rect.center = pos
        return rect

    def getGb(self, bg):
        if type(bg) is pygame.Surface:
            bg = pygame.transform.smoothscale(bg, self.rect.size)
            return bg
        return None


class Button:
    def __init__(self, area: pygame.Rect, pos: list, size: list, content: str = ''):
        self._area = area
        self.screen = pygame.display.get_surface()
        self._boderRect = None
        self._paddingRect = None

        self._borderWidth = 1
        self._radius = 8
        self._setup(pos, size)

        self._fontSize = 23
        self._content = ButtonContent(self._boderRect, content, self._fontSize)

        # color
        self._colorBorder = (0, 0, 0)
        self._colorPadding = (123, 123, 123)

        # status
        self.enable = True
        self.hover = False
        self.pressing = False
        self.clicked = False

        # func
        self._func = None

    def addContent(self, txt):
        self._content = ButtonContent(self._boderRect, txt, self._fontSize)

    def _actioion(self):
        if self.clicked and self._func is not None:
            #Sound.clickSound_play()
            self._func()

    def _ensuringBntInArea(self):
        if self._boderRect.left < self._area.left:
            self._boderRect.left = self._area.left
        elif self._boderRect.right > self._area.right:
            self._boderRect.right = self._area.right

        if self._boderRect.top < self._area.top:
            self._boderRect.top = self._area.top
        elif self._boderRect.bottom > self._area.bottom:
            self._boderRect.bottom = self._area.bottom

    def _setup(self, pos, size):
        rect = pygame.Rect(0, 0, size[0], size[1])
        rect.center = pos
        self._boderRect = rect.copy()
        self._ensuringBntInArea()
        self._setupPadding()

    def _setupPadding(self):
        width = self._boderRect.width - self._borderWidth * 2
        height = self._boderRect.height - self._borderWidth * 2
        self._paddingRect = self._boderRect.copy()
        self._paddingRect.size = [width, height]
        self._paddingRect.center = self._boderRect.center

    def connect(self, func):
        self._func = func

    def _checkEventHover(self):
        mousePos = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mousePos[0], mousePos[1], 1, 1)
        if mouseRect.colliderect(self._boderRect):
            self.hover = True
        else:
            self.hover = False

    def _checkEventPress(self):
        if self.hover:
            mousePress = pygame.mouse.get_pressed()
            if mousePress[0]:
                self.pressing = True
            elif self.clicked:
                self.pressing = False
        else:
            self.pressing = False

    def _checkEventClick(self):
        if self.pressing:
            mousePress = pygame.mouse.get_pressed()
            if not mousePress[0]:
                self.clicked = True
        else:
            self.clicked = False

    def _checkEvent(self):
        self._checkEventHover()
        self._checkEventPress()
        self._checkEventClick()

    def _reSizeRect(self, rect, d: int):
        center = rect.center
        rect.width += d
        rect.height += d
        rect.center = center

    def _getBorderRect(self):
        newRect = self._boderRect.copy()
        if self.hover and not self.pressing:
            self._reSizeRect(newRect, 5)
        elif self.pressing:
            self._reSizeRect(newRect, -2)

        return newRect

    def _getPaddingRect(self):
        newRect = self._paddingRect.copy()
        if self.hover and not self.pressing:
            self._reSizeRect(newRect, 5)
        elif self.pressing:
            self._reSizeRect(newRect, -2)

        return newRect

    def _getContent(self):
        if self.hover and not self.pressing:
            self._content.setFontSize(self._fontSize + 2)
        elif self.pressing:
            self._content.setFontSize(self._fontSize - 1)
        else:
            self._content.setFontSize(self._fontSize)

    def _draw(self):
        pygame.draw.rect(self.screen, self._colorBorder, self._getBorderRect(), self._borderWidth, self._radius)
        pygame.draw.rect(self.screen, self._colorPadding, self._getPaddingRect(), border_radius=self._radius)

    def _updateContent(self):
        self._getContent()
        self._content.update()

    def _setPos(self, pos, dx, dy):
        self._boderRect.center = pos
        self._ensuringBntInArea()
        self._boderRect.centerx += dx
        self._boderRect.centery += dy
        self._setupPadding()

    def posCenter(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.center, dx, dy)

    def posTopleft(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.topleft, dx, dy)

    def posTopright(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.topright, -dx, dy)

    def posMidtop(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.midtop, dx, dy)

    def posBottomleft(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.bottomleft, dx, -dy)

    def posBottomright(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.bottomright, -dx, -dy)

    def posMidbottom(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.midbottom, dx, -dy)

    def posMidleft(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.midleft, dx, dy)

    def posMidright(self, dx: int = 0, dy: int = 0):
        self._setPos(self._area.midright, -dx, dy)

    def update(self):
        if self.enable:
            self._checkEvent()
            self._draw()
            self._updateContent()
            self._actioion()


class ButtonContent:
    def __init__(self, boderRect: pygame.Rect, text, fontSize: int, fontName: str = 'comic sans', bold: bool = True,
                 italic: bool = False):
        self.screen = pygame.display.get_surface()
        self._boderRect = boderRect
        self._text = text
        self.color = (255, 255, 255)
        self.fontName = fontName
        self.fontSize = fontSize
        self.fontBold = bold
        self.fontItalic = italic
        self.font = self._getFont()

        self._wRect = self._getWRect()
        self._horiD = 5  # khoảng cách 2 bên
        self._surList = self._getSurList(self._text, self._wRect)
        self._surRectList = self._getSurRect(self._surList, self._wRect)

    def _setup(self):
        pass

    def _getFont(self):
        return pygame.font.SysFont(self.fontName, self.fontSize, self.fontBold, self.fontItalic)

    def _getWRect(self):
        ws = self.font.render('a', True, (0, 0, 0))
        return ws.get_rect()

    def _analysText(self, txt: str, wRect: pygame.Rect):
        maxWidth = self._boderRect.width - self._horiD * 2
        words = txt.split(' ')
        lenWords = [len(word) * wRect.width for word in words]
        lenMax = max(max(lenWords), maxWidth)
        txtList = []
        temp = words[0]
        lTemp = lenWords[0]

        i = 1
        while i < len(words):
            if lTemp + lenWords[i] > lenMax:
                txtList.append(temp)
                temp = words[i]
                lTemp = lenWords[i]
            else:
                temp += words[i]
                lTemp += lenWords[i]
            i += 1
        txtList.append(temp)
        return txtList

    def _getSurList(self, txt, wRect):
        txtList = self._analysText(txt, wRect)
        return [self.font.render(t, True, self.color) for t in txtList]

    def _getSurRect(self, surList: list[pygame.Surface], wRect):
        y = self._boderRect.centery - (len(surList) * wRect.height) // 2
        rectList = []
        for sur in surList:
            rect = sur.get_rect(centerx=self._boderRect.centerx, y=y)
            rectList.append(rect)
            y += wRect.height
        return rectList

    def _reload(self):
        self._wRect = self._getWRect()
        self._surList = self._getSurList(self._text, self._wRect)
        self._surRectList = self._getSurRect(self._surList, self._wRect)

    def setFontSize(self, fontSize: int):
        self.fontSize = fontSize
        self.font = self._getFont()
        self._reload()

    def _draw(self):
        for i in range(len(self._surList)):
            self.screen.blit(self._surList[i], self._surRectList[i])

    def update(self):
        self._draw()


