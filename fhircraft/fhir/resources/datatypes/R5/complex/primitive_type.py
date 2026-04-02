from fhircraft.fhir.resources.datatypes.R5.complex.data_type import DataType


class PrimitiveType(DataType):
    """
    Parent type for DataTypes with a simple value
    """

    _type = "PrimitiveType"
