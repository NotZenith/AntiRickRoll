"""Unit tests for the circular buffer."""

import numpy as np
import pytest
from audio.buffer.circular import CircularBuffer

def test_buffer_write_read():
    buffer = CircularBuffer(capacity=100, channels=1)
    data = np.random.rand(50, 1).astype(np.float32)

    written = buffer.write(data)
    assert written == 50
    assert buffer.size == 50

    read_data = buffer.read(50)
    assert np.array_equal(data, read_data)
    assert buffer.size == 0

def test_buffer_overflow():
    buffer = CircularBuffer(capacity=10, channels=1)
    data = np.random.rand(15, 1).astype(np.float32)

    written = buffer.write(data)
    assert written == 10
    assert buffer.overflow_count == 1
    assert buffer.dropped_frames == 5

def test_buffer_underflow():
    buffer = CircularBuffer(capacity=10, channels=1)
    read_data = buffer.read(5)
    assert read_data is None
    assert buffer.underflow_count == 1

def test_buffer_peek():
    buffer = CircularBuffer(capacity=10, channels=1)
    data = np.array([[0.1], [0.2], [0.3], [0.4]], dtype=np.float32)
    buffer.write(data)

    peeked = buffer.peek(2)
    assert np.array_equal(peeked, np.array([[0.3], [0.4]], dtype=np.float32))
    assert buffer.size == 4 # Peek doesn't remove
