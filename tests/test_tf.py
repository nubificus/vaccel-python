from vaccel.session import Session
from vaccel.tensorflow import Tensor, TensorType, Node, TensorFlowModel
from vaccel.resource import Resource


def test_tf():
    session = Session(flags=0)

    model_path = "/usr/local/share/vaccel/models/tf/lstm2"
    a = Resource(session, model_path, rtype=2)

    TensorFlowModel.load(session, a)
    
    nname = "serving_default_input_1"
    nid = 0
    n1 = Node(nname, nid)
    in_nodes = [n1]

    nname = "StatefulPartitionedCall"
    nid = 0
    n2 = Node(nname, nid)
    out_nodes = [n2]

    t = Tensor([1, 30], TensorType.FLOAT)
    t.data = [1.0] * 30
    t.dims = [1, 30]

    in_tensors = [t]  # int64_t dims[] = {1, 30};

    out = TensorFlowModel.run(session, a, in_nodes, in_tensors, out_nodes)
    for t in out:
        print(t.__str__())

        offset = t.data
        print(offset)

    # a.unregister_resource()
