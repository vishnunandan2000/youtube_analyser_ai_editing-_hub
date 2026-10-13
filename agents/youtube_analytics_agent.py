"""
YouTube Analytics Agent.
Orchestrates video metadata extraction, KPI calculation, comment harvesting,
and generates rich Plotly charts.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.youtube_service import youtube_service
from services.oauth_service import oauth_service
from agents.sentiment_agent import sentiment_agent
from models.analytics_models import VideoMetadata, AnalyticsKPIs, CommentItem, SentimentBreakdown, FeedbackReport
from utils.logging_config import logger

class YouTubeAnalyticsAgent:
    def __init__(self):
        pass

    def run_analysis(self, url: str, max_comments: int = 50, enable_authorized_analytics: bool = False) -> Dict[str, Any]:
        """
        Execute complete Division A YouTube Intelligence workflow.
        """
        metadata, kpis = youtube_service.get_video_details(url)
        if enable_authorized_analytics:
            kpis = youtube_service.get_authorized_analytics(kpis, metadata.duration_seconds)
            
        comments = youtube_service.fetch_comments(url, max_comments=max_comments)
        
        classified_comments, sentiment_summary, feedback_report = sentiment_agent.analyze_comments(comments)

        # Generate Plotly Visualizations
        pie_fig = self.create_sentiment_pie(sentiment_summary)
        bar_fig = self.create_sentiment_bar(sentiment_summary)
        engagement_fig = self.create_engagement_chart(kpis)

        return {
            "metadata": metadata,
            "kpis": kpis,
            "comments": classified_comments,
            "sentiment_summary": sentiment_summary,
            "feedback_report": feedback_report,
            "pie_chart": pie_fig,
            "bar_chart": bar_fig,
            "engagement_chart": engagement_fig
        }

    def create_sentiment_pie(self, summary: SentimentBreakdown) -> go.Figure:
        """Create responsive donut chart for sentiment distribution."""
        labels = ["Positive", "Negative", "Neutral"]
        values = [summary.positive_count, summary.negative_count, summary.neutral_count]
        colors = ["#10B981", "#EF4444", "#6B7280"]

        if sum(values) == 0:
            values = [1, 1, 1]
            labels = ["No Data", "No Data", "No Data"]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors),
            textinfo="label+percent",
            hoverinfo="label+value+percent"
        )])
        fig.update_layout(
            title_text="Audience Sentiment Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif"),
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        return fig

    def create_sentiment_bar(self, summary: SentimentBreakdown) -> go.Figure:
        """Create bar chart showing absolute comment counts per sentiment."""
        df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Count": [summary.positive_count, summary.negative_count, summary.neutral_count],
            "Color": ["#10B981", "#EF4444", "#6B7280"]
        })
        fig = px.bar(
            df,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            color_discrete_map={"Positive": "#10B981", "Negative": "#EF4444", "Neutral": "#6B7280"},
            title="Comment Classification Volume"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif"),
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig

    def create_engagement_chart(self, kpis: AnalyticsKPIs) -> go.Figure:
        """Create horizontal comparison chart for public engagement metrics."""
        metrics = ["Views", "Likes", "Comments"]
        counts = [kpis.views or 0, kpis.likes or 0, kpis.comments_count or 0]

        fig = go.Figure(data=[go.Bar(
            y=metrics,
            x=counts,
            orientation='h',
            marker=dict(color=["#6366F1", "#3B82F6", "#8B5CF6"])
        )])
        fig.update_layout(
            title_text="Audience Reach & Interaction Scale (Logarithmic)",
            xaxis_type="log",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig

youtube_analytics_agent = YouTubeAnalyticsAgent()
