import sys
import os
from alembic.Abc import *
from alembic.AbcGeom import *
import alembic

"""
#   how to execute:
    
    python D:\abc_echo.py "C:\pCubeShape1.abc" 
    
    #   Result  #
    AbcEcho for C:\Users\yan\Desktop\rfm_project\pCubeShape1.abc                                                         Alembic Info:                                                                                                                                                                                                      _ai_AlembicVersion=Alembic 1.5.4 (built May  8 2014 14:31:50)
    <Object> pCube1Shape                                                                                                 
    schema=AbcGeom_Xform_v3;schemaObjTitle=AbcGeom_Xform_v3:.xform                                                       
    schema=AbcGeom_PolyMesh_v1;schemaBaseType=AbcGeom_GeomBase_v1;schemaObjTitle=AbcGeom_PolyMesh_v1:.geom               
    <CompoundProperty>, .geom, AbcGeom_PolyMesh_v1                                                                       
    <CompoundProperty>, .arbGeomParams,                                                                                  
    <ArrayProperty>, custom,                                                                                             
        sample 0: V3fArray(8)                                                                                                
    <ArrayProperty>, .faceCounts,
        sample 0: 
        IntArray(6)   
    <ArrayProperty>, .faceIndices,
        sample 0: IntArray(24)
    <ArrayProperty>, P, 
        sample 0: V3fArray(8)
        scalar .selfBnds        
"""

def visitProperties(parent_property, display_value=False):
    for header in parent_property.propertyheaders:
        if header.isCompound():
            compound_prop = ICompoundProperty(parent_property, header.getName())
            visit_compound_property(compound_prop)
        if header.isScalar():
            print '\tscalar {}'.format(header.getName())
        if header.isArray():
            prop = IArrayProperty(parent_property, header.getName())
            visit_array_property(prop)


def visit_array_property(parent_property, display_value=False):
    prop_type = 'ArrayProperty'
    prop_name = parent_property.getName()
    schema = parent_property.getMetaData().get("schema")
    print '<{0}>, {1}, {2}'.format(prop_type, prop_name, schema)
    for j, s in enumerate(parent_property.samples):
        print '\tsample {0}: {1}({2})'.format(j, type(s).__name__, len(s))

    value = parent_property.getValue(ISampleSelector(0))
    if value and display_value:
        print '\tname:{0}, {1}, value:{2}'.format(
            parent_property.getName(), parent_property.getMetaData().serialize(), list(value))


def visit_compound_property(parent_property, display_value=False):
    prop_type = 'CompoundProperty'
    prop_name = parent_property.getName()
    schema = parent_property.getMetaData().get("schema")
    print '<{0}>, {1}, {2}'.format(prop_type, prop_name, schema)
    visitProperties(parent_property)


def get_mesh_objects(iarch):
    if not iarch:
        return

    mesh_objs = list()
    for i in range(iarch.getTop().getNumChildren()):
        transform_obj = IObject(iarch.getTop(), iarch.getTop().getChildHeader(i).getName())
        for j in range(transform_obj.getNumChildren()):
            mesh_obj = IObject(transform_obj, transform_obj.getChildHeader(i).getName())
            print '<Object> {}'.format(mesh_obj.getName())
            print transform_obj.getMetaData().serialize()
            print mesh_obj.getMetaData().serialize()
            mesh_objs.append(mesh_obj)
            return mesh_objs

def visit_archieve(abc_file):
    if not abc_file:
        return

    if not os.path.exists(abc_file):
        print 'File not exists.'
        return

    #   Read archive
    iarch = alembic.Abc.IArchive(abc_file)

    #   Print alembic info
    metadata = iarch.getTop().getMetaData()
    print 'Alembic Info:\n{0}\n'.format(metadata)

    #   visit object
    mesh_objs = get_mesh_objects(iarch)

    #   visit properties
    for mesh_obj in mesh_objs:
        parent_property = mesh_obj.getProperties()
        visitProperties(parent_property)

if __name__ == '__main__':
    abc_file = sys.argv[1]
    if abc_file:
        print 'AbcEcho for {}\n'.format(abc_file)
        visit_archieve(abc_file)
    else:
        print 'No abc file.'


