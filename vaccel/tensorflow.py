from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError

import functools
import operator
import sys
from enum import IntEnum

class Node:
    """A representation of TensorFlow graph input or output node"""

    def __init__(self, name, node_id):
        self._name = bytes(name, "ascii")
        self._id = node_id

    def __str__(self):
        return '{}:{}'.format(self._name.decode('ascii'), self._id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, node_id):
        self._id = node_id

    def _to_ctype(self, ctype=None):
        if ctype == None:
            ctype = ffi.new("struct vaccel_tf_node *")
        ctype.name = ffi.new("char[]", self._name)
        ctype.id = self._id
        return ctype

    @staticmethod
    def _to_carray(nodes):
        cnodes = ffi.new("struct vaccel_tf_node[%d]" % len(nodes))
        for i, n in enumerate(nodes):
            n._to_ctype(cnodes[i])

        return cnodes

class TensorType(IntEnum):
    FLOAT = lib.VACCEL_TF_FLOAT
    DOUBLE = lib.VACCEL_TF_DOUBLE
    INT32 = lib.VACCEL_TF_INT32
    UINT8 = lib.VACCEL_TF_UINT8
    INT16 = lib.VACCEL_TF_INT16
    INT8 = lib.VACCEL_TF_INT8
    STRING = lib.VACCEL_TF_STRING
    COMPLEX = lib.VACCEL_TF_COMPLEX
    INT64 = lib.VACCEL_TF_INT64
    BOOL = lib.VACCEL_TF_BOOL
    QINT8 = lib.VACCEL_TF_QINT8
    QUINT8 = lib.VACCEL_TF_QUINT8
    QINT32 = lib.VACCEL_TF_QINT32
    BFLOAT16 = lib.VACCEL_TF_BFLOAT16
    QINT16 = lib.VACCEL_TF_QINT16
    QUINT16 = lib.VACCEL_TF_QUINT16
    UINT16 = lib.VACCEL_TF_UINT16
    COMPLEX128 = lib.VACCEL_TF_COMPLEX128
    HALF = lib.VACCEL_TF_HALF
    RESOURCE = lib.VACCEL_TF_RESOURCE
    VARIANT = lib.VACCEL_TF_VARIANT
    UINT32 = lib.VACCEL_TF_UINT32
    UINT64 = lib.VACCEL_TF_UINT64

class Tensor:
    """A representation of a Tensor"""

    _size_dict = dict([
            (TensorType.FLOAT, (ffi.sizeof('float'), 'float')),
            (TensorType.DOUBLE, (ffi.sizeof('double'), 'double')),
            (TensorType.INT32, (ffi.sizeof('int32_t'), 'int32_t')),
            (TensorType.UINT8, (ffi.sizeof('int8_t'), 'int8_t')),
            (TensorType.INT16, (ffi.sizeof('int16_t'), 'int16_t')),
            (TensorType.INT8, (ffi.sizeof('int8_t'), 'int8_t')),
            (TensorType.INT64, (ffi.sizeof('int64_t'), 'int64_t')),
            (TensorType.BOOL, (ffi.sizeof('bool'), 'bool')),
            (TensorType.UINT16, (ffi.sizeof('uint16_t'), 'uint16_t')),
            (TensorType.UINT32, (ffi.sizeof('uint32_t'), 'uint32_t')),
            (TensorType.UINT64, (ffi.sizeof('uint64_t'), 'uint64_t'))
    ])

    class OutOfBoundsTensorIndex(RuntimeError):
        def __init__(self, index, length):
            self._index = index
            self._length = length

        def __str__(self):
            return "Looking for index {} in a dimension of size {}".format(self._index, self._length)

    class UnmatchingDimensions(RuntimeError):
        def __init__(self, tensor_dims, data_len):
            self._dims = tensor_dims
            self._data_len = data_len

        def __str__(self):
            return "Trying to set data with length {} in tensor with dims: {}".format(self._data_len, self._dims)

    def __init__(self, dims, dtype:TensorType):
        self._dims = dims
        self._data = []
        self._dtype = dtype

    def __str__(self):
        return "Tensor {} of {}".format(self._dims, self._dtype)

    def _csize(self):
        return self._size_dict[self._dtype][0]

    def _ctype(self):
        return self._size_dict[self._dtype][1]

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, dims):
        self._dims = dims

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if self.len() != len(data):
            raise self.UnmatchingDimensions(self.dims, len(data))

        self._data = data

    def len(self):
        return functools.reduce(operator.mul, self.dims)

    def get_index(self, indices):
        index = 0
        dim_len = 1

        for i, dim in reversed(list(enumerate(self.dims))):
            if self.dims[i] < indices[i]:
                raise self.OutOfBoundsTensorIndex(indices[i], self.dims[i])

            index += indices[i] * dim_len
            dim_len = dim_len * self.dims[i]

        return index

    def get(self, indices):
        index = self.get_index(indices)
        return self.data[index]

    def _to_ctype(self, ctype=None):
        if ctype == None:
            ctype = ffi.new("struct vaccel_tf_tensor *")

        ctype.dims = ffi.new("int64_t[%d]" % len(self.dims), self.dims)
        ctype.nr_dims = len(self.dims)
        ctype.data = ffi.new("%s[%d]" % (self._ctype(), self._csize() * len(self.data)), self.data)
        ctype.size = self._csize() * len(self.data)
        ctype.data_type = int(self._dtype)

        return ctype

    @staticmethod
    def _to_carray(tensors):
        ctensors = ffi.new("struct vaccel_tf_tensor[%d]" % len(tensors))
        for i, t in enumerate(tensors):
            t._to_ctype(ctensors[i])

        return ctensors

    @staticmethod
    def _from_ctype(ctensor):
        dims = ffi.unpack(ctensor.dims, ctensor.nr_dims)
        dtype = TensorType(ctensor.data_type)

        tensor = Tensor(dims, dtype)
        typed_cdata = ffi.cast("%s *" % tensor._ctype(), ctensor.data)
        tensor.data = ffi.unpack(typed_cdata, int(ctensor.size / tensor._csize()))

        return tensor
        
    @staticmethod
    def _from_carray(ctensors, nr_tensors):
        ctensors = ffi.unpack(ctensors, nr_tensors)
        return [Tensor._from_ctype(t) for t in ctensors]
        

