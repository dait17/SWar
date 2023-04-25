import os


class Path:
    def __init__(self):
        pass

    @staticmethod
    def getMotherPath():
        return os.getcwd()

    @staticmethod
    def getPath(path):
        s = 'SWar'
        st = path.index(s) + len(s) if s in path else 0
        path = path[st:]
        path = path.strip('..')

        path = path.strip('\\')
        return Path.getMotherPath() + '\\' + path



if __name__ == '__main__':
    print(Path.getPath('asd'))

