class _CoreAppException(Exception):
    '''
    One of base exceptions for the app, should be inherited when an error occurred within the app.
    '''
    pass


class _UserException(Exception):
    '''
    One of base exceptions for the app, should be inherited when an error is caused by user.
    '''
    pass


class LoadError(_CoreAppException):
    '''
    Raises when there is an error occurred while loading a video
    '''
    pass


class IncorrectFileTypeError(_UserException):
    '''
    Raises when file types other than JSON is being used when loading playlists.
    '''
    pass


class IncorrectJSONFileError(_UserException):
    '''
    Raises when the JSON file used is incorrect.
    '''
    pass


class InvalidInputError(_UserException):
    '''
    Raises when an input from the user is invalid
    '''
    pass


