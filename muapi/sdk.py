from .images import ImagesAPI
from .videos import VideosAPI
from .uploads import UploadsAPI
from .predictions import PredictionsAPI


class MuAPI:
    def __init__(self):
        self.images = ImagesAPI()
        self.videos = VideosAPI()
        self.uploads = UploadsAPI()
        self.predictions = PredictionsAPI()