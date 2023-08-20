import importlib.metadata

from .train.trainer import Trainer
from .evaluate import infer
from .case_setup.case import case_builder
from .models import GNS, EGNN, SEGNN, PaiNN
from .data import DAM2D, LDC2D, LDC3D, RPF2D, RPF3D, TGV2D, TGV3D, H5Dataset
from .utils import PushforwardConfig

__all__ = [
    "Trainer",
    "infer",
    "case_builder",
    "GNS",
    "EGNN",
    "SEGNN",
    "PaiNN",
    "H5Dataset",
    "TGV2D",
    "TGV3D",
    "RPF2D",
    "RPF3D",
    "LDC2D",
    "LDC3D",
    "DAM2D",
    "PushforwardConfig",
]

__version__ = importlib.metadata.version("lagrangebench_test")