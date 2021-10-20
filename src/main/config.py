import configparser
from settings import *


def setup_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'ConfigLocation': os.path.join(DATA_FOLDER, 'config.ini'),
        'MusicLocation': MUSIC_FOLDER,
        'PlaylistDefaultFolder': DEFAULT_PLAYLISTS_FOLDER,
        'AllowFlush': False
    }

    config['USER'] = {
        'MusicLocation': MUSIC_FOLDER,
        'PlaylistDefaultFolder': DEFAULT_PLAYLISTS_FOLDER,
        'AllowFlush': False
    }

    with open(os.path.join(DATA_FOLDER,'config.ini'), 'w') as configfile:
        config.write(configfile)


def _read_config(path, choice = 'USER'):
    config = configparser.ConfigParser()
    data = config.read(path)
    return config[choice]


def get_user_music_location(path):
    return _read_config(path)['MusicLocation']


def get_user_playlist_default_folder(path):
    return _read_config(path)['PlaylistDefaultFolder']


def get_user_flush_choice(path):
    return _read_config(path).getboolean('AllowFlush')


