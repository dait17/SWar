from bot import *
from game import Game
from gameTools import *
from messageBox import MessageBox
from player import Player
from items import Items


from sound import Sound


class Map:
    def __init__(self, mapPath):
        #Che do bat tu
        # p = Player()
        # p.bullets.setLevel(99999)
        # p.spaceship.maxHp = 99999
        # p.spaceship.hp = 99999
        # Game.setPlayer([p])
        Sound.playingSound_play()
        Game.setPlayer([Player()])
        self.data = self._loadData(mapPath)
        self.background = self.getBackground()
        self.items = self._getItems()
        self.rounds = []
        self.roundId = 0
        self.curRound = None
        self._setupRound()
        self._win = None
        self._wTime = 0
        self._enableTime = 0
        self._trans = True
        self._transTimer = pygame.time.get_ticks()
        self._transTime = 1000
        self.enable = True

    def _loadImg(self, path):
        path = Path.getPath(path)
        try:
            return pygame.image.load(path)
        except Exception:
            pass
        return None

    def _getBackgrounds(self, pathList: list):
        bgs = []
        for p in pathList:
            img = self._loadImg(p)
            if img is not None:
                bgs.append(img)
        return bgs

    def getBackground(self):
        background = self.data.get('background')
        pathList = background.get('imgPathList')
        ops = background.get('ops')
        bgs = self._getBackgrounds(pathList)
        return Background(bgs, ops)

    def _loadData(self, path):
        path = Path.getPath(path)
        return HandleJson.readFile(path)

    def _setupRound(self):
        rounds = self.data.get('rounds')
        for i in range(0, 4):
            round = Round(rounds.get(f'round{i + 1}'))
            self.rounds.append(round)
        self.curRound = self.getCurRound(self.roundId)

    def getCurRound(self, id):
        if id >= 4:
            return None
        return self.rounds[id]

    def _nextRound(self):
        self.roundId += 1
        self.curRound = self.getCurRound(self.roundId)
        if self.curRound is None:
            self._win = True

    def _handleRound(self):
        if len(Game.enemyList) == 0 and not self._trans:
            nbots = self.curRound.Next()
            if nbots is None:
                self._trans = True
                self._nextRound()
            else:
                Game.ExtendEnemy(nbots)
        else:
            if pygame.time.get_ticks() - self._transTimer >= self._transTime:
                self._trans = False

    def _won(self):
        if self._wTime == 0:
            Sound.wonSound_play()
            self._wTime = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self._wTime >= 1000:
            MessageBox.show('You win!', '', Game.srect.center, (0, 255, 0), 36)
            if self._enableTime == 0:
                self._enableTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self._enableTime >= 3000:
                self.enable = False

    def _lose(self):
        if self._wTime == 0:
            self._wTime = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self._wTime >= 1000:
            MessageBox.show('Game Over!', '', Game.srect.center, (255, 0, 0), 36)
            if self._enableTime == 0:
                self._enableTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self._enableTime >= 3000:
                self.enable = False

    def update(self):
        self.background.update()
        if self._win is None:
            self._handleRound()
            self.items.update()
            if len(Game.playerList) == 0:
                self._win = False
        elif self._win:
            self._won()
        else:
            self._lose()

    def _getItems(self):
        dropRate = self.data.get("items")
        return Items(dropRate)


class Background:
    def __init__(self, imgList, ops):
        self.imgList = imgList
        self.rectList = None
        self._xList = []
        self.ops = ops
        self.maxWidth = 0

        self._setup(self.imgList, ops)
        self.imgRect = None
        self._v = 0.1

    def _setup(self, imgList: list[pygame.Surface], ops: str):
        rl = []
        st = 0
        if ops.upper() == 'REPEAT':
            if len(imgList) == 1:
                newImg = imgList[0].copy()
                newImg = pygame.transform.flip(newImg, True, False)
                imgList.append(newImg)
        for img in imgList:
            rect = img.get_rect(y=0)
            rect.left = st
            rl.append(rect)
            self._xList.append(rect.x)
            st += rect.right - 1
            self.maxWidth += rect.width - 1
        self.rectList = rl

    def _updateRect(self):
        for i in range(len(self.rectList)):
            self._xList[i] -= self._v
            self.rectList[i].x = self._xList[i]
            if self.rectList[i].right < 0:
                self._xList[i] = self.maxWidth // len(self.rectList) - 1

    def update(self):
        if len(self.imgList) > 0:
            self._updateRect()
            for i in range(len(self.imgList)):
                Game.blit(self.imgList[i], self.rectList[i])
        else:
            Game.screen.fill((255, 255, 255))


