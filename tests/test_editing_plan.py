"""
Unit tests for Edit Decision List (EDL) models and allowable operations.
"""

from models.editing_models import EditDecisionList, EditOperation, EditOperationType

def test_edl_schema_validation():
    edl = EditDecisionList(
        job_id="job_test_123",
        source_media_path="video.mp4",
        source_duration_sec=120.0,
        target_duration_sec=115.0,
        operations=[
            EditOperation(
                op_type=EditOperationType.KEEP,
                start_sec=0.0,
                end_sec=50.0,
                reason="Introduction"
            ),
            EditOperation(
                op_type=EditOperationType.CUT_PAUSE,
                start_sec=50.0,
                end_sec=55.0,
                reason="Long silence pause"
            ),
            EditOperation(
                op_type=EditOperationType.KEEP,
                start_sec=55.0,
                end_sec=120.0,
                reason="Core explanation"
            ),
            EditOperation(
                op_type=EditOperationType.OVERLAY_ENGAGEMENT,
                start_sec=15.0,
                end_sec=21.0,
                reason="Animated subscribe card"
            )
        ]
    )

    assert edl.job_id == "job_test_123"
    assert len(edl.operations) == 4
    # Ensure allowlisted operation types
    for op in edl.operations:
        assert isinstance(op.op_type, EditOperationType)
        assert op.end_sec >= op.start_sec
