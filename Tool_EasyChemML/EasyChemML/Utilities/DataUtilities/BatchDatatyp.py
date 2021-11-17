from enum import Enum
from typing import Tuple, List, Dict

import numpy as np, h5py


class BatchDatatypClass(Enum):
    NUMPY_STRING = 'STRING'
    PYTHON_OBJECT = 'OBJECT'
    NUMPY_INT8 = 'INT8'
    NUMPY_INT16 = 'INT16'
    NUMPY_INT32 = 'INT32'
    NUMPY_INT64 = 'INT64'
    NUMPY_FLOAT16 = 'FLOAT16'
    NUMPY_FLOAT32 = 'FLOAT32'
    NUMPY_FLOAT64 = 'FLOAT64'
    NUMPY_COMPLEX64 = 'COMPLEX64'
    NUMPY_COMPLEX128 = 'COMPLEX128'


class BatchDatatyp:
    _DatatypClass: BatchDatatypClass
    _shape: tuple

    def __init__(self, typclass: BatchDatatypClass, shape: Tuple = None):
        self._DatatypClass = typclass
        self._shape = shape

        if not isinstance(shape,tuple) and not shape is None:
            raise Exception('shape is not a tuple')

        if shape is None:
            self._shape = ()

    def __repr__(self):
        return f'(class: {self._DatatypClass} | shape: {self._shape})'

    def __eq__(self, other):
        if isinstance(other, BatchDatatyp):
            if other.get_DatatypClass() == self._DatatypClass:
                return True
            else:
                return False
        elif isinstance(other, BatchDatatypClass):
            if other == self._DatatypClass:
                return True
            return False
        else:
            return False
        return False

    def get_DatatypClass(self):
        return self._DatatypClass

    def get_shape(self):
        return self._shape

    def set_shape(self, shape: Tuple):
        self._shape = shape

    def toNUMPY(self, string_as_obj = True):
        out_string = ''

        if self._shape is None or len(self._shape) < 1 or self._shape[0] == 1:
            out_string = ''
        else:
            out_string = str(self._shape)

        if self._DatatypClass == BatchDatatypClass.NUMPY_STRING:
            if not (self._shape is None or len(self._shape) == 0 or self._shape[0] > 0):
                raise Exception('String column cannot be an Array')
            if string_as_obj:
                out_string = out_string + 'O'
            else:
                out_string = out_string + 'U'
        elif self._DatatypClass == BatchDatatypClass.PYTHON_OBJECT:
            if not (self._shape is None or len(self._shape) == 0 or self._shape[0] > 0):
                raise Exception('Object column cannot be an Array')
            out_string = out_string + 'O'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT8:
            out_string = out_string + 'int8'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT16:
            out_string = out_string + 'int16'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT32:
            out_string = out_string + 'int32'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT64:
            out_string = out_string + 'int64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT16:
            out_string = out_string + 'float16'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT32:
            out_string = out_string + 'float32'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT64:
            out_string = out_string + 'float64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_COMPLEX64:
            out_string = out_string + 'complex64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_COMPLEX128:
            out_string = out_string + 'complex128'
        return out_string

    def toH5(self):
        out_string = ''

        if self._shape is None or len(self._shape) == 0:
            out_string = ''
        else:
            out_string = str(self._shape)

        if self._DatatypClass == BatchDatatypClass.NUMPY_STRING:
            if not (self._shape is None or len(self._shape) == 0 or self._shape[0] == 1):
                raise Exception('String column cannot be an Array')
            return h5py.string_dtype(encoding='utf-8')
        elif self._DatatypClass == BatchDatatypClass.PYTHON_OBJECT:
            if not (self._shape is None or len(self._shape) == 0 or self._shape[0] == 1):
                raise Exception('Object column cannot be an Array')
            return h5py.string_dtype(encoding='utf-8')
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT8:
            out_string = out_string + 'int8'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT16:
            out_string = out_string + 'int16'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT32:
            out_string = out_string + 'int32'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_INT64:
            out_string = out_string + 'int64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT16:
            out_string = out_string + 'float16'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT32:
            out_string = out_string + 'float32'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_FLOAT64:
            out_string = out_string + 'float64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_COMPLEX64:
            out_string = out_string + 'complex64'
        elif self._DatatypClass == BatchDatatypClass.NUMPY_COMPLEX128:
            out_string = out_string + 'complex128'

        return out_string

    @staticmethod
    def Fabricator_BY_str(typAsString: str, shape: tuple = None):
        typAsString = typAsString.lower().strip()

        if 'u' in typAsString or typAsString == 'str':
            if not (shape is None or len(shape) == 0):
                raise Exception('String column cannot be an Array')
            return BatchDatatyp(BatchDatatypClass.NUMPY_STRING, shape)
        elif typAsString == 'o' or typAsString == 'object':
            if not (shape is None or len(shape) == 0):
                raise Exception('Object column cannot be an Array')
            return BatchDatatyp(BatchDatatypClass.PYTHON_OBJECT, shape)
        elif typAsString == 'int8':
            return BatchDatatyp(BatchDatatypClass.NUMPY_INT8, shape)
        elif typAsString == 'int16':
            return BatchDatatyp(BatchDatatypClass.NUMPY_INT16, shape)
        elif typAsString == 'int32' or typAsString == 'int' or typAsString == 'integer':
            return BatchDatatyp(BatchDatatypClass.NUMPY_INT32, shape)
        elif typAsString == 'int64':
            return BatchDatatyp(BatchDatatypClass.NUMPY_INT64, shape)
        elif typAsString == 'float16':
            return BatchDatatyp(BatchDatatypClass.NUMPY_FLOAT16, shape)
        elif typAsString == 'float32' or typAsString == 'float' or typAsString == 'flt':
            return BatchDatatyp(BatchDatatypClass.NUMPY_FLOAT32, shape)
        elif typAsString == 'float64':
            return BatchDatatyp(BatchDatatypClass.NUMPY_FLOAT64, shape)
        elif typAsString == 'complex' or typAsString == 'complex64':
            return BatchDatatyp(BatchDatatypClass.NUMPY_COMPLEX64, shape)
        elif typAsString == 'complex128':
            return BatchDatatyp(BatchDatatypClass.NUMPY_COMPLEX128, shape)
        else:
            raise Exception(f'cannot detect the Basedatatyp of {typAsString}')

    @staticmethod
    def Fabricator_BY_Classes(typAsClass: BatchDatatypClass):
        return BatchDatatyp(typAsClass)
