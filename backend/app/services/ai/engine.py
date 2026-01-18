from typing import List, Dict, Any
import re
from collections import Counter

class AIEngine:
    """
    MVP AI Engine for InfluencerHub.
    Uses heuristic-based analysis and rule-based categorization.
    """

    # MVP Taxonomy: Simple Keyword Mapping
    CATEGORY_KEYWORDS = {
        "Fitness": ["gym", "workout", "protein", "fitness", "yoga", "running", "lift"],
        "Tech": ["code", "software", "gadget", "crypto", "blockchain", "ai", "developer"],
        "Beauty": ["makeup", "skincare", "fashion", "style", "lipstick", "cosmetics"],
        "Food": ["recipe", "cooking", "delicious", "foodie", "restaurant", "eat"],
        "Travel": ["travel", "vacation", "trip", "hotel", "explore", "adventure"]
    }

    def categorize_bio(self, bio_text: str) -> List[str]:
        """
        Analyzes a text string (Bio/Description) and assigns categories based on keyword usage.
        Returns a list of matching categories sorted by confidence (match count).
        """
        if not bio_text:
            return []

        bio_lower = bio_text.lower()
        scores = Counter()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for word in keywords:
                # Simple word boundary regex to avoid partial matches (e.g. 'cat' in 'catch')
                if re.search(r'\b' + re.escape(word) + r'\b', bio_lower):
                    scores[category] += 1

        # Return categories with at least 1 match, sorted by score desc
        return [cat for cat, score in scores.most_common() if score > 0]

    def detect_brand_mentions(self, text: str, brand_names: List[str]) -> List[str]:
        """
        Scans text for specific brand names.
        """
        if not text:
            return []
        
        found_brands = []
        text_lower = text.lower()
        
        for brand in brand_names:
            if re.search(r'\b' + re.escape(brand.lower()) + r'\b', text_lower):
                found_brands.append(brand)
        
        return found_brands

    def analyze_sentiment_rule_based(self, text: str) -> float:
        """
        Stub for simple heuristic sentiment analysis.
        Returns score -1.0 (Negative) to 1.0 (Positive).
        """
        # Very naive MVP implementation
        positive_words = {"love", "great", "amazing", "best", "good", "excellent"}
        negative_words = {"hate", "worst", "bad", "terrible", "awful", "scam"}
        
        tokens = set(re.findall(r'\w+', text.lower()))
        pos_count = len(tokens.intersection(positive_words))
        neg_count = len(tokens.intersection(negative_words))
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0
            
        return (pos_count - neg_count) / total

# Singleton instance
ai_engine = AIEngine()
