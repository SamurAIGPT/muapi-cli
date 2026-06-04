from .images import ImagesAPI
from .videos import VideosAPI
from .uploads import UploadsAPI
from .predictions import PredictionsAPI
from .audio import AudioAPI
from .models import ModelsAPI
from .accounts import AccountAPI
from .edit import EditAPI
from .enhance import EnhanceAPI
class MuAPI:
    def __init__(self):
        self.images = ImagesAPI()
        self.videos = VideosAPI()
        self.uploads = UploadsAPI()
        self.predictions = PredictionsAPI()
        self.audio = AudioAPI()
        self.models = ModelsAPI()
        self.account=AccountAPI()
        self.edit=EditAPI()
        self.enhance=EnhanceAPI()
        
