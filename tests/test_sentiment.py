"""
Unit tests for sentiment breakdown, comment schema, and classification models.
"""

from models.analytics_models import CommentItem, SentimentBreakdown, SentimentEnum, TopicCluster, FeedbackReport

def test_comment_item_model():
    c = CommentItem(
        id="c_1",
        author="John Doe",
        text="This video is fantastic, loved the neural network explanation!",
        sentiment=SentimentEnum.POSITIVE,
        rationale="Praise for clarity",
        topic="Explanation Quality",
        is_actionable=False
    )
    assert c.sentiment == SentimentEnum.POSITIVE
    assert c.sentiment.value in ["Positive", "Negative", "Neutral"]

def test_sentiment_breakdown_percentages():
    sb = SentimentBreakdown(
        total_comments=10,
        classified_count=10,
        positive_count=7,
        negative_count=1,
        neutral_count=2,
        positive_pct=70.0,
        negative_pct=10.0,
        neutral_pct=20.0,
        failed_count=0
    )
    assert sb.positive_pct + sb.negative_pct + sb.neutral_pct == 100.0
    assert sb.total_comments == 10
