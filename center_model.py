import os
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import(
    vtkDataObject, 
    vtkPlane, 
    vtkUnstructuredGrid
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkFiltersCore import vtkCutter
from model import Model
from vtkmodules.vtkRenderingCore import(
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkPointPicker,
    vtkProperty,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkLight
)
#from case2vtu import case2vtu
""" case = case2vtu()
 """
# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

__all__ = [
    "CenterModel"
]

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

class CenterModel(Model):
    def __init__(self, server, fileList):
        super().__init__(server)
        renderer = vtkRenderer()
        renderer.SetBackground(0.68, 0.8, 1.0)
        renderWindow = vtkRenderWindow()
        renderWindow.DoubleBufferOn()
        renderWindow.AddRenderer(renderer)
        # renderWindow.SetOffScreenRendering(1)

        # Light
        lightInfo = [(2,48,0.8),(-41,-49,0.6),(48,-34,0.5)]
        for info in lightInfo:
            light = vtkLight()        
            light.SetLightTypeToCameraLight()
            light.SetDirectionAngle(info[0], info[1])
            light.SetIntensity(info[2])
            renderer.AddLight(light)

        renderWindowInteractor = vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()        

        # Read Data
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(os.path.join(CURRENT_DIRECTORY, "case_t0001.vtu"))
        reader.Update()

        # Extract Array/Field information
        dataset_arrays = []
        fields = [
            (reader.GetOutput().GetPointData(), vtkDataObject.FIELD_ASSOCIATION_POINTS),
            (reader.GetOutput().GetCellData(), vtkDataObject.FIELD_ASSOCIATION_CELLS),
        ]
        for field in fields:
            field_arrays, association = field
            for i in range(field_arrays.GetNumberOfArrays()):
                array = field_arrays.GetArray(i)
                array_range = array.GetRange()
                dataset_arrays.append(
                    {
                        "text": array.GetName(),
                        "value": i,
                        "range": list(array_range),
                        "type": association,
                    }
                )
        default_array = dataset_arrays[0]
        default_min, default_max = default_array.get("range")

        # Mesh
        plane = vtkPlane()
        mesh_mapper = vtkDataSetMapper()
        mesh_mapper.SetInputConnection(reader.GetOutputPort())
        mesh_actor = vtkActor()
        mesh_actor.SetMapper(mesh_mapper)
        renderer.AddActor(mesh_actor)

        # Mesh: Setup default representation to surface
        mesh_actor.GetProperty().SetRepresentationToSurface()
        mesh_actor.GetProperty().SetPointSize(1)
        mesh_actor.GetProperty().EdgeVisibilityOff()

        # Mesh: Apply rainbow color map
        mesh_lut = mesh_mapper.GetLookupTable()
        mesh_lut.SetHueRange(0.666, 0.0)
        mesh_lut.SetSaturationRange(1.0, 1.0)
        mesh_lut.SetValueRange(1.0, 1.0)
        mesh_lut.Build()

        # Mesh: Color by default array
        mesh_mapper.SelectColorArray(default_array.get("text"))
        mesh_mapper.GetLookupTable().SetRange(default_min, default_max)
        if default_array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
            mesh_mapper.SetScalarModeToUsePointFieldData()
        else:
            mesh_mapper.SetScalarModeToUseCellFieldData()
        mesh_mapper.SetScalarVisibility(True)
        mesh_mapper.SetUseLookupTableScalarRange(True)

        # Mesh Scalar Bar
        meshBarActor = vtkScalarBarActor()
        meshBarActor.SetLookupTable(mesh_lut)
        meshBarActor.SetTitle(default_array.get("text"))
        meshBarActor.SetDragable(True)
        meshBarActor.SetPosition( 0.92, 0.05)
        meshBarActor.SetPosition2( 0.07, 0.9 )
        renderer.AddActor2D(meshBarActor)
        
        # Plane
        plane = vtkPlane()
        plane.SetNormal(1, 0, 0)
        plane.SetOrigin(reader.GetOutput().GetCenter())
        planeCutter = vtkCutter()
        planeCutter.SetInputConnection(reader.GetOutputPort())    
        planeCutter.SetCutFunction(plane)    
        planeMapper = vtkDataSetMapper()
        planeMapper.SetInputConnection(planeCutter.GetOutputPort())
        planeActor = vtkActor()
        planeActor.SetMapper(planeMapper)
        renderer.AddActor(planeActor)

        # Contour: Setup default representation to surface
        planeActor.GetProperty().SetRepresentationToSurface()
        planeActor.GetProperty().SetPointSize(1)
        planeActor.GetProperty().EdgeVisibilityOff()
        
        # Plane: Apply rainbow color map
        planeLut = planeMapper.GetLookupTable()
        planeLut.SetHueRange(0.666, 0.0)
        planeLut.SetSaturationRange(1.0, 1.0)
        planeLut.SetValueRange(1.0, 1.0)
        planeLut.Build()

        # Contour: Color by default array
        planeMapper.SelectColorArray(default_array.get("text"))
        planeMapper.GetLookupTable().SetRange(default_min, default_max)
        if default_array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
            planeMapper.SetScalarModeToUsePointFieldData()
        else:
            planeMapper.SetScalarModeToUseCellFieldData()
        planeMapper.SetScalarVisibility(True)
        planeMapper.SetUseLookupTableScalarRange(True)

        # Mesh Scalar Bar
        planeBarActor = vtkScalarBarActor()
        planeBarActor.SetLookupTable(planeLut)
        planeBarActor.SetTitle(default_array.get("text"))
        planeBarActor.SetDragable(True)
        planeBarActor.SetPosition( 0.84, 0.05)
        planeBarActor.SetPosition2(0.07, 0.9)
        renderer.AddActor2D(planeBarActor)

        # # Cube Axes
        # cube_axes = vtkCubeAxesActor()
        # renderer.AddActor(cube_axes)

        # # Cube Axes: Boundaries, camera, and styling
        # cube_axes.SetBounds(mesh_actor.GetBounds())
        # cube_axes.SetCamera(renderer.GetActiveCamera())
        # cube_axes.SetXLabelFormat("%6.1f")
        # cube_axes.SetYLabelFormat("%6.1f")
        # cube_axes.SetZLabelFormat("%6.1f")
        # cube_axes.SetFlyModeToOuterEdges()

        # 高亮
        preSelProperty=vtkProperty()
        preSelProperty.SetColor(1, 0, 0)
        preSelProperty.SetAmbient(1)
        preSelProperty.SetDiffuse(1)
        preSelProperty.SetSpecular(1)
        preSelProperty.SetSpecularPower(5)
        preSelProperty.SetLineWidth(3.0)
        preSelProperty.SetPointSize(4.0)
        preSelData=vtkUnstructuredGrid()
        preSelActor=vtkActor()
        preSelActor.SetProperty(preSelProperty)
        renderer.AddActor(preSelActor)

        preSelmapper = vtkDataSetMapper()
        preSelActor.SetMapper(preSelmapper)
        preSelmapper.SetInputData(preSelData)
        preSelmapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1.0, -1.0)
        preSelmapper.SetRelativeCoincidentTopologyLineOffsetParameters(-1.0, -1.0)

        renderer.ResetCamera()

        # 记录成员变量
        self.renderWindow = renderWindow
        self.renderer = renderer
        self.meshActor = mesh_actor
        self.meshBarActor = meshBarActor
        self.plane = plane
        self.planeActor = planeActor
        self.planeBarActor = planeBarActor
        self.meshDataSetArrays = dataset_arrays
        self.interactor = renderWindowInteractor
        self.cellPicker = vtkCellPicker()
        self.meshColorIdx = 0
        self.preSelData = preSelData
        self.preSelActor = preSelActor

        # 初始状态下隐藏平面
        self.SetPlaneVisible(False)

    def GetRenderWindow(self):
        return self.renderWindow

    def SetMeshVisible(self, flag):
        self.meshActor.SetVisibility(flag)
        self.meshBarActor.SetVisibility(flag)
        self.preSelActor.SetVisibility(flag)

    def SetPlaneVisible(self,flag):
        self.planeActor.SetVisibility(flag)
        self.planeBarActor.SetVisibility(flag)

    def GetMeshDataSetArrays(self):
        return self.meshDataSetArrays

    def ColorByArray(actor, barActor, array):
        _min, _max = array.get("range")
        mapper = actor.GetMapper()
        mapper.SelectColorArray(array.get("text"))
        barActor.SetTitle(array.get("text"))
        mapper.GetLookupTable().SetRange(_min, _max)
        if array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
            mapper.SetScalarModeToUsePointFieldData()
        else:
            mapper.SetScalarModeToUseCellFieldData()
        mapper.SetScalarVisibility(True)
        mapper.SetUseLookupTableScalarRange(True)

    def UpdateResultCololrIdx(self, idx):
        self.meshColorIdx = idx
        array = self.meshDataSetArrays[idx]
        CenterModel.ColorByArray(self.meshActor, self.meshBarActor, array)

    def UpdatePlaneColorIdx(self, idx):
        array = self.meshDataSetArrays[idx]
        CenterModel.ColorByArray(self.planeActor, self.planeBarActor, array)

    def UpdatePlanePosition(self, planeType, percent):
        """
        @param planeType 0-X 1-Y 2-Z
        @param percent 0-1
        """
        bounds = self.meshActor.GetBounds()
        centerX = (bounds[1] + bounds[0])/2.0
        centerY = (bounds[3] + bounds[2])/2.0
        centerZ = (bounds[5] + bounds[4])/2.0
        
        if(planeType == 0):
            self.plane.SetNormal(1,0,0)
            centerX = bounds[0] + (bounds[1]- bounds[0])*percent
        if(planeType == 1):
            self.plane.SetNormal(0,1,0)
            centerY = bounds[2] + (bounds[3]- bounds[2])*percent
        if(planeType == 2):
            self.plane.SetNormal(0,0,1)
            centerZ = bounds[4] + (bounds[5]- bounds[4])*percent
        self.plane.SetOrigin(centerX, centerY, centerZ)

    def Pick(self, x, y):
        self.preSelData.Initialize()

        # 网格隐藏时不拾取（平面不进行拾取）
        if(not self.meshActor.GetVisibility()):
            return None

        data = self.meshActor.GetMapper().GetInput()

        # 拾取
        colorArray = self.meshDataSetArrays[self.meshColorIdx]
        if(colorArray.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS):
            self.cellPicker.Pick(x, y, 0, self.GetRenderWindow().GetRenderers().GetFirstRenderer())
            selPointId = self.cellPicker.GetPointId()
            if(selPointId != -1):
                pointData = data.GetPointData()
                array = pointData.GetScalars(colorArray.get("text"))
                if(not array):
                    return None

                result = []
                result.append(f"PointId={selPointId}")
                result.append(f"Value={array.GetValue(selPointId)}")

                # 高亮     
                self.preSelData.Allocate(10)
                self.preSelData.SetPoints(data.GetPoints())
                self.preSelData.InsertNextCell(1, 1, [selPointId])
                return result

        if(colorArray.get("type") == vtkDataObject.FIELD_ASSOCIATION_CELLS):
            self.cellPicker.Pick(x, y, 0, self.GetRenderWindow().GetRenderers().GetFirstRenderer())
            selCellId = self.cellPicker.GetCellId()
            if(selCellId != -1):
                cellData = data.GetCellData()
                array = cellData.GetScalars(colorArray.get("text"))
                if(not array):
                    return None
                
                result = []
                result.append(f"CellId={selCellId}")
                result.append(f"Value={array.GetValue(selCellId)}")

                # 高亮
                self.preSelData.Allocate(10)
                self.preSelData.SetPoints(data.GetPoints())
                cell = data.GetCell(selCellId)
                print(cell.GetPointIds())
                self.preSelData.InsertNextCell(cell.GetCellType(),
                    cell.GetPointIds())
                return result

        return None

    def ClearPreSel(self):
        self.preSelData.Initialize()
