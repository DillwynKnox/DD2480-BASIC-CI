
from dataclasses import dataclass
from typing import List


@dataclass
class Stage:
    stage: str
    command: str

@dataclass
class PipelineConfig:
    project: str
    stages: List[Stage]