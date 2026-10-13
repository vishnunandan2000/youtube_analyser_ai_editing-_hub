"""
Pydantic models for YouTube Intelligence, Analytics KPIs, Sentiment, and Recommendations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class SentimentEnum(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"

class CommentItem(BaseModel):
    id: str
    author: str = "Anonymous"
    text: str
    published_at: str = ""
    like_count: int = 0
    sentiment: Optional[SentimentEnum] = None
    rationale: Optional[str] = None
    topic: Optional[str] = None
    is_actionable: bool = False
    confidence: float = 1.0

class SentimentBreakdown(BaseModel):
    total_comments: int = 0
    classified_count: int = 0
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    positive_pct: float = 0.0
    negative_pct: float = 0.0
    neutral_pct: float = 0.0
    failed_count: int = 0

class VideoMetadata(BaseModel):
    video_id: str
    title: str = "Unknown Video"
    channel_name: str = "Unknown Channel"
    channel_id: str = ""
    thumbnail_url: str = ""
    description: str = ""
    duration_seconds: float = 0.0
    published_at: str = ""
    tags: List[str] = Field(default_factory=list)

class AnalyticsKPIs(BaseModel):
    # Public Metrics
    views: Optional[int] = None
    likes: Optional[int] = None
    comments_count: Optional[int] = None
    
    # Calculated Metrics
    like_to_view_ratio: Optional[float] = None      # (likes / views) * 100
    comment_to_view_ratio: Optional[float] = None   # (comments / views) * 100
    public_engagement_rate: Optional[float] = None  # ((likes + comments) / views) * 100
    
    # Authenticated Metrics (Marked unavailable unless OAuth granted)
    shares: Optional[int] = None
    subscribers_gained: Optional[int] = None
    watch_time_hours: Optional[float] = None
    average_view_duration_sec: Optional[float] = None
    average_percentage_viewed: Optional[float] = None
    
    # Retrieval metadata
    data_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_authenticated: bool = False
    notes: Dict[str, str] = Field(default_factory=dict)

class TopicCluster(BaseModel):
    topic: str
    count: int
    sentiment_distribution: Dict[str, int] = Field(default_factory=dict)
    representative_comments: List[str] = Field(default_factory=list)

class FeedbackReport(BaseModel):
    topics: List[TopicCluster] = Field(default_factory=list)
    key_clarifications: List[str] = Field(default_factory=list)
    positive_highlights: List[str] = Field(default_factory=list)
    critical_concerns: List[str] = Field(default_factory=list)
    actionable_suggestions: List[str] = Field(default_factory=list)

class RecommendationPriority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class VideoImprovementItem(BaseModel):
    category: str  # e.g., "Hook", "Thumbnail", "Pacing", "Explanation", "Engagement"
    priority: RecommendationPriority = RecommendationPriority.MEDIUM
    observed_problem: str
    supporting_evidence: str
    proposed_improvement: str
    expected_benefit: str
    implementation_steps: List[str] = Field(default_factory=list)

class VideoImprovementReport(BaseModel):
    video_id: str
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    recommendations: List[VideoImprovementItem] = Field(default_factory=list)
    suggested_titles: List[str] = Field(default_factory=list)
    thumbnail_concepts: List[str] = Field(default_factory=list)
    opening_hooks: List[str] = Field(default_factory=list)
    chapter_plan: List[Dict[str, Any]] = Field(default_factory=list)
