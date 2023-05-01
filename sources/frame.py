from widget import Frame, Button
from gameTools import *
from map import Map
from sound import Sound
from game import Game


class MainFrame:
    def __init__(self):
        Sound.mainSound_play()
        self._frame = self._getFrame()
        self._setupBnt()

    def _getFrame(self):
        fr = Frame(Screen.sRect.center, Screen.sRect.size, Image.load('..\\assets\\img_background\\pxfuel.jpg'))
        return fr

    def _getBntPlay(self):
        bnt = Button(self._frame.rect, [0, 0], [250, 50], "Play")
        bnt.posCenter(0, -100)
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
        bnt = Button(self._frame.rect, [0, 0], [250, 50], "Exit")
        bnt.posCenter(0, 100)
        bnt.connect(MainFrame._bntExitFunc)
        return bnt

    def _setupBnt(self):
        self._frame.addBnt(self._getBntPlay())
        self._frame.addBnt(self._getBntSoundSetting())
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
        return path[:path.index('.json')]

    def _bntMap(self, mapName:str, dx,dy=0):
        bnt = Button(self._frame.rect, [0,0], [100,100], mapName)
        bnt.posCenter(dx,dy)
        return bnt

    def _setupBntMap(self):
        mp = 'assets\\map'
        maps = Path.getFiles(mp)
        map1Bnt = self._bntMap(self._getMapName(maps[0]),-100)
        map1Bnt.connect(lambda :( Game.setMap(Map(Path.getPath(mp+'\\'+maps[0]))),
                                  Sound.playingSound_play()))
        self._frame.addBnt(map1Bnt)

        map2Bnt = self._bntMap(self._getMapName(maps[1]), 100)
        map2Bnt.connect(lambda: Game.setMap(Map(Path.getPath(mp + '\\' + maps[1]))))
        self._frame.addBnt(map2Bnt)


    def update(self):
        # MapFrame._setupBntMap()
        self._frame.update()


if __name__ == '__main__':
    from game import Game

    Game.setFrame(MapFrame())
    Game.run()
