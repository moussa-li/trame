from assets import LoadFileToUrl
from constantsymbol import Constant
from model import Model

__all__ = [
    "BottomModel"
]

class BottomModel(Model):
    def __init__(self, server, leftImage = "", rightImage = ""):
        super().__init__(server)
        
        self.leftImage = leftImage
        self.rightImage = rightImage

    @property
    def leftImage(self):
        return self.state[Constant.BOTTOM_LEFT_IMG_KEY]

    @leftImage.setter
    def leftImage(self, img):
        self.state[Constant.BOTTOM_LEFT_IMG_KEY] = LoadFileToUrl(Constant.BOTTOM_LEFT_IMG_KEY, img)

    @property
    def rightImage(self):
        return self.state[Constant.BOTTOM_RIGHT_IMG_KEY]

    @rightImage.setter
    def rightImage(self, img):
        self.state[Constant.BOTTOM_RIGHT_IMG_KEY] = LoadFileToUrl(Constant.BOTTOM_RIGHT_IMG_KEY, img)
