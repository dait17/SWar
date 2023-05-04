from widget import Frame, Button
from gameTools import *
from map import Map
#from sound import Sound
from game import Game


class MainFrame:
    def __init__(self):
        #Sound.mainSound_play()
        self._frame = self._getFrame()
        self._setupBnt()

    def _getFrame(self):
        fr = Frame(Screen.sRect.center, Screen.sRect.size, Image.load('..\\assets\\img_background\\pxfuel.jpg'))
        return fr

    def _getBntPlay(self):
        bnt = Button(self._frame.rect, [0, 0], [250, 70], "Play")
        bnt.posCenter(0, -70)
        bnt.connect(lambda: Game.setFrame(MapFrame()))
        return bnt

    def _getBntSoundSetting(self):
        bnt = Button(self._frame.rect, [0, 0], [250, 50], "Sound Setting")
        bnt.posCenter(0, 0)
        return bnt

    @staticmethod
    def _bntExitFunc():
        pygame.quit()
        sys.exit()

    @staticmethod
    def _bntPlayFunc():
        pass

    def _getBntExit(self):
        bnt = Button(self._frame.rect, [0, 0], [250, 70], "Exit")
        bnt.posCenter(0, 70)
        bnt.connect(MainFrame._bntExitFunc)
        return bnt

    def _setupBnt(self):
        self._frame.addBnt(self._getBntPlay())
        # self._frame.addBnt(self._getBntSoundSetting())
        self._frame.addBnt(self._getBntExit())

    def Enable(sefl):
        sefl._frame.setEnable()

    def Diasable(self):
        self._frame.setDisable()

    def update(self):
        self._frame.update()


class MapFrame:
    def __init__(self):
        self._frame = self._getFrame()
        self._setupBnt()

    def _getFrame(self):
        fr = Frame(Screen.sRect.center, Screen.sRect.size, Image.load('..\\assets\\img_background\\bg_green.jpg'))
        return fr

    def _getBntBack(self):
        bnt = Button(self._frame.rect, [0, 0], [80, 40], "Back")
        bnt.posTopleft(20, 10)
        bnt.connect(lambda: Game.setFrame(MainFrame()))
        return bnt

    def _setupBnt(self):
        self._frame.addBnt(self._getBntBack())
        self._setupBntMap()

    def _getMapName(self, path: str):
        st = 0
        if '\\' in path:
            st = path.rindex('\\') + 1
        return path[st:path.index('.json')]

    def _bntMap(self, mapName: str, dx, dy=0):
        bnt = Button(self._frame.rect, [0, 0], [150, 150], mapName)
        bnt.posCenter(dx, dy)
        return bnt

    def _getMapBG(self, mapPath):
        try:
            path = HandleJson.readFile(mapPath).get("background").get("imgPathList")[0]
            return Image.load(path)
        except Exception:
            return None

    def _createBntMap(self, mapPath, size):
        bnt = Button(self._frame.rect, [0, 0], size, self._getMapName(mapPath))
        bg = self._getMapBG(mapPath)
        bnt.setBackground(bg)
        bnt.connect(lambda: (
            Game.setMap(Map(Path.getPath(mapPath))),
            #Sound.playingSound_play()
        ))
        return bnt

    def _setPosBnt(self, bntList, size, distance):
        l = len(bntList)
        w, h = size
        dx, dy = distance
        maxBntW = int((Screen.sRect.width - dx) / (w + dx))
        maxW = min((w + dx) * l - dx, maxBntW * (w + dx) - dx)
        maxH = (round(l / maxBntW)) * (h + dy) - dy
        stX = (Screen.sRect.width - maxW) // 2
        stY = (Screen.sRect.height - maxH) // 2
        x, y = stX, stY
        for bnt in bntList:
            bnt.goto(*[x, y])
            x += w + dx
            if x > maxW:
                x = stX
                y += h + dy

    def _setupBntMap(self):
        mp = 'assets\\map\\'
        maps = Path.getFiles(mp)
        size = [300, 200]
        bntList = []
        for map in maps:
            bntList.append(self._createBntMap(mp + map, size))
            # self._frame.addBnt(self._createBntMap(mp+map,size))
        self._setPosBnt(bntList, size, [150, 100])
        self._frame.addBnt(*bntList)

    def update(self):
        # MapFrame._setupBntMap()
        self._frame.update()


if __name__ == '__main__':
    from game import Game

    Game.setFrame(MapFrame())
    Game.run()
