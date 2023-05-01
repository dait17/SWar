from gameTools import *
from pygame import mixer
from game import Game

mixer.init()


class Sound:
    _volume = HandleJson.readFile('..\\assets\\sound\\volume.json')
    bgsVolume = _volume.get("gbsVolume")
    effectVolume = _volume.get("effectVolume")

    Chanel = mixer.Channel(0)

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
        Sound.shotSound.set_volume(Sound.effectVolume)
        Sound.enemyShotSound.set_volume(Sound.effectVolume)
        Sound.collectSound.set_volume(Sound.effectVolume)
        Sound.botExplosionSound.set_volume(Sound.effectVolume)
        Sound.playerExplosionSound.set_volume(Sound.effectVolume)

    @staticmethod
    def mainSound_play():
        Sound.mainSound.play(-1,fade_ms=300)
        Sound.playingSound.stop()

    @staticmethod
    def playingSound_play():
        Sound.playingSound.play(-1, fade_ms=300)
        Sound.mainSound.stop()

    @staticmethod
    def clickSound_play():
        Sound.clickSound.play()

    @staticmethod
    def shotSound_play():
        Sound.shotSound.play()

    @staticmethod
    def enemyShotSound_play():
        Sound.enemyShotSound.play()

    @staticmethod
    def collectSound_play():
        Sound.collectSound.play()

    @staticmethod
    def wonSound_play():
        Sound.wonSound.play()
        Sound.playingSound.stop()


Sound.setVolume()

if __name__ == '__main__':
    # Sound.playingSound_play()
    Game.run()





