from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class AutoMeshOption(Enum):
    CUSTOM_MESH = 0
    AUTOMESH = 1


@dataclass
class Material(ABC):
    material_name: str
    auto_mesh: AutoMeshOption = AutoMeshOption.AUTOMESH
    mesh_size: float = 0.0

@dataclass
class Boundary(ABC):
    name: str
    type: int