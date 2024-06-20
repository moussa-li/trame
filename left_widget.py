from left_model import LeftModel
from trame_vuetify.widgets import vuetify
from group_container import CreateGroupContainer
__all__ = [
    "LeftWidget"
]

class LeftWidget:
    def __init__(self, container, leftModel):
        self.model = leftModel
        self.container = container
        self.model.AddUpdataCallBack("LeftWidget", self.UpdateView)
        self.UpdateView()

    def UpdateView(self):
        self.container.clear()
        self.container.classes="pa-0 fill-height"
        self.container.style = "display:flex;flex-direction:column"
        # 遍历数据
        idx = 0
        count = len(self.model.infoGroup.items())
        with self.container:
            for key, data in self.model.infoGroup.items():
                with vuetify.VContainer(fluid=True, style="display:flex;flex-direction:column") as groupContainer:     
                    if(idx == count-1):
                        groupContainer.style ="flex:1"
                    with vuetify.VRow(align="center", justify="center", style="flex:0"):
                        vuetify.VChip(style="background-color:#2c56a3;color:#ffffff;font-size:20px", large=True,
                            depressed = True).set_text(key)      
                    with vuetify.VContainer(fluid=True, style="flex:1;background-color:#b0ccfe;height=100%") as container:  
                        container.add_child('<p></p>') 
                        for str in data:
                            container.add_child(f'<p>{str}</p>') 
                # if(idx == 1):                    
                #     with vuetify.VContainer(fluid=True, classes="blue fill-height") as groupContainer:
                #         with CreateGroupContainer(groupContainer, key) as container:                        
                #             container.add_child('<p></p>') 
                #             for str in data:
                #                 container.add_child(f'<p>{str}</p>') 
                # else:
                #     vuetify.VContainer(fluid=True, classes="red")
                #with groupcontainer:
                #     with CreateGroupContainer(groupContainer, key) as container:                        
                #         container.add_child('<p></p>') 
                #         for str in data:
                #             container.add_child(f'<p>{str}</p>') 
                idx += 1
            #vuetify.VSpacer(style="background-color:#b0ccfe")
            
            #         vuetify.VContainer(style="background-color:red", classes="pa-0 fill-height")
            #self.centerContainer = vuetify.VContainer(fluid=True, classes="red")   
            #self.bottomContainer = vuetify.VContainer(fluid=True, classes="blue fill-height")   