class TensorFlowModel:
    """A TensorFlow model vAccel resource"""

    def __init__(self):
        """Create a TensorFlow model resource"""
        self._inner = ffi.new("struct vaccel_tf_model *")

    def __del__(self):
        """Destroy a vAccel TensorFlow model"""
        
        lib.vaccel_tf_model_destroy(self._inner)

    def _get_inner_resource(self):
        return self._inner.resource

    def from_model_file(self, model_path:str):
        """Initialize a TensorFlow model by loading it from a .pb file"""

        ret = lib.vaccel_tf_model_new(self._inner, bytes(model_path, 'ascii'))
        if ret != 0:
            raise VaccelError(ret, "Could not create model")

    def from_data(self, data:bytes):
        """Initialize a TensorFlow model from a byte array"""

        ret = lib.vaccel_tf_model_new_from_buffer(self._inner, data)
        if ret != 0:
            raise VaccelError(ret, "Could not create model")

    def id(self):
        """Id of the TensorFlow model"""
        return lib.vaccel_tf_model_get_id(self._inner)

    def is_registered(self, session):
        """Returns True if the model is registered with session"""
        return session.has_resource(self)

    def load_graph(self, session):
        status = ffi.new("struct vaccel_tf_status *")
        ret = lib.vaccel_tf_model_load_graph(session._to_inner(), self._inner,
                status)
        if ret != 0:
            raise VaccelError(ret, "Could not load TensorFlow graph")

    def run(self, session, in_nodes, in_tensors, out_nodes):
        _run_options = ffi.new("struct vaccel_tf_buffer *");
        _status = ffi.new("struct vaccel_tf_status *");
        _out_tensors = ffi.new("struct vaccel_tf_tensor[%d]" % len(out_nodes))

        _in_nodes = Node._to_carray(in_nodes)
        _in_tensors = Tensor._to_carray(in_tensors)
        _out_nodes = Node._to_carray(out_nodes)

        ret = lib.vaccel_tf_model_run(session._to_inner(), self._inner, _run_options,
                _in_nodes, _in_tensors, len(in_nodes),
                _out_nodes, _out_tensors, len(out_nodes),
                _status)
        if ret != 0:
            print(ffi.string(_status.message))
            raise VaccelError(ret, "Could not run TensorFlow graph")

        return Tensor._from_carray(_out_tensors, len(out_nodes))


