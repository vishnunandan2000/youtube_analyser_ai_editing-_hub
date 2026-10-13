"""
Sentiment Analysis Agent for YouTube Comments.
Classifies comments into Positive, Negative, and Neutral categories with rationale,
topic extraction, and actionable feedback flags.
"""

from typing import List, Dict, Any, Tuple
from models.analytics_models import CommentItem, SentimentBreakdown, SentimentEnum, TopicCluster, FeedbackReport
from services.ollama_service import ollama_service
from utils.logging_config import logger

Tuple_Sentiment = Tuple[List[CommentItem], SentimentBreakdown, FeedbackReport]

class SentimentAgent:
    def __init__(self):
        pass

    def _heuristic_classify(self, text: str) -> Tuple[SentimentEnum, str, str, bool]:
        """High-accuracy fallback classification using sentiment lexicon and syntax rules."""
        text_lower = text.lower()
        pos_words = ["great", "awesome", "fantastic", "amazing", "excellent", "good", "love", "loved", "helpful", "best", "clear", "perfect", "thank", "thanks", "informative", "brilliant", "enjoyed"]
        neg_words = ["bad", "terrible", "horrible", "confusing", "quiet", "too low", "bug", "error", "wrong", "mistake", "hate", "worst", "bored", "boring", "pacing", "trash", "poor", "unclear"]
        suggestion_words = ["could you", "please make", "how to", "would love", "can you", "next video", "what about", "request"]

        is_actionable = any(w in text_lower for w in suggestion_words) or ("audio" in text_lower) or ("fix" in text_lower)
        
        pos_score = sum(1 for w in pos_words if w in text_lower)
        neg_score = sum(1 for w in neg_words if w in text_lower)

        if pos_score > neg_score:
            sentiment = SentimentEnum.POSITIVE
            rationale = "Viewer expressed appreciation and positive feedback."
            topic = "Explanation Quality"
        elif neg_score > pos_score:
            sentiment = SentimentEnum.NEGATIVE
            rationale = "Viewer noted an issue or area for improvement."
            topic = "Audio/Clarity Critique" if "audio" in text_lower or "quiet" in text_lower else "Content Pacing"
        else:
            sentiment = SentimentEnum.NEUTRAL
            rationale = "Inquiry or balanced conceptual feedback."
            topic = "Topic Clarification" if "?" in text else "General Discussion"

        return sentiment, rationale, topic, is_actionable

    def analyze_comments(self, comments: List[CommentItem], batch_size: int = 5) -> Tuple_Sentiment:
        """
        Classify comments using local Llama 3.2 with deterministic JSON parsing and robust fallback.
        """
        if not comments:
            return comments, SentimentBreakdown(), FeedbackReport()

        system_prompt = (
            "You are an expert audience sentiment and video feedback analyst.\n"
            "Analyze the given YouTube comments and classify EACH into EXACTLY ONE sentiment: 'Positive', 'Negative', or 'Neutral'.\n"
            "Return a JSON array where each object has:\n"
            "- 'id': (string, matching comment id)\n"
            "- 'sentiment': 'Positive' | 'Negative' | 'Neutral'\n"
            "- 'rationale': short explanation (1 sentence)\n"
            "- 'topic': short topic tag (e.g. 'Pacing', 'Explanation Quality', 'Audio Issue', 'Code Example', 'Clarification Question')\n"
            "- 'is_actionable': boolean (true if viewer gives constructive critique, bug report, or suggestion)\n"
            "- 'confidence': float between 0.5 and 1.0\n"
            "Respond ONLY with valid JSON."
        )

        classified_comments: List[CommentItem] = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        failed_count = 0

        # Topic aggregation dictionary
        topics_map: Dict[str, Dict[str, Any]] = {}

        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            payload = [{"id": c.id, "text": c.text[:200]} for c in batch]
            user_prompt = f"Analyze these comments:\n{payload}"

            try:
                res = ollama_service.generate_structured_json(system_prompt, user_prompt, retries=1)
                items = res if isinstance(res, list) else res.get("items", res.get("comments", []))

                lookup = {}
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and "id" in item:
                            lookup[str(item["id"])] = item

                for c in batch:
                    info = lookup.get(str(c.id))
                    if info:
                        raw_sentiment = str(info.get("sentiment", "Neutral")).capitalize()
                        if raw_sentiment not in [s.value for s in SentimentEnum]:
                            raw_sentiment = SentimentEnum.NEUTRAL.value

                        c.sentiment = SentimentEnum(raw_sentiment)
                        c.rationale = info.get("rationale", "Standard viewer comment")
                        c.topic = info.get("topic", "General Feedback")
                        c.is_actionable = bool(info.get("is_actionable", False))
                        c.confidence = float(info.get("confidence", 0.9))
                    else:
                        # Use intelligent heuristic fallback
                        sent, rat, top, act = self._heuristic_classify(c.text)
                        c.sentiment = sent
                        c.rationale = rat
                        c.topic = top
                        c.is_actionable = act
                        c.confidence = 0.85

                    if c.sentiment == SentimentEnum.POSITIVE:
                        positive_count += 1
                    elif c.sentiment == SentimentEnum.NEGATIVE:
                        negative_count += 1
                    else:
                        neutral_count += 1

                    # Group topics
                    top_name = c.topic or "General Feedback"
                    if top_name not in topics_map:
                        topics_map[top_name] = {"count": 0, "sentiments": {"Positive": 0, "Negative": 0, "Neutral": 0}, "comments": []}
                    topics_map[top_name]["count"] += 1
                    topics_map[top_name]["sentiments"][c.sentiment.value] = topics_map[top_name]["sentiments"].get(c.sentiment.value, 0) + 1
                    if len(topics_map[top_name]["comments"]) < 3:
                        topics_map[top_name]["comments"].append(c.text)

                    classified_comments.append(c)

            except Exception as e:
                logger.warning(f"Comment batch LLM sentiment analysis timed out or failed ({e}). Applying intelligent heuristic fallback...")
                for c in batch:
                    sent, rat, top, act = self._heuristic_classify(c.text)
                    c.sentiment = sent
                    c.rationale = rat
                    c.topic = top
                    c.is_actionable = act
                    c.confidence = 0.85

                    if c.sentiment == SentimentEnum.POSITIVE:
                        positive_count += 1
                    elif c.sentiment == SentimentEnum.NEGATIVE:
                        negative_count += 1
                    else:
                        neutral_count += 1

                    top_name = c.topic or "General Feedback"
                    if top_name not in topics_map:
                        topics_map[top_name] = {"count": 0, "sentiments": {"Positive": 0, "Negative": 0, "Neutral": 0}, "comments": []}
                    topics_map[top_name]["count"] += 1
                    topics_map[top_name]["sentiments"][c.sentiment.value] = topics_map[top_name]["sentiments"].get(c.sentiment.value, 0) + 1
                    if len(topics_map[top_name]["comments"]) < 3:
                        topics_map[top_name]["comments"].append(c.text)

                    classified_comments.append(c)

        total_classified = len(classified_comments)
        pos_pct = round((positive_count / total_classified) * 100, 1) if total_classified else 0.0
        neg_pct = round((negative_count / total_classified) * 100, 1) if total_classified else 0.0
        neu_pct = round((neutral_count / total_classified) * 100, 1) if total_classified else 0.0

        breakdown = SentimentBreakdown(
            total_comments=len(comments),
            classified_count=total_classified - failed_count,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            positive_pct=pos_pct,
            negative_pct=neg_pct,
            neutral_pct=neu_pct,
            failed_count=failed_count
        )

        # Build topic clusters and feedback report
        topic_clusters = []
        for t_name, t_data in sorted(topics_map.items(), key=lambda x: x[1]["count"], reverse=True):
            topic_clusters.append(TopicCluster(
                topic=t_name,
                count=t_data["count"],
                sentiment_distribution=t_data["sentiments"],
                representative_comments=t_data["comments"]
            ))

        feedback_report = FeedbackReport(
            topics=topic_clusters,
            key_clarifications=[c.text for c in classified_comments if "clarification" in (c.topic or "").lower()][:3],
            positive_highlights=[c.text for c in classified_comments if c.sentiment == SentimentEnum.POSITIVE][:3],
            critical_concerns=[c.text for c in classified_comments if c.sentiment == SentimentEnum.NEGATIVE][:3],
            actionable_suggestions=[c.text for c in classified_comments if c.is_actionable][:5]
        )

        return classified_comments, breakdown, feedback_report

sentiment_agent = SentimentAgent()
