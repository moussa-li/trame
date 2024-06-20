from trame_vuetify.widgets import vuetify


def CreateGroupContainer(container, tittle):
    with container:
        #添加标题
        with vuetify.VRow(align="center", justify="center"):
            vuetify.VChip(style="background-color:#2c56a3;color:#ffffff;font-size:20px", large=True,
                depressed = True).set_text(tittle)

            # 添加子容器
        return vuetify.VContainer(fluid=True, style="background-color:#b0ccfe;height=100%")