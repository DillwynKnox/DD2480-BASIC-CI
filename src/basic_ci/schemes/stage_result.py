from dataclasses import dataclass


@dataclass
class Stage_result:
    name: str
    success: bool
    command: str
    output: str