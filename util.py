
def setToIMathArray(type_traits, *in_list):
    """     Set to imath array.

    :Param iTPTraits: alembic abc type traits.
                      (can look at Alembic/Abc/TypedPropertyTraits.h)
                      Ex: Int32TPTraits, P3fTPTraits,...
    :Param iList:
    :Return: imath array object
    :Rtype: imath.V3fArray
    """
    array = type_traits.arrayType(len(in_list))
    for i in range(len(in_list)):
        array[i] = in_list[i]
    return array