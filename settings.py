import os

ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(ROOT_FOLDER, 'data')
DEFAULT_PLAYLISTS_FOLDER = os.path.join(DATA_FOLDER, "SavedPlaylists")
MUSIC_FOLDER = os.path.join(DATA_FOLDER, 'now_playing')
SRC_FOLDER = os.path.join(ROOT_FOLDER, "src")
MAIN_FOLDER = os.path.join(SRC_FOLDER, "main")

UI_FOLDER = os.path.join(SRC_FOLDER, "ui")
GENERATED_UI_FOLDER = os.path.join(UI_FOLDER, "generated")
SUBCLASSES_UI_FOLDER = os.path.join(UI_FOLDER, "subclasses")

ASSETS_FOLDER = os.path.join(ROOT_FOLDER, 'assets')