class Round:
    def __init__(self, waveList: list[dict]):
        self.waveList = waveList
        self.waveCount = None
        self.curWave = None
        self._setup(waveList)

    def _setup(self, waveList: list):
        if len(waveList) > 0:
            self.waveCount = len(waveList)
            self.curWave = 0

    def _createGroupBot(self, data: dict):
        try:
            botName = data.get('botName')
            quantity = data.get('quantity')
            groupType = data.get('groupType')
            distance = data.get('distance')
            hp = data.get('hp')
            size = data.get('size')
            startPoint = data.get('startPoint')
            pointList = data.get('pointList')
            gb = Bots.getGroupBot(botName, quantity)
            for bot in gb:
                bot.setHP(hp)
                bot.setSize(size)

            BotGroup.setPointList(gb, groupType, distance, pointList, startPoint)

            return gb

        except Exception as e:
            print(e)
            MessageBox.show('Lỗi: ', 'Không tạo được bot', [100, 10])
            return []

    def getNormalBots(self, data):
        data = data.get('normalBot')
        bots = []
        for d in data:
            bots.extend(self._createGroupBot(d))
        return bots

    def _getSpecialBot(self, data):
        botName = data.get('botName')
        quantity = data.get('quantity')
        return Bots.getGroupBot(botName, quantity)

    def getSpecialBots(self, data):
        data = data.get('specialBot')
        bots = []
        for d in data:
            bots.extend(self._getSpecialBot(d))
        return bots

    def _getBoss(self, data):
        botName = data.get('botName')
        boss = Bots.getBot(botName)
        boss.setHP(data.get('hp'))
        boss.setSize(data.get('size'))

        return boss

    def getBoss(self, data):
        data = data.get("boss")
        bossList = []
        for d in data:
            bossList.append(self._getBoss(d))
        return bossList

    def Next(self):
        bots = []
        if self.curWave is not None:
            if self.curWave >= self.waveCount:
                return None
            try:
                data = self.waveList[self.curWave]
                bots.extend(self.getNormalBots(data))
                bots.extend(self.getSpecialBots(data))
                bots.extend(self.getBoss(data))
                self.curWave += 1
                return bots
            except Exception:
                MessageBox.show('Lỗi: ', 'Không lấy được curWave', [100, 30])
                return None
        else:
            return None


class BotGroup:

    def __init__(self):
        pass

    @staticmethod
    def _chainingDistance(startPoint, distance):
        dx, dy = distance
        stX, stY = startPoint
        if stY < 0:
            dx = 0
            dy = -dy
        elif stX < 0:
            dx = -dx
            dy = 0
        elif stX > Game.srect.width:
            dy = 0
        elif stY > Game.srect.height:
            dx = 0
        return dx, dy

    @staticmethod
    def chaining(bots: list[NormalBot], distance, pointList, startPoint):
        if len(bots) == 0:
            return
        dx, dy = distance

        dx += bots[0].spaceship.rect.width
        dy += bots[0].spaceship.rect.height

        dx, dy = BotGroup._chainingDistance(startPoint, [dx, dy])
        x, y = startPoint
        for bot in bots:
            bot.setPointList(pointList)
            bot.spaceship.gotoPos([x, y])
            y += dy
            x += dx

    @staticmethod
    def __is_prime(n):
        if n <= 1:
            return False
        for i in range(2, n):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def _find_closest_factors(target):
        m = 0
        while BotGroup.__is_prime(target):
            m += 1
            target -= 1
        min_diff = target
        r, c = target, 1
        for i in range(1, target + 1):
            if target % i == 0:
                j = target // i
                if abs(i - j) < min_diff:
                    min_diff = abs(i - j)
                    r, c = i, j
        return r, c, m

    @staticmethod
    def _getStartR(bots, rows, cols, mod, startPoint, dx, dy, maxW, maxH):
        stX = startPoint[0] - maxW // 2
        stY = startPoint[1] - maxH // 2
        x = stX
        y = stY
        i = 0
        for r in range(rows):
            for c in range(cols):
                bots[i].spaceship.goto(x, y)
                x += dx
                i += 1
            y += dy
            x = stX
        x = stX
        for j in range(mod):
            bots[i].spaceship.goto(x, y)
            x += dx
            i += 1

    @staticmethod
    def _createPointsR(x, y):
        return [[x, y], [x, y - 50], [x - 50, y], [x - 50, y - 50], [x, y - 50], [x, y]]

    @staticmethod
    def _setPointR(bots, rows, cols, mod, pointList, dx, dy, maxW, maxH):
        for point in pointList:
            stX = point[0] - maxW // 2
            stY = point[1] - maxH // 2
            x = stX
            y = stY
            i = 0
            dxx = 5
            dyy = 5
            for r in range(rows):
                for c in range(cols):
                    bots[i].appendPoint(BotGroup._createPointsR(x + dxx * i, y + dyy * i))
                    x += dx
                    i += 1
                x = stX
                y += dy
            for _ in range(mod):
                bots[i].appendPoint(BotGroup._createPointsR(*point))
                i += 1

        for bot in bots:
            bot.setAutomove()

    @staticmethod
    def rectangle(bots: list[NormalBot], distance, pointList, startPoint):
        l = len(bots)
        dx = bots[0].spaceship.rect.width + distance[0]
        dy = bots[0].spaceship.rect.height + distance[1]
        rows, cols, mod = BotGroup._find_closest_factors(l)
        maxW = cols * dx - distance[0]
        maxH = rows * dy - distance[1]
        BotGroup._getStartR(bots, rows, cols, mod, startPoint, dx, dy, maxW, maxH)
        BotGroup._setPointR(bots, rows, cols, mod, pointList, dx, dy, maxW, maxH)

    @staticmethod
    def setPointList(bots, groupType: str, distance, pointList, startPoint):
        groupType = groupType.upper()
        if groupType == "CHAINING":
            BotGroup.chaining(bots, distance, pointList, startPoint)
        elif groupType == "RECTANGLE":
            BotGroup.rectangle(bots, distance, pointList, startPoint)
