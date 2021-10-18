class MediaMetadata:
    def __init__(self, info_dict:dict):
        '''
        Keeps track of the metadata of a YouTube video
        All keys:
        'id', 'title', 'formats', 'thumbnails', 'description', 'upload_date', 'uploader', 'uploader_id', 'uploader_url',
         'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url',
         'categories', 'tags', 'playable_in_embed', 'is_live', 'was_live', 'live_status', 'release_timestamp',
         'automatic_captions', 'subtitles', 'chapters', 'like_count', 'dislike_count', 'channel', 'track', 'artist',
         'album', 'creator', 'alt_title', 'availability', 'original_url', 'webpage_url_basename', 'extractor',
         'extractor_key', 'playlist', 'playlist_index', 'thumbnail', 'display_id', 'requested_subtitles', '__has_drm',
         'requested_formats', 'format', 'format_id', 'ext', 'width', 'height', 'resolution', 'fps', 'vcodec', 'vbr',
         'stretched_ratio', 'acodec', 'abr'
        :param info_dict: The dictionary containing the metadata of the video
        '''
        self._full_info = info_dict
        self.id = info_dict['id']
        self.title = info_dict['title']
        self.formats = info_dict['formats']
        self.thumbnails = info_dict['thumbnails']
        self.description = info_dict['description']
        self.upload_date = info_dict['upload_date']
        self.uploader = info_dict['uploader']
        self.uploader_id = info_dict['uploader_id']
        self.uploader_url = info_dict['uploader_url']
        self.channel_id = info_dict['channel_id']
        self.channel_url = info_dict['channel_url']
        self.duration = info_dict['duration']
        self.view_count = info_dict['view_count']
        self.average_rating = info_dict['average_rating']
        self.age_limit = info_dict['age_limit']
        self.webpage_url = info_dict['webpage_url']
        self.categories = info_dict['categories']
        self.tags = info_dict['tags']
        self.playable_in_embed = info_dict['playable_in_embed']
        self.is_live = info_dict['is_live']
        self.was_live = info_dict['was_live']
        self.live_status = info_dict['live_status']
        self.release_timestamp = info_dict['release_timestamp']
        self.automatic_captions = info_dict['automatic_captions']
        self.subtitles = info_dict['subtitles']
        self.chapters = info_dict['chapters']
        self.like_count = info_dict['like_count']
        self.dislike_count = info_dict['dislike_count']
        self.channel = info_dict['channel']
        self.track = info_dict['track']
        self.artist = info_dict['artist']
        self.album = info_dict['album']
        self.creator = info_dict['creator']
        self.alt_title = info_dict['alt_title']
        self.availability = info_dict['availability']
        self.original_url = info_dict['original_url']
        self.webpage_url_basename = info_dict['webpage_url_basename']
        self.extractor = info_dict['extractor']
        self.extractor_key = info_dict['extractor_key']
        self.playlist = info_dict['playlist']
        self.playlist_index = info_dict['playlist_index']
        self.thumbnail = info_dict['thumbnail']
        self.display_id = info_dict['display_id']
        self.requested_subtitles = info_dict['requested_subtitles']
        self.__has_drm = info_dict['__has_drm']
        self.requested_formats = info_dict['requested_formats']
        self.format = info_dict['format']
        self.format_id = info_dict['format_id']
        self.ext = info_dict['ext']
        self.width = info_dict['width']
        self.height = info_dict['height']
        self.resolution = info_dict['resolution']
        self.fps = info_dict['fps']
        self.vcodec = info_dict['vcodec']
        self.vbr = info_dict['vbr']
        self.stretched_ratio = info_dict['stretched_ratio']
        self.acodec = info_dict['acodec']
        self.abr = info_dict['abr']

    def __str__(self):
        print(self._full_info)



