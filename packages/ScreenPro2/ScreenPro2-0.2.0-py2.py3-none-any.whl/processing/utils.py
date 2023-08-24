import os
import sys
import numpy as np


def printNow(printInput):
    print(printInput)
    sys.stdout.flush()


def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError:
        # printNow(path + ' already exists')
        pass
