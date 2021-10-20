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


def _read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_user_music_location(path):
    return _read_config(path)['USER']['MusicLocation']


def get_user_playlist_default_folder(path):
    return _read_config(path)['USER']['PlaylistDefaultFolder']


def get_user_flush_choice(path):
    return _read_config(path)['USER'].getboolean('AllowFlush')


def modify_config(path,key, new_value):
    data = _read_config(path)
    data['USER'][key] = str(new_value)
    with open(path,'w') as f:
        data.write(f)

def modify_pl_loc(path, new_value):
    modify_config(path, 'PlaylistDefaultFolder', new_value)

def modify_music_loc(path, new_value):
    modify_config(path, 'MusicLocation', new_value)

def modify_flush_state(path, new_value):
    modify_config(path, 'AllowFlush', new_value)

if __name__ =="__main__":
    setup_config()