import json
import os
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkCommonCore import vtkPoints,vtkFloatArray
from vtkmodules.vtkCommonDataModel import(
    vtkDataObject, 
    vtkPlane, 
    vtkUnstructuredGrid,
    vtkHexahedron,
    
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

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkIOXML import vtkXMLDataSetWriter

class case2vtu():

    def __init__(self):
        self.output_path = "test.vtu"
        output_path = self.output_path
        work_path = "./work_dir/center"
        self.work_path = work_path
        self.dirs = os.listdir(work_path)
        self.ugrids = []
        self.__read_cases()
        print('Writing: ', self.output_path)
        writer = vtkXMLDataSetWriter()
        writer.SetFileName(self.output_path)
        writer.SetInputData(self.ugrids[0])
        writer.Write()
        
        


    def __read_cases(self): # 读取所有的求解文件夹
        dirs = self.dirs
        for dir in dirs: # 遍历所有文件
            case_path = os.path.join(self.work_path, dir)
            if os.path.isdir(case_path): # 如果是文件夹进入处理
                # case_dirs.append(case_path)
                self.ugrids.append(self.__read_case(case_path))

    def __read_case(self, filename):
        mesh_filename = filename + '/meshinfo.json'
        Data_filename = filename + '/Data'
        with open(mesh_filename,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
            nodes = json_data["instance"]["PART-1-1"]["Node"]
            elems = json_data["instance"]["PART-1-1"]["Elem"]

            points = vtkPoints()
            node_count = 0
            node_maps = {}
            for node in nodes: # 遍历顶点
                points.InsertPoint(node_count, node["Coord"])
                node_maps[str(node["ID"])] = node_count
                # node_maps.append(node_map)
                node_count = node_count+1

            ugrid = vtkUnstructuredGrid()
            for elem in elems: # 遍历元素
                if elem["Type"] == "C3D8":
                    hexahedron = vtkHexahedron()
                    for content_index in range(0,len(elem["Content"])):
                        content = elem["Content"][content_index]
                        # print (node_maps[str(content)])
                        
                        # hexahedron.GetPointIds().SetId(content_index, node_maps[str(content)])
                        hexahedron.GetPointIds().SetId(content_index, node_maps[str(content)])
                    ugrid.InsertNextCell( hexahedron.GetCellType(), hexahedron.GetPointIds())

            ugrid.SetPoints(points)

        Data_dirs = os.listdir(Data_filename)
        for Data_dir in Data_dirs: # 遍历Data文件夹
            data_sets = self.__read_cnt(os.path.join(Data_filename,Data_dir,"ResultData"))
            for data_set in data_sets:
                cellData = vtkFloatArray()
                cellData.SetNumberOfComponents(int(data_set[2]))
                # print(data_set[0])
                # print(data_set[1])
                # print(data_set[2])
                # print(data_set[3])
                # print(len(data_set[3:]))
                for data in data_set[3:]:
                    cellData.InsertNextValue(float(data))
                if Data_dir == "res_cnt":
                    ugrid.GetPointData().AddArray(cellData)
                if Data_dir == "res_nodal":
                    ugrid.GetCellData().AddArray(cellData)
                cellData.SetName(data_set[0])

            # elif Data_dir == "res_nodal":
                # self.__read_nodal(os.path.join(Data_filename,Data_dir,"ResultData"))
        return ugrid
        # for Data_dir in Data_dirs:
            # res_path 


    def __read_cnt(self,filename):
        case_dirs = os.listdir(filename)
        data_sets = []
        for case_dir in case_dirs:
            case_path = os.path.join(filename,case_dir,"dTwinsResult.txt")
            data_set = []
            with open(case_path, "r", encoding='utf-8') as f:  #打开文本
                for line in f:
                    data_set.append(line.strip())  #读取文本
                data_set.insert(0, case_dir)
            data_sets.append(data_set)
        return data_sets
    def __read_nodal(self,filename):
        return

    # def MakeUnstructuredGrid(aCell):
    #     pcoords = aCell.GetParametricCoords()
    #     for i in range(0, aCell.GetNumberOfPoints()):
    #         aCell.GetPointIds().SetId(i, i)
    #         aCell.GetPoints().SetPoint(i, (pcoords[3 * i]), (pcoords[3 * i + 1]), (pcoords[3 * i + 2]))

    #     ug = vtkUnstructuredGrid()
    #     ug.SetPoints(aCell.GetPoints())
    #     ug.InsertNextCell(aCell.GetCellType(), aCell.GetPointIds())
    #     return ug



if __name__ == '__main__':
    case2vtu()