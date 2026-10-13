"""
Unit tests for caption formatting and timestamp conversions.
"""

from utils.timestamp_utils import seconds_to_srt_time, seconds_to_vtt_time, seconds_to_human_time, srt_time_to_seconds

def test_seconds_to_srt_time():
    assert seconds_to_srt_time(0.0) == "00:00:00,000"
    assert seconds_to_srt_time(65.5) == "00:01:05,500"
    assert seconds_to_srt_time(3661.123) == "01:01:01,123"

def test_seconds_to_vtt_time():
    assert seconds_to_vtt_time(0.0) == "00:00:00.000"
    assert seconds_to_vtt_time(65.5) == "00:01:05.500"

def test_seconds_to_human_time():
    assert seconds_to_human_time(45.0) == "00:45"
    assert seconds_to_human_time(302.0) == "05:02"
    assert seconds_to_human_time(3605.0) == "01:00:05"

def test_srt_time_to_seconds():
    assert srt_time_to_seconds("00:01:05,500") == 65.5
    assert srt_time_to_seconds("00:01:05.500") == 65.5
