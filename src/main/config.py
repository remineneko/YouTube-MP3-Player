import configparser
from settings import *


def setup_config():
    '''
    Setups basic config for the app in the Settings section.
    '''
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

    if not os.path.isfile(os.path.join(DATA_FOLDER,'config.ini')):
        with open(os.path.join(DATA_FOLDER,'config.ini'), 'w') as configfile:
            config.write(configfile)


def _read_config(path):
    '''
    Reads the config file.
    :param path: Path to the config file.
    :return: The data from the config file.
    '''
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_user_music_location(path):
    '''
    Gets the location where the user stores the music
    :param path: The path to the config file
    :return: The path where the user stores the music
    '''
    return _read_config(path)['USER']['MusicLocation']


def get_user_playlist_default_folder(path):
    '''
        Gets the location where the user stores the playlists.
        :param path: The path to the config file
        :return: The path where the user stores the music
    '''
    return _read_config(path)['USER']['PlaylistDefaultFolder']


def get_user_flush_choice(path):
    '''
    Gets the user's choice of flushing.
    :param path:
    :return:
    '''
    return _read_config(path)['USER'].getboolean('AllowFlush')


def _modify_config(path, key, new_value):
    '''
    Modifies the config
    :param path: Path to the config file
    :param key: The key that needs changing
    :param new_value: The new value for the key
    :return:
    '''
    data = _read_config(path)
    data['USER'][key] = str(new_value)
    with open(path,'w') as f:
        data.write(f)


def modify_pl_loc(path, new_value):
    _modify_config(path, 'PlaylistDefaultFolder', new_value)


def modify_music_loc(path, new_value):
    _modify_config(path, 'MusicLocation', new_value)


def modify_flush_state(path, new_value):
    _modify_config(path, 'AllowFlush', new_value)


if __name__ =="__main__":
    setup_config()