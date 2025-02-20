import torch
import torch.nn as nn
import colossalai
import colossalai.nn as col_nn
from torch.fx import symbolic_trace
from colossalai.fx.passes.meta_info_prop import MetaInfoProp
from colossalai.fx.passes.adding_split_node_pass import split_with_split_nodes_pass, uniform_split_pass
from colossalai.fx.passes.utils import get_comm_size

MODEL_DIM = 16
BATCH_SIZE = 8
PIPELINE_SIZE = 2


class MLP(torch.nn.Module):

    def __init__(self, dim: int):
        super().__init__()
        self.linear1 = torch.nn.Linear(dim, dim)
        self.linear2 = torch.nn.Linear(dim, dim)
        self.linear3 = torch.nn.Linear(dim, dim)
        self.linear4 = torch.nn.Linear(dim, dim)

    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        x = self.linear3(x)
        x = self.linear4(x)
        return x


def test_comm_size_compute():
    model = MLP(MODEL_DIM)
    input_sample = torch.rand(BATCH_SIZE, MODEL_DIM)
    gm = symbolic_trace(model)
    MetaInfoProp(gm).run(input_sample)
    annotated_model = uniform_split_pass(gm, PIPELINE_SIZE)
    split_model, split_submodules = split_with_split_nodes_pass(annotated_model)
    submodule_list = list(split_model.children())
    comm_size = get_comm_size(submodule_list[0], submodule_list[1])
    # the shape of tensor send from partition 0 to partition 1 is (8, 16)
    assert comm_size == 128


if __name__ == '__main__':
    test_comm_size_compute()
