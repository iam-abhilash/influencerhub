# AI Insight Engine Architecture

## 1. Goal
To convert unstructured data (Bio, Posts, Descriptions) into structured, queryable tags and insights **without** running expensive GPU clusters for the MVP.

## 2. Processing Pipeline

```mermaid
graph LR
    A[Raw Text Input] --> B{Clean/Normalize}
    B --> C[Keyword Extractor]
    B --> D[Brand Detector]
    
    C --> E[Category Scorer]
    D --> F[Insight Aggregator]
    
    E --> G[Final Tags (e.g., 'Fitness', 'Tech')]
    F --> H[Brand Report (e.g., 'Mentioned Nike')]
```

## 3. Algorithms (MVP vs Future)

| Feature | MVP (Current) | Future (V2 - High Scale) |
| :--- | :--- | :--- |
| **Categorization** | **Keyword Density**: Counting occurrences of predefined dictionaries (`gym` -> Fitness). | **Zero-Shot Classification**: Using DistilBERT/OpenAI to classify text into dynamic categories without hardcoded lists. |
| **Brand Detection** | **Regex Matching**: Exact string matching. | **Named Entity Recognition (NER)**: Detecting organizations even if misspelled or unknown. |
| **Sentiment** | **Bag of Words**: Counting `good` vs `bad` words. | **Transformer Sentiment**: Context-aware sentiment (e.g., detecting sarcasm). |
| **Similarity** | **Tag Overlap**: Jaccard similarity between tag lists. | **Vector Search**: Storing embeddings (Vectors) in Postgres `pgvector` for semantic "Find influencers like this". |

## 4. Why this approach?
1.  **Speed**: Regex and Dictionary lookups are O(N) and run instantly in Python.
2.  **Cost**: Zero API tokens (OpenAI/Anthropic) required for the basic pipeline.
3.  **Explainability**: If a user asks "Why is this categorized as Fitness?", we can point to the word "gym" in their bio.

## 5. Implementation Details
The core logic resides in `backend/app/services/ai/engine.py`.
- **Input**: User `bio` or Recent Post Captions.
- **Output**: List of Strings (`niche` field in DB).
- **Trigger**: Run asynchronously on `UserUpdate` or `Ingestion`.
