from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError

import functools
import operator
from enum import IntEnum


class Node:
    """A representation of TensorFlow graph input or output node"""

    def __init__(self, name, node_id):
        self._name = bytes(name, "ascii")
        self._id = node_id
        self.__hidden__ = list()

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

    def to_cffi(self):
        name = ffi.new("char[]", self._name)
        nid = self._id

        ctype = ffi.new("struct vaccel_tf_node []", 1)
        self.__hidden__.append(ctype)
        self.__hidden__.append(name)
        ctype[0].name = name
        ctype[0].id = nid

        return ctype[0]

    def _to_carray(self, nodes):
        temp = []
        for i, n in enumerate(nodes):
            temp.append(n.to_cffi())

        ctypenew = ffi.new("struct vaccel_tf_node[]", temp)
        # hack to keep memory alive
        self.__hidden__.append(ctypenew)

        return ctypenew


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

    def __init__(self, dims, dtype: TensorType):
        self._dims = dims
        self._data = []
        self._dtype = dtype
        self.__hidden__ = []

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

    def to_cffi(self):
        dims = ffi.new("int64_t[%d]" % len(self.dims), self.dims)
        # hack to keep memory alive
        self.__hidden__.append(dims)

        nr_dims = len(self.dims)

        data = ffi.new("%s[%d]" % (self._ctype(), len(self.data)), self.data)
        # hack to keep memory alive
        self.__hidden__.append(data)

        size = self._csize() * len(self.data)
        data_type = int(self._dtype)

        ctype = ffi.new("struct vaccel_tf_tensor []", 1)
        # hack to keep memory alive
        self.__hidden__.append(ctype)

        ctype[0].dims = dims
        ctype[0].nr_dims = nr_dims
        ctype[0].data = data
        ctype[0].size = size
        ctype[0].data_type = data_type

        return ctype[0]

    def _to_carray(self, tensors):

        ctensors = ffi.new("struct vaccel_tf_tensor[%d]" % len(tensors))
        self.__hidden__.append(ctensors)

        temp = []
        for i, t in enumerate(tensors):
            temp.append(t.to_cffi())
#           __hidden__.append(ctensors[i])

#       ctypenew = ffi.new("struct vaccel_tf_tensor**", ctensors)
        ctypenew = ffi.new("struct vaccel_tf_tensor[]", temp)
        self.__hidden__.append(ctypenew)
        ctypenew = ffi.new("struct vaccel_tf_tensor**", ctypenew)
        self.__hidden__.append(ctypenew)
#       return ctensors
        return ctypenew

    @staticmethod
    def _from_ctype(ctensor):
        dims = ffi.unpack(ctensor.dims, ctensor.nr_dims)
#       dims = [ctensor.dims[i] for i in range(ctensor.nr_dims)]
        dtype = TensorType(ctensor.data_type)

        tensor = Tensor(dims, dtype)
        typed_cdata = ffi.cast("%s *" % tensor._ctype(), ctensor.data)
        tensor.data = ffi.unpack(typed_cdata, int(
            ctensor.size / tensor._csize()))

        return tensor

    @staticmethod
    def _from_carray(ctensors, nr_tensors):
        ctensors = ffi.unpack(ctensors, nr_tensors)
        return [Tensor._from_ctype(t) for t in ctensors]


class TensorFlowModel:
    def load(session, resource):
        status = ffi.new("struct vaccel_tf_status *")

        ret = lib.vaccel_tf_session_load(
            session._to_inner(), resource._inner, status)
        if ret != 0:
            raise VaccelError(ret, "Could not load tf session")

    def run(session, resource, in_nodes, in_tensors, out_nodes):
        _run_options = ffi.new("struct vaccel_tf_buffer *")
        _status = ffi.new("struct vaccel_tf_status *")
        _out_tensors_ = ffi.new("struct vaccel_tf_tensor[%d]" % len(out_nodes))
        _out_tensors = ffi.new("struct vaccel_tf_tensor**", _out_tensors_)

        _in_nodes = in_nodes[0]._to_carray(in_nodes)
        _in_tensors = in_tensors[0]._to_carray(in_tensors)
        _out_nodes = out_nodes[0]._to_carray(out_nodes)

        ret = lib.vaccel_tf_session_run(session._to_inner(), resource._inner, _run_options,
                                        _in_nodes, _in_tensors, len(in_nodes),
                                        _out_nodes, _out_tensors, len(
                                            out_nodes),
                                        _status)
        if ret != 0:
            print(ffi.string(_status.message))
            raise VaccelError(ret, "Could not run TensorFlow graph")

        return Tensor._from_carray(_out_tensors, len(out_nodes))
