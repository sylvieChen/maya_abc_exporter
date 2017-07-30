import maya.OpenMaya as om


def get_children(dag_path=None):
    if isinstance(dag_path, str) or isinstance(dag_path, unicode):
        selection_list = om.MSelectionList()
        selection_list.add(dag_path)
        dag_path = om.MDagPath()
        selection_list.getDagPath(0, dag_path)

    result = list()
    for i in range(dag_path.childCount()):
        child = dag_path.child(i)
        child_dag_path = dag_path.getAPathTo(child)
        result.extend(get_children(dag_path=child_dag_path))
        result.append(child_dag_path)

    return result