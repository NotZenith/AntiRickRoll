"""Unit tests for the audio processing pipeline."""

import numpy as np
import pytest
from audio.processing.pipeline import AudioPipeline
from audio.processing.stages import ChannelConverter, Normalizer

def test_pipeline_processing():
    pipeline = AudioPipeline()
    pipeline.add_stage(ChannelConverter(target_channels=1))
    pipeline.add_stage(Normalizer(target_peak=1.0))

    # 2 channels, peak at 0.5
    data = np.array([[0.5, 0.5], [-0.5, -0.5]], dtype=np.float32)

    processed = pipeline.process(data)

    assert processed.shape == (2, 1)
    assert np.max(np.abs(processed)) == 1.0 # Normalized

def test_channel_converter():
    conv = ChannelConverter(target_channels=1)
    data = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    mono = conv.process(data)
    assert mono.shape == (2, 1)
    assert np.allclose(mono, np.array([[0.5], [0.5]], dtype=np.float32))
