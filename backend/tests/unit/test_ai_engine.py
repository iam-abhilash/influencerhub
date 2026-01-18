import pytest
from app.services.ai.engine import ai_engine

class TestAIEngine:
    def test_fitness_categorization(self):
        bio = "I love gym and protein shakes. Workout daily."
        cats = ai_engine.categorize_bio(bio)
        assert "Fitness" in cats
        assert "Tech" not in cats

    def test_mixed_categorization(self):
        bio = "Coding all day, running all night."
        cats = ai_engine.categorize_bio(bio)
        assert "Tech" in cats
        assert "Fitness" in cats

    def test_sentiment_positive(self):
        text = "This product is amazing and I love it!"
        score = ai_engine.analyze_sentiment_rule_based(text)
        assert score > 0.3

    def test_sentiment_negative(self):
        text = "This is the worst scam ever. Hate it."
        score = ai_engine.analyze_sentiment_rule_based(text)
        assert score < -0.3
