from imath import *
import math
import pymel.core as pm
import alembic
from alembic.Abc import *
from alembic.AbcGeom import *

from abc_add_custom_attribute.util import setToIMathArray
from abc_add_custom_attribute.maya.mesh_data import MeshData
from abc_add_custom_attribute.archive_info import ArchiveInfo


class MeshWriter(object):
    def __init__(self, dag_path=None, filename=None):
        super(MeshWriter, self).__init__()
        self.dag_path = dag_path
        self.filename = filename
        self.archive_info = ArchiveInfo()

    def write_poly(self):
        #   Create archive
        oarch = alembic.Abc.OArchive(self.filename)
        top = oarch.getTop()
        obj_name = self.dag_path.partialPathName()
        tsidx = top.getArchive().addTimeSampling(self.archive_info.ts)

        #   Create top xform
        xform = OXform(top, str(obj_name), tsidx)

        #   Create mesh
        meshObj = OPolyMesh(xform, '{}Shape'.format(obj_name), tsidx)
        mesh_schema = meshObj.getSchema()

        #   Add custom property
        arb_geom_param = meshObj.getSchema().getArbGeomParams()
        geometry_scope = GeometryScope.kVertexScope
        custom_param = self.add_attribute(parent=arb_geom_param, geometry_scope=geometry_scope)

        #   Set sample
        frame_range = self.archive_info.end_frame - self.archive_info.start_frame + 1
        for i in range(frame_range):
            currentFrame = self.archive_info.start_frame + i
            pm.currentTime(currentFrame)

            # Get current mesh data
            mesh_data = MeshData(self.dag_path)

            points = mesh_data.get_points()
            imath_point_array = setToIMathArray(P3fTPTraits, *points)

            vids, fcounts = mesh_data.get_vertices()
            imath_face_indices = setToIMathArray(Int32TPTraits, *list(vids))
            imath_face_counts = setToIMathArray(Int32TPTraits, *list(fcounts))

            bbox_max_point, bbox_min_point = mesh_data.get_bbox_end_points()
            imath_bbox = Box3d(V3d(bbox_min_point.x, bbox_min_point.y, bbox_min_point.z), V3d(bbox_max_point.x, bbox_max_point.y, bbox_max_point.z))

            trans_info = mesh_data.get_trasform_info()

            # Set xform sample
            xsamp = XformSample()
            xsamp.setTranslation(V3d(*trans_info[0]))
            xsamp.setRotation(V3d(*trans_info[1][0]), math.degrees(trans_info[1][1]))
            xsamp.setScale(V3d(*trans_info[2]))
            xform.getSchema().set(xsamp)

            # Set mesh sample
            mesh_samp = OPolyMeshSchemaSample(imath_point_array, imath_face_indices, imath_face_counts)
            mesh_samp.setSelfBounds(imath_bbox)
            mesh_schema.set(mesh_samp)

            # Set custom attribute
            if currentFrame == self.archive_info.start_frame:
                # array = P3fTPTraits.arrayType(len(imath_point_array))
                # for j in range(len(imath_point_array)):
                #     array[j] = list(imath_point_array)[j]
                samp = OP3fGeomParamSample(imath_point_array, geometry_scope)
                samp.setVals(imath_point_array)
                custom_param.set(samp)
                custom_param.setTimeSampling(self.archive_info.ts)

    def add_attribute(self, prop_name="custom", parent=None, geometry_scope=GeometryScope.kVertexScope):
        if not parent:
            return
        #   Add custom property
        custom_param = OP3fGeomParam(parent, prop_name, False, geometry_scope, 1)
        return custom_param