
import torch.distributed as dist
def get_world_size() -> int:
    if not dist.is_available():
        return 1
    if not dist.is_initialized():
        return 1
    return dist.get_world_size()


import torch
TORCH_VERSION = tuple(int(x) for x in torch.__version__.split(".")[:2])