from enum import Enum


class DataType(Enum):
    """gradiently Supported DataTypes"""

    INT32 = 0
    INT64 = 1
    FLOAT64 = 2
    FLOAT32 = 3
    STRING = 4


Int32 = DataType.INT32
Int64 = DataType.INT64
Float32 = DataType.FLOAT32
Float64 = DataType.FLOAT64
String = DataType.STRING
