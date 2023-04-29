import pygame, os, json, sys


class Path:
    motherFol = 'SWar'

    def __init__(self):
        pass

    @staticmethod
    def getMotherPath():
        cur_path = os.getcwd()
        return cur_path[:cur_path.index(Path.motherFol) + len(Path.motherFol)]

    @staticmethod
    def getPath(path):
        st = path.index(Path.motherFol) + len(Path.motherFol) if Path.motherFol in path else 0
        path = path[st:]
        path = path.strip('..')

        path = path.strip('\\')
        return Path.getMotherPath() + '\\' + path

    @staticmethod
    def fillPath(path: str):
        st = path.index(Path.motherFol) + len(Path.motherFol) if Path.motherFol in path else 0
        path = path[st:]
        path = path.strip('..')
        path = path.strip('\\')
        return path

    @staticmethod
    def getFiles(folder):
        return os.listdir(Path.getPath(folder))


class HandleJson:
    def __init__(self):
        pass

    @staticmethod
    def readFile(path):
        path = Path.getPath(path)
        if os.path.exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        return []

    @staticmethod
    def write(path, content):
        path = Path.getPath(path)
        with open(path, 'w') as file:
            json.dump(content, file)

    @staticmethod
    def append(path, content: dict):
        old = HandleJson.readFile(path)
        old.update(content)
        HandleJson.write(path, old)


class Image:
    @staticmethod
    def load(path):
        path = Path.getPath(path)
        if os.path.exists(path):
            try:
                return pygame.image.load(path).convert_alpha()
            except Exception:
                return None

    @staticmethod
    def smothscale(sur, size):
        try:
            return pygame.transform.smoothscale(sur, size)
        except Exception:
            return None


class Screen:
    sRect = pygame.Rect(0, 0, 1200, 750)
    screen = pygame.display.set_mode(sRect.size)

    @staticmethod
    def blit(sur, pos):
        try:
            Screen.screen.blit(sur, pos)
        except Exception:
            return False
        return True

    @staticmethod
    def drawRect(rect, color=(255, 0, 0), width=0, borderRadius=-1):
        pygame.draw.rect(Screen.screen, color, rect, width, borderRadius)


if __name__ == '__main__':
    pass
