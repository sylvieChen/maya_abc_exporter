import os
import maya.OpenMaya as om
import pymel.core as pm
from abc_add_custom_attribute.maya.attribute_writer import MeshWriter
from abc_add_custom_attribute.maya.util import get_children

DEFAULT_OUT_FILENAME = 'out'
FILE_EXTENSION = 'abc'


def get_filepath_name(file_dir=None, filename=DEFAULT_OUT_FILENAME):
    if not file_dir:
        file_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        file_dir = file_dir

    file_path_name = os.path.abspath(os.path.join(file_dir, filename))
    file_path_name = '{filename}.{ext}'.format(filename=file_path_name, ext=FILE_EXTENSION)
    return file_path_name


def main():
    #   Get selected objs
    selection_list = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection_list)

    #   Export mesh
    dag_path = om.MDagPath()
    selection_list.getDagPath(0, dag_path)
    all_dagpaths = get_children(dag_path=dag_path)
    for dagpath in all_dagpaths:
        obj_name = dagpath.partialPathName()
        out_file_dir = pm.workspace(q=True, fullName=True)
        filename = get_filepath_name(file_dir=out_file_dir, filename=obj_name)
        print filename

        mesh_writer = MeshWriter(dag_path=dag_path, filename=filename)
        mesh_writer.write_poly()
