from bottom_model import BottomModel
from constantsymbol import Constant
from trame_vuetify.widgets import vuetify

__all__ = [
    "BottomWidget"
]

class BottomWidget:
    def __init__(self, container, bottomModel):
        self.model = bottomModel
        with container:
            #  with vuetify.VRow(classes="fill-height ma-0 pa-0", align="center", justify="center"):
            #     with vuetify.VCol(cols="6"):
            #         self.leftImage = vuetify.VImg(style="max-height:100%",
            #         src = (Constant.BOTTOM_LEFT_IMG_KEY, self.model.leftImage))
            #     with vuetify.VCol(cols="6"):
            #         self.rightImage = vuetify.VImg(style="max-height:100%",
            #         src = (Constant.BOTTOM_RIGHT_IMG_KEY, self.model.rightImage))
            with vuetify.VContainer(fluid=True, style="height:100%;display:flex;flex-direction:row;flex-wrap:nowrap", classes="ma-0 pa-0"):
                self.leftImage = vuetify.VImg(style="flex:1",classes="mx-1",
                     src = (Constant.BOTTOM_LEFT_IMG_KEY, self.model.leftImage))
                self.rightImage = vuetify.VImg(style="flex:1",classes="mx-1",
                     src = (Constant.BOTTOM_RIGHT_IMG_KEY, self.model.rightImage))
                pass
    