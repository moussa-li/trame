from assets import LoadFileToUrl
from constantsymbol import Constant
from trame.ui.vuetify import VAppLayout
from trame_client.ui.core import AbstractLayout
from trame_client.widgets import html
from trame_vuetify.widgets import vuetify

__all__ = [
    "AppLayout"
]

class AppLayout(VAppLayout):
    """
    页面布局，包含标题栏，左侧栏，中间栏，右侧栏，底边栏以及Footer
    """
    def __init__(self, _server, template_name="main", **kwargs):
        super().__init__(_server, template_name=template_name, **kwargs)
        with self:
            # 标题栏
            with vuetify.VAppBar(app=True, flat=True, style="background-color:#112b5c") as toolbar:
                # toolbar.src = LoadFileToUrl("app-bar-img", "web/www/asset/app-bar.png")
                self.toolbar = toolbar
                #self.icon = vuetify.VAppBarNavIcon()
                vuetify.VSpacer()
                self.title = vuetify.VToolbarTitle("application",style="color:#ffffff;font-size:40px")
                vuetify.VSpacer()
            
            # 主窗口
            with vuetify.VMain() as content:
                self.content = content
                with vuetify.VContainer(fluid=True, style="background-color:#112b5c;display:flex;flex-direction:row;flex-wrap:nowrap", classes="pa-0 fill-height"):
                    #with vuetify.VRow(classes="ma-0 pa-0", dense=True, style='height:100%'):
                        #with vuetify.VCol(cols="3"):
                            # 左侧栏
                            # self.leftContainer = vuetify.VContainer(fluid=True,v_show=(Constant.LEFT_CONTAINER_VISIBILITY,),style="flex:0 0 20%;max-width:20%")
                        
                        #with vuetify.VCol(cols="6"):
                            with vuetify.VContainer(classes="pa-0 fill-height", style="flex:1 0 60%;display:flex;flex-direction:column;flex-wrap:nowrap"):
                                # 中间栏
                                self.centerContainer = vuetify.VContainer(fluid=True, style="flex:1 0 100%;")   
                                #with vuetify.VRow(classes="ma-0 pa-0", dense=True, style='height:40%'):
                                # 底边栏
                                self.bottomContainer = vuetify.VContainer(fluid=True, style="flex:0 0 40%;max-height:40%",v_show=(Constant.BOTTOM_CONTAINER_VISIBILITY,))   
 
                        #with vuetify.VCol(cols="3"):
                            # 右侧栏
                            # self.rightContainer = vuetify.VContainer(fluid=True,v_show=(Constant.RIGHT_CONTAINER_VISIBILITY,),style="flex:0 0 20%;max-width:20%")
            #Footer
            with vuetify.VFooter(app=True, classes="my-0 py-0") as footer:
                self.footer = footer
                vuetify.VSpacer()
                reload = self.server.controller.on_server_reload
                if reload.exists():
                    with vuetify.VBtn(
                        x_small=True,
                        icon=True,
                        click=self.on_server_reload,
                        classes="mx-2",
                    ):
                        vuetify.VIcon("mdi-autorenew", x_small=True)               

                

    def on_server_reload(self):
        self.server.controller.on_server_reload(self.server)