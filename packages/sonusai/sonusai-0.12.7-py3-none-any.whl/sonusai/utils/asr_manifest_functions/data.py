from dataclasses import dataclass
from typing import Dict

TranscriptData = Dict[str, str]


@dataclass(frozen=True)
class PathInfo:
    abs_path: str
    audio_filepath: str
