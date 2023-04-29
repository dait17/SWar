from widget import Frame, Button
from gameTools import *


class MainFrame:
    def __init__(self):
        self._frame = self._getFrame()
        self._setupBnt()

    def _getFrame(self):
        fr = Frame(Screen.sRect.center, Screen.sRect.size, Image.load('..\\assets\\img_background\\pxfuel.jpg'))
        return fr

    def _getBntPlay(self):
        bnt = Button(self._frame.rect, [0, 0], [250, 50], "Play")
        bnt.posCenter(0,-100)
        bnt.connect(MainFrame._bntPlayFunc)
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




if __name__ == '__main__':
    from game import Game
    Game.setFrame(MainFrame())
    Game.run()

