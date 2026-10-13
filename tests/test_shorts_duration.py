"""
Unit tests for YouTube Shorts candidate duration limits (strictly <= 60 seconds).
"""

from services.shorts_service import shorts_service
from models.schemas import SubtitleSegment

def test_shorts_selection_under_60_seconds():
    # Synthetic lecture segments spanning 120 seconds
    segments = [
        SubtitleSegment(id=1, start=0.0, end=15.0, text="Welcome to this lecture on generative neural architectures."),
        SubtitleSegment(id=2, start=15.0, end=35.0, text="The transformer model computes self-attention across tokens."),
        SubtitleSegment(id=3, start=35.0, end=60.0, text="This formula allows parallel training across thousands of GPUs."),
        SubtitleSegment(id=4, start=60.0, end=85.0, text="Now let us look at how diffusion generates imagery from noise."),
        SubtitleSegment(id=5, start=85.0, end=115.0, text="In summary, foundational models power the modern AI revolution.")
    ]

    candidates = shorts_service.rank_and_select_candidates(
        segments=segments,
        total_video_duration=120.0,
        target_count=3
    )

    assert len(candidates) > 0
    for cand in candidates:
        assert cand.duration_sec <= 60.0, f"Candidate {cand.id} exceeded 60s limit: {cand.duration_sec}s"
        assert cand.duration_sec > 0.0
        assert cand.verified_under_60s is True
