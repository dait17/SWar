import os


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



if __name__ == '__main__':
    print(Path.getPath('asd'))

