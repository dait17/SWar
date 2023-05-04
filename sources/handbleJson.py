import json
import os
from path import Path as P


def readFile(path):
    path = P.getPath(path)
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return []


def write(path, content):
    path = P.getPath(path)
    with open(path, 'w') as file:
        json.dump(content, file)


def append(path, content: dict):
    old = readFile(path)
    old.update(content)
    write(path, old)
