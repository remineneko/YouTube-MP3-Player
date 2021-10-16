import subprocess
import sys
import os

from settings import *


def convert(target_name:str):
    if target_name[target_name.rfind('.') + 1:] == 'ui':
        subprocess.check_call([sys.executable, "-m", "PyQt5.uic.pyuic", "-x", target_name,  '-o', target_name[:target_name.rfind('.')]+".py"])


if __name__ == '__main__':
    for file in os.listdir(ASSETS_FOLDER):
        convert(os.path.join(ASSETS_FOLDER,file))



