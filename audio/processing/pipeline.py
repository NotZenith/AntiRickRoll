"""Modular audio processing pipeline."""

import numpy as np
from typing import List
from audio.processing.stages import ProcessingStage

class AudioPipeline:
    """Orchestrates multiple processing stages."""

    def __init__(self):
        self.stages: List[ProcessingStage] = []

    def add_stage(self, stage: ProcessingStage) -> None:
        """Adds a stage to the end of the pipeline."""
        self.stages.append(stage)

    def process(self, data: np.ndarray) -> np.ndarray:
        """Processes data through all stages sequentially."""
        processed_data = data
        for stage in self.stages:
            processed_data = stage.process(processed_data)
        return processed_data

    def clear(self) -> None:
        """Clears all stages."""
        self.stages = []
