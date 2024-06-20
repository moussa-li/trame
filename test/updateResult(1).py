from vtkmodules.vtkFiltersSources import vtkConeSource,vtkPointSource
from vtkmodules.vtkCommonCore import (
    vtkPoints,vtkFloatArray,vtkLookupTable,vtkIdList
)

from vtkmodules.vtkCommonDataModel import( 
    vtkUnstructuredGrid,
    vtkTriangle,
    vtkHexahedron,
    vtkTetra,
    vtkQuad
) 
import vtkmodules.vtkCommonDataModel as vtk
from vtkmodules.vtkRenderingCore import(
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)
# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor,vtkAxesActor
# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

from vtkmodules.vtkRenderingAnnotation import vtkAxesActor

#创建灰色渲染grid1和渐变渲染网格grid2
grid1 = vtkUnstructuredGrid()
#grid2 = vtkUnstructuredGrid()

#grid1节点数据存储
points = vtkPoints()
points.InsertNextPoint(0,0,0)
points.InsertNextPoint(1,0,0)
points.InsertNextPoint(1,1,0)
points.InsertNextPoint(0,1,0)
points.InsertNextPoint(0,0,1)
points.InsertNextPoint(1,0,1)
points.InsertNextPoint(1,1,1)
points.InsertNextPoint(0,1,1)
points.InsertNextPoint(0,2,0)
points.InsertNextPoint(2,2,0)
points.InsertNextPoint(0,4,0)
points.InsertNextPoint(3,3,4)

'''
#测试节点数据获取方式
pointNum = points.GetNumberOfPoints()
for j in range(pointNum):
    point = points.GetPoint(j)
    print("point '%s' xcoord '%s' ycoord '%s' zcoord '%s'",j,point[0],point[1],point[2])
'''

grid1.SetPoints(points)

#grid1单元数据存储
hex = vtkHexahedron()
hex.GetPointIds().SetId(0,0)
hex.GetPointIds().SetId(1,1)
hex.GetPointIds().SetId(2,2)
hex.GetPointIds().SetId(3,3)
hex.GetPointIds().SetId(4,4)
hex.GetPointIds().SetId(5,5)
hex.GetPointIds().SetId(6,6)
hex.GetPointIds().SetId(7,7)
grid1.InsertNextCell(vtk.VTK_HEXAHEDRON,hex.GetPointIds())

#测试：获取hex单元面上的每个点
'''
num = hex.GetNumberOfFaces()
for i in range(num):
    face= hex.GetFace(i)
    pointsIds = face.GetPointIds()
    for i in range(pointsIds.GetNumberOfIds()):
        index = pointsIds.GetId(i)
        point = points.GetPoint(index)
        print("hexface '%s' xcoord '%s' ycoord '%s' zcoord '%s'",index,point[0],point[1],point[2])
'''

tet = vtkTetra()
tet.GetPointIds().SetId(0,8)
tet.GetPointIds().SetId(1,9)
tet.GetPointIds().SetId(2,10)
tet.GetPointIds().SetId(3,11)
grid1.InsertNextCell(vtk.VTK_TETRA,tet.GetPointIds())

#测试：获取tet单元面上的每个点
'''
num = tet.GetNumberOfFaces()
for i in range(num):
    face= tet.GetFace(i)
    pointsIds = face.GetPointIds()
    for i in range(pointsIds.GetNumberOfIds()):
        index = pointsIds.GetId(i)
        point = points.GetPoint(index)
        print("tetface '%s' xcoord '%s' ycoord '%s' zcoord '%s'",index,point[0],point[1],point[2])
'''
'''
#grid2节点数据存储
points2 = vtkPoints()
points2.InsertNextPoint(0,2,0)
points2.InsertNextPoint(2,2,0)
points2.InsertNextPoint(0,4,0)
grid2.SetPoints(points2)

#grid2单元数据存储
tri = vtkTriangle()
tri.GetPointIds().SetId(0,0)
tri.GetPointIds().SetId(1,1)
tri.GetPointIds().SetId(2,2)
grid2.InsertNextCell(vtk.VTK_TRIANGLE, tri.GetPointIds())
'''

#为grid1网格添加节点解
pointScalars = vtkFloatArray()
for i in range(0,12):
    pointScalars.InsertNextValue((i+1)/100)
grid1.GetPointData().SetScalars(pointScalars)


pointScalars = vtkFloatArray()
for i in range(0,12):
    pointScalars.InsertNextValue((i+1)/10)
grid1.GetPointData().SetScalars(pointScalars)


#为grid1建立颜色映射表
# lut = vtkLookupTable()
# actor.GetProperty().SetRepresentationToSurface()
#             actor.GetProperty().SetPointSize(1)
#             actor.GetProperty().EdgeVisibilityOff()
#             # Mesh: Apply rainbow color map
#             actor_mesh_mapper = actor.GetMapper()
#             actor_lut = actor_mesh_mapper.GetLookupTable()
#             actor_lut.SetHueRange(0.666, 0.0)#色调范围
#             actor_lut.SetSaturationRange(1.0, 1.0)#颜色映射的饱和度范围
#             #actor_lut.SetValueRange(1.0, 1.0)
#             actor_lut.SetNumberOfColors(12)
#             actor_lut.Build()
# lut.SetTableValue(3,

#为grid1创建数据映射器
mesh_mapper1 = vtkDataSetMapper()
mesh_mapper1.SetInputData(grid1)
mesh_mapper1.ScalarVisibilityOn()
mesh_mapper1.SetScalarModeToDefault()
mesh_actor1 = vtkActor()

mesh_actor1.SetMapper(mesh_mapper1)


lut = mesh_mapper1.GetLookupTable()
lut.SetNumberOfTableValues(10)
lut.Build()
# lut.SetTableValue(0,0,0,0,1)
# lut.SetTableValue(1,0.89,0.81,0.34,1)
# lut.SetTableValue(2,1,0.3882,0.2784,1)

meshBarActor = vtkScalarBarActor()
meshBarActor.SetLookupTable(lut)
meshBarActor.SetTitle("test")

meshBarActor.SetDragable(True)
meshBarActor.SetPosition( 0.92, 0.05)
meshBarActor.SetPosition2( 0.07, 0.9 )
meshBarActor.SetNumberOfLabels(12)



#为grid2创建数据映射器，并将颜色映射表传递给数据映射器
# mesh_mapper2 = vtkDataSetMapper()
# mesh_mapper2.SetInputData(grid2)
# mesh_mapper2.SetScalarRange(0,2)
# mesh_mapper2.SetLookupTable(lut)
# mesh_actor2 = vtkActor()
# mesh_actor2.SetMapper(mesh_mapper2)

#创建渲染器和窗口
renderer = vtkRenderer()
renderer.SetBackground(0.0274, 0.2588, 0.6118)
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
#演员登场，后登场的演员会挡住先登场的演员
renderer.AddActor(mesh_actor1)
renderer.AddActor2D(meshBarActor)
# renderer.AddActor(mesh_actor2)
renderer.ResetCamera()

#创建交互器
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()        

#开始渲染和交互
renderWindow.Render()
renderWindowInteractor.Start()