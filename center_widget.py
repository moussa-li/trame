from constantsymbol import Constant
from trame.widgets import vuetify, html, trame, vtk as vtk_widgets

__all__ = [
    "CenterWidget"
]

class Representation:
    Points = 0
    Wireframe = 1
    Surface = 2
    SurfaceWithEdges = 3

class LookupTable:
    Rainbow = 0
    Inverted_Rainbow = 1
    Greyscale = 2
    Inverted_Greyscale = 3

class PlaneType:
    X = 0
    Y = 1
    Z = 2

class CenterWidget:
    def __init__(self, container, centerModel):
        self.model = centerModel
        self.ctrl = self.model.ctrl
        self.state = self.model.state
        # 状态数据
        self.state.setdefault(Constant.CENTER_ACTIVE_UI, None)
        self.state.setdefault(Constant.CENTRE_TOOL_TIP, "")
        # 拾取
        self.enablePicking = False

        # 注册数据更新回调
        self.state.change(Constant.CENTER_RESULT_REPRESENTATION)(self.UpdateResultRepresentation)
        self.state.change(Constant.CENTER_PLANE_REPRESENTATION)(self.UpdatePlaneRepresentation)
        self.state.change(Constant.CENTER_RESULT_COLOR_ARRAY_IDX)(self.UpdateResultColorArray)
        self.state.change(Constant.CENTER_PLANE_COLOR_ARRAY_IDX)(self.UpdatePlaneColorArray)
        self.state.change(Constant.CENTER_RESULT_COLOR_PRESET)(self.UpdateResultColorPreset)
        self.state.change(Constant.CENTER_PLANE_COLOR_PRESET)(self.UpdatePlaneColorPreset)
        self.state.change(Constant.CENTER_RESULT_OPACITY)(self.UpdateResultOpacity)
        self.state.change(Constant.CENTER_PLANE_OPACITY)(self.UpdatePlaneOpacity)
        self.state.change(Constant.CENTER_PLANE_TYPE)(self.UpdatePlaneType)
        self.state.change(Constant.CENTER_PLANE_X_VALUE)(self.UpdatePlaneXValue)
        self.state.change(Constant.CENTER_PLANE_Y_VALUE)(self.UpdatePlaneYValue)
        self.state.change(Constant.CENTER_PLANE_Z_VALUE)(self.UpdatePlaneZValue)
        self.state.change(Constant.CENTER_ENABLE_PICKING)(self.UpdateEnablePicking)

        with container:
            container.style += ";position:relative"     
            trame.ClientTriggers(mounted=f"{Constant.CENTER_PIXEL_RATIO} = window.devicePixelRatio")
            with vuetify.VContainer(style="position:absolute;left:0px;top:10px;min-width:10px;max-width:10px;z-index:200;display:flex;flex-direction:column"):
                vuetify.VCheckbox(
                    on_icon="mdi-cube-outline",
                    off_icon="mdi-cube-off-outline",
                    classes="mx-1",
                    hide_details=True,
                    dense=True,
                    #style="position:absolute;left:10px;top:10px;z-index:200",
                    v_model=(Constant.CENTER_DRAWER_VISIBILITY, False),
                )
                vuetify.VCheckbox(
                     on_icon="mdi-lightbulb-off-outline",
                    off_icon="mdi-lightbulb-outline",
                    classes="mx-1",
                    hide_details=True,
                    dense=True,
                    #style="position:absolute;left:10px;top:10px;z-index:200",
                    v_model=(Constant.CENTER_ENABLE_PICKING, False),
                )
                with vuetify.VBtn(icon=True, 
                    #style="position:absolute;left:10px;top:40px;z-index:200",
                    click="$refs.view.resetCamera()"):
                        vuetify.VIcon("mdi-crop-free")
            self.drawerContainer = vuetify.VContainer(
                v_show=(Constant.CENTER_DRAWER_VISIBILITY,),
                classes="mx-1",
                hide_details=True,
                dense=True,
                style="background-color:#2c56a3;position:absolute;left:40px;top:25px;min-width:400px;max-width:400px;height:90%;z-index:200"
            )
            with vuetify.VCard(
                style=(Constant.CENTER_TOOL_TIP_STYLE, {"display": "none"}), elevation=2, outlined=True
            ):
                with vuetify.VCardText():                   
                    #{{centertooltip}}
                    html.Pre(f"{{{{{Constant.CENTRE_TOOL_TIP}}}}}")
            self.InitDrawer()

            #self.view = vtk_widgets.VtkLocalView(renderWindow)
            self.view = vtk_widgets.VtkRemoteView(
                view=self.model.GetRenderWindow(), 
                interactive_ratio=1,
                interactor_events=("events", ["LeftButtonPress"]),
                LeftButtonPress=(self.OnLeftButtonPress, f"[utils.vtk.event($event), {Constant.CENTER_PIXEL_RATIO}]"),
            )
            #self.ctrl.view_update = self.view.update
            self.ctrl.view_reset_camera = self.view.reset_camera
            self.ctrl.on_server_ready.add(self.view.update)

    def OnLeftButtonPress(self, event, pixelRatio):
        if(self.enablePicking):
            pos = event["position"]
            x = pos["x"]
            y = pos["y"]

            pickInfo = self.model.Pick(x, y)
            if(not pickInfo):
                self.model.state.update(
                    {
                        Constant.CENTRE_TOOL_TIP: "",
                        Constant.CENTER_TOOL_TIP_STYLE: {"display": "none"},
                    }
                ) 
                return 

            self.model.state[Constant.CENTRE_TOOL_TIP] = " ".join(pickInfo)
            self.model.state[Constant.CENTER_TOOL_TIP_STYLE] = {
                    "position": "absolute",
                    "left": f"{(x / pixelRatio )+ 20}px",
                    "bottom": f"{(y / pixelRatio ) + 20}px",
                    "zIndex": 100,
                    "pointerEvents": "none",
                }

    def InitDrawer(self):
        with self.drawerContainer:
            self.InitPipeLineWidget()
            vuetify.VDivider(classes="mb-2")
            self.InitResultCard()
            self.InitPlaneCard()

    def InitPipeLineWidget(self):
        trame.GitTree(
            sources=(
                "pipeline",
                [
                    {"id": "1", "parent": "0", "visible": 1, "name": "Result"},
                    {"id": "2", "parent": "1", "visible": 0, "name": "Plane"},
                ],
            ),
            width=370,
            actives_change=(self.OnActivesChange, "[$event]"),
            visibility_change=(self.OnVisibilityChange, "[$event]"),
        )

    def InitUiCard(self, title, uiName):
        with vuetify.VCard(v_show=f"{Constant.CENTER_ACTIVE_UI} == '{uiName}'"):
            vuetify.VCardTitle(
                title,
                classes="grey lighten-1 py-1 grey--text text--darken-3",
                style="user-select: none; cursor: pointer",
                hide_details=True,
                dense=True,
            )
            content = vuetify.VCardText(classes="py-2")
        return content

    def InitResultCard(self):
        with self.InitUiCard(title="Result", uiName="Result"):
            vuetify.VSelect(
                # Representation
                v_model=(Constant.CENTER_RESULT_REPRESENTATION, Representation.Surface),
                items=(
                    "representations",
                    [
                        {"text": "Points", "value": 0},
                        {"text": "Wireframe", "value": 1},
                        {"text": "Surface", "value": 2},
                        {"text": "SurfaceWithEdges", "value": 3},
                    ],
                ),
                label="Representation",
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
            with vuetify.VRow(classes="pt-2", dense=True):
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        # Color By
                        label="Color by",
                        v_model=(Constant.CENTER_RESULT_COLOR_ARRAY_IDX, 0),
                        items=("array_list", self.model.GetMeshDataSetArrays()),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        # Color Map
                        label="Colormap",
                        v_model=(Constant.CENTER_RESULT_COLOR_PRESET, LookupTable.Rainbow),
                        items=(
                            "colormaps",
                            [
                                {"text": "Rainbow", "value": 0},
                                {"text": "Inv Rainbow", "value": 1},
                                {"text": "Greyscale", "value": 2},
                                {"text": "Inv Greyscale", "value": 3},
                            ],
                        ),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
            vuetify.VSlider(
                # Opacity
                v_model=(Constant.CENTER_RESULT_OPACITY, 1.0),
                min=0,
                max=1,
                step=0.1,
                label="Opacity",
                classes="mt-1",
                hide_details=True,
                dense=True,
            )


    def InitPlaneCard(self):
        with self.InitUiCard(title="Plane", uiName="Plane"):
            vuetify.VSelect(
                # Contour By
                label="Plane Type",
                v_model=(Constant.CENTER_PLANE_TYPE, 0),
                items=("type_list", 
                    [
                        {"text": "X", "value": 0},
                        {"text": "Y", "value": 1},
                        {"text": "Z", "value": 2},
                    ],
                ),
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
            self.InitPlaneDataContainer(0, Constant.CENTER_PLANE_X_VALUE)
            self.InitPlaneDataContainer(1, Constant.CENTER_PLANE_Y_VALUE)
            self.InitPlaneDataContainer(2, Constant.CENTER_PLANE_Z_VALUE)
            
            vuetify.VSelect(
                # Representation
                v_model=(Constant.CENTER_PLANE_REPRESENTATION, Representation.Surface),
                items=(
                    "representations",
                    [
                        {"text": "Points", "value": 0},
                        {"text": "Wireframe", "value": 1},
                        {"text": "Surface", "value": 2},
                        {"text": "SurfaceWithEdges", "value": 3},
                    ],
                ),
                label="Representation",
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
            with vuetify.VRow(classes="pt-2", dense=True):
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        # Color By
                        label="Color by",
                        v_model=(Constant.CENTER_PLANE_COLOR_ARRAY_IDX, 0),
                        items=("array_list", self.model.GetMeshDataSetArrays()),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        # Color Map
                        label="Colormap",
                        v_model=(Constant.CENTER_PLANE_COLOR_PRESET, LookupTable.Rainbow),
                        items=(
                            "colormaps",
                            [
                                {"text": "Rainbow", "value": 0},
                                {"text": "Inv Rainbow", "value": 1},
                                {"text": "Greyscale", "value": 2},
                                {"text": "Inv Greyscale", "value": 3},
                            ],
                        ),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
            vuetify.VSlider(
                # Opacity
                v_model=(Constant.CENTER_PLANE_OPACITY, 1.0),
                min=0,
                max=1,
                step=0.1,
                label="Opacity",
                classes="mt-1",
                hide_details=True,
                dense=True,
            )

    def InitPlaneDataContainer(self, containerName, modelName):
        with vuetify.VContainer(v_show=f"{Constant.CENTER_PLANE_TYPE} == {containerName}"):
            vuetify.VSlider(
                    # Contour Value
                    v_model=(modelName, 0.5),
                    min=("contour_min", 0),
                    max=("contour_max", 1),
                    step=("contour_step", 0.05),
                    label="Percent",
                    classes="my-1",
                    hide_details=True,
                    dense=True,
                )


    @staticmethod
    def UpdateRepresentation(actor, mode):
        property = actor.GetProperty()
        if mode == Representation.Points:
            property.SetRepresentationToPoints()
            property.SetPointSize(5)
            property.EdgeVisibilityOff()
        elif mode == Representation.Wireframe:
            property.SetRepresentationToWireframe()
            property.SetPointSize(1)
            property.EdgeVisibilityOff()
        elif mode == Representation.Surface:
            property.SetRepresentationToSurface()
            property.SetPointSize(1)
            property.EdgeVisibilityOff()
        elif mode == Representation.SurfaceWithEdges:
            property.SetRepresentationToSurface()
            property.SetPointSize(1)
            property.EdgeVisibilityOn()

    def UpdateResultRepresentation(self, **kwargs):
        self.UpdateRepresentation(self.model.meshActor, kwargs[Constant.CENTER_RESULT_REPRESENTATION])
        self.view.update()
    
    def UpdatePlaneRepresentation(self, **kwargs):
        self.UpdateRepresentation(self.model.planeActor, kwargs[Constant.CENTER_PLANE_REPRESENTATION])
        self.view.update()

    def OnActivesChange(self, ids):
        _id = ids[0]
        if _id == "1":  # Mesh
            self.state[Constant.CENTER_ACTIVE_UI] = "Result"
        elif _id == "2":  # Contour
            self.state[Constant.CENTER_ACTIVE_UI] = "Plane"
        else:
            self.state[Constant.CENTER_ACTIVE_UI] = "nothing"

    def OnVisibilityChange(self, event):
        _id = event["id"]
        _visibility = event["visible"]

        if _id == "1":  # Mesh
            self.model.SetMeshVisible(_visibility)
        elif _id == "2":  # Plane
            self.model.SetPlaneVisible(_visibility)
        self.view.update() 

    def UpdateResultColorArray(self, **kwargs):
        self.model.UpdateResultCololrIdx(kwargs[Constant.CENTER_RESULT_COLOR_ARRAY_IDX])
        self.view.update()

    def UpdatePlaneColorArray(self, **kwargs):
        self.model.UpdatePlaneColorIdx(kwargs[Constant.CENTER_PLANE_COLOR_ARRAY_IDX])
        self.view.update()

    @staticmethod
    def UsePreset(actor, preset):
        lut = actor.GetMapper().GetLookupTable()
        if preset == LookupTable.Rainbow:
            lut.SetHueRange(0.666, 0.0)
            lut.SetSaturationRange(1.0, 1.0)
            lut.SetValueRange(1.0, 1.0)
        elif preset == LookupTable.Inverted_Rainbow:
            lut.SetHueRange(0.0, 0.666)
            lut.SetSaturationRange(1.0, 1.0)
            lut.SetValueRange(1.0, 1.0)
        elif preset == LookupTable.Greyscale:
            lut.SetHueRange(0.0, 0.0)
            lut.SetSaturationRange(0.0, 0.0)
            lut.SetValueRange(0.0, 1.0)
        elif preset == LookupTable.Inverted_Greyscale:
            lut.SetHueRange(0.0, 0.666)
            lut.SetSaturationRange(0.0, 0.0)
            lut.SetValueRange(1.0, 0.0)
        lut.Build() 

    def UpdateResultColorPreset(self, **kwargs):
        CenterWidget.UsePreset(self.model.meshActor, kwargs[Constant.CENTER_RESULT_COLOR_PRESET])
        self.view.update()

    def UpdatePlaneColorPreset(self, **kwargs):
        CenterWidget.UsePreset(self.model.planeActor, kwargs[Constant.CENTER_PLANE_COLOR_PRESET])
        self.view.update()

    def UpdateResultOpacity(self, **kwargs):
        self.model.meshActor.GetProperty().SetOpacity(kwargs[Constant.CENTER_RESULT_OPACITY])
        self.view.update()


    def UpdatePlaneOpacity(self, **kwargs):
        self.model.planeActor.GetProperty().SetOpacity(kwargs[Constant.CENTER_PLANE_OPACITY])
        self.view.update()

    def UpdatePlaneType(self, **kwargs):
        planeType = kwargs[Constant.CENTER_PLANE_TYPE]
        percent = 0.5
        if(planeType == 0):
            percent = self.model.state[Constant.CENTER_PLANE_X_VALUE]
        if(planeType == 1):
            percent = self.model.state[Constant.CENTER_PLANE_Y_VALUE]
        if(planeType == 2):
            percent = self.model.state[Constant.CENTER_PLANE_Z_VALUE]
        self.model.UpdatePlanePosition(planeType, percent)
        self.view.update()

    def UpdatePlaneXValue(self, **kwargs):
        self.model.UpdatePlanePosition(0, kwargs[Constant.CENTER_PLANE_X_VALUE])
        self.view.update()

    def UpdatePlaneYValue(self, **kwargs):
        self.model.UpdatePlanePosition(1, kwargs[Constant.CENTER_PLANE_Y_VALUE])
        self.view.update()
    
    def UpdatePlaneZValue(self, **kwargs):
        self.model.UpdatePlanePosition(2, kwargs[Constant.CENTER_PLANE_Z_VALUE])
        self.view.update()

    def UpdateEnablePicking(self, **kwargs):
        self.model.ClearPreSel()
        self.enablePicking = kwargs[Constant.CENTER_ENABLE_PICKING]
        # 先隐藏
        self.model.state.update(
            {
                Constant.CENTRE_TOOL_TIP: "",
                Constant.CENTER_TOOL_TIP_STYLE: {"display": "none"},
            }
        )
        self.view.update()
