
from assets import LoadFileToUrl
from app_layout import AppLayout

from bottom_model import BottomModel
from bottom_widget import BottomWidget
from center_model import CenterModel
from center_widget import CenterWidget
from constantsymbol import Constant
from left_model import LeftModel
from left_widget import LeftWidget
from right_widget import RightWidget
from right_model import RightModel
from pathlib import Path
from trame.app import get_server
from trame.widgets import vuetify
from trame_vuetify.widgets import vuetify
from trame_client.widgets.core import VirtualNode
from trame_server import Server

import wslink
import web
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------
#server = get_server("wdd")
server = Server("wdd", VirtualNode)
server.enable_module(web)

state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Data setup
# -----------------------------------------------------------------------------

centerModel = CenterModel(server, [])
bottomModel = BottomModel(server, 'work_dir/bottom/001.png', 'work_dir/bottom/002.png')
leftModel = LeftModel(server, Path(__file__).parent / 'work_dir/left')
#rightModel = RightModel(server, Path(__file__).parent / 'work_dir/right')

# 数据版本更新
version = 0
globalLayoug = None
def UpdateModel():
    print(f'UpdateModel version-{version}')
    bottomModel.leftImage = "work_dir/bottom/001.png"
    bottomModel.rightImage = "work_dir/bottom/002.png"
    
    leftModel.UpdateModel()
    #rightModel.UpdateModel()

    if(globalLayoug):
        globalLayoug.flush_content()

    # 强制刷新
    state.flush()

def UpdateData():
    """
    监测数据版本是否已更新
    """
    path = Path(__file__).parent / "work_dir/version.txt"
    if(path.exists()):
        # 打开版本文件获取当前结果版本号
        versionFile = open(path.absolute(), 'rb')
        currentVersion = int(versionFile.read())
        versionFile.close()

        # 版本更新时调用更新回调
        global version
        if(currentVersion > version):
            version = currentVersion
            UpdateModel()
    
    wslink.schedule_callback(1.0, UpdateData)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# GUI elements
# -----------------------------------------------------------------------------

def StandardButtons():
    vuetify.VCheckbox(
        v_model=(Constant.LEFT_CONTAINER_VISIBILITY, True),
        on_icon="icon-left-checkbox-on",
        off_icon="icon-left-checkbox-off",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=(Constant.BOTTOM_CONTAINER_VISIBILITY,True),
         on_icon="icon-bottom-checkbox-on",
        off_icon="icon-bottom-checkbox-off",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    vuetify.VCheckbox(
        v_model=(Constant.RIGHT_CONTAINER_VISIBILITY,True),
         on_icon="icon-right-checkbox-on",
        off_icon="icon-right-checkbox-off",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "物理场在线监测应用系统"

with AppLayout(server) as layout:
    globalLayoug = layout
    layout.title.set_text("")
    
    with layout.toolbar:
        # toolbar components
        vuetify.VDivider(vertical=True, classes="mx-2")
        StandardButtons()

    # 中心三维可视化视口
    centerWidget = CenterWidget(layout.centerContainer, centerModel)
    
    # 底部图片展示
    # bottomWidget = BottomWidget(layout.bottomContainer, bottomModel)
    
    # 左侧信息显示
    # leftWidget = LeftWidget(layout.leftContainer, leftModel)

    # 右侧信息显示
    #rightWidget = RightWidget(layout.rightContainer)

if __name__ == "__main__":
        UpdateData()
        server.start()