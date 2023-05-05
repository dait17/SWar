from gameTools import *
from pygame import mixer
from game import Game

mixer.init()


class Sound:
    _volume = HandleJson.readFile('..\\assets\\sound\\volume.json')
    bgsVolume = _volume.get("gbsVolume")
    effectVolume = _volume.get("effectVolume")

    BgChanel = mixer.Channel(0)
    PBChanel = mixer.Channel(1)
    EBChanel = mixer.Channel(2)
    EChanel = mixer.Channel(3)
    IChanel = mixer.Channel(4)

    mainSound = mixer.Sound(Path.getPath('..\\assets\\sound\\mainSound.mp3'))
    playingSound = mixer.Sound(Path.getPath('..\\assets\\sound\\playingSound.mp3'))

    clickSound = mixer.Sound(Path.getPath('..\\assets\\sound\\clickSound.wav'))
    shotSound = mixer.Sound(Path.getPath('..\\assets\\sound\\laser-gun-72558.mp3'))
    enemyShotSound = mixer.Sound(Path.getPath('..\\assets\\sound\\shoot02wav-14562.mp3'))
    collectSound = mixer.Sound(Path.getPath('..\\assets\\sound\\collectSound.mp3'))
    botExplosionSound = mixer.Sound(Path.getPath('..\\assets\\sound\\sinus-bomb-137068.mp3'))
    playerExplosionSound = mixer.Sound(Path.getPath('..\\assets\\sound\\explosion-5981.mp3'))
    wonSound = mixer.Sound(Path.getPath('..\\assets\\sound\\winSound.mp3'))



    @staticmethod
    def setVolume():
        Sound.mainSound.set_volume(Sound.bgsVolume)
        Sound.playingSound.set_volume(Sound.bgsVolume)
        Sound.wonSound.set_volume(Sound.bgsVolume)

        Sound.clickSound.set_volume(Sound.effectVolume)
        Sound.shotSound.set_volume(Sound.effectVolume/2)
        Sound.enemyShotSound.set_volume(Sound.effectVolume)
        Sound.collectSound.set_volume(Sound.effectVolume)
        Sound.botExplosionSound.set_volume(Sound.effectVolume)
        Sound.playerExplosionSound.set_volume(Sound.effectVolume)

    @staticmethod
    def mainSound_play():
        try:
            Sound.BgChanel.play(Sound.mainSound, -1,fade_ms=300)
        except Exception:
            pass

    @staticmethod
    def playingSound_play():
        try:
            Sound.BgChanel.play(Sound.playingSound, -1,fade_ms=300)
        except Exception:
            pass

    @staticmethod
    def clickSound_play():
        try:
            Sound.clickSound.play()
        except Exception:
            pass

    @staticmethod
    def shotSound_play():
        try:
            Sound.PBChanel.play(Sound.shotSound)
            # Sound.shotSound.play()
        except Exception:
            pass

    @staticmethod
    def enemyShotSound_play():
        try:
            Sound.EBChanel.play(Sound.enemyShotSound)
        except Exception:
            pass

    @staticmethod
    def collectSound_play():
        try:
            Sound.IChanel.play(Sound.collectSound)
        except Exception:
            pass

    @staticmethod
    def wonSound_play():
        try:
            Sound.wonSound.play()
            Sound.playingSound.stop()
        except Exception:
            pass


Sound.setVolume()

if __name__ == '__main__':
    # Sound.playingSound_play()
    Game.run()
