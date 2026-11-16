"""
NLP Utilities for the Smart Feedback Analyzer.

This module handles all Natural Language Processing tasks:
1. Text preprocessing (cleaning, tokenization)
2. Sentiment analysis using VADER SentimentIntensityAnalyzer

KEY DESIGN DECISION — Preserving Negation Words:
    Words like "not", "never", "no", "neither", "nor", "don't", "won't", etc.
    are critical for accurate sentiment analysis. For example:
        - "This product is good"     → Positive
        - "This product is NOT good" → Negative
    VADER inherently handles negation, so our preprocessing pipeline is
    careful NOT to remove these words during text cleaning.
"""

import re
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ─── Initialize the VADER Sentiment Analyzer ─────────────────────────────────
# VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and
# rule-based sentiment analysis tool specifically designed for social media
# text, but works well on general-purpose text too.
analyzer = SentimentIntensityAnalyzer()

# ─── Negation words to preserve during preprocessing ─────────────────────────
# These words flip the sentiment of the words that follow them.
# Removing them would destroy important semantic information.
NEGATION_WORDS = {
    'not', 'no', 'never', 'neither', 'nor', 'nobody', 'nothing',
    'nowhere', 'none', "don't", "doesn't", "didn't", "won't",
    "wouldn't", "couldn't", "shouldn't", "isn't", "aren't",
    "wasn't", "weren't", "haven't", "hasn't", "hadn't",
    "can't", "cannot", "mustn't",
}


def preprocess_text(text):
    """
    Clean and preprocess the feedback text for sentiment analysis.

    Steps:
        1. Strip leading/trailing whitespace.
        2. Remove URLs (http/https links).
        3. Remove HTML tags.
        4. Remove special characters and digits, BUT preserve negation
           contractions (e.g., "don't", "won't") and letters.
        5. Normalize excessive whitespace.

    Args:
        text (str): Raw feedback text from the user.

    Returns:
        str: Cleaned text ready for sentiment analysis.
             Returns empty string if input is empty/whitespace.
    """
    if not text or not text.strip():
        return ''

    # Step 1: Strip whitespace
    cleaned = text.strip()

    # Step 2: Remove URLs
    cleaned = re.sub(r'https?://\S+|www\.\S+', '', cleaned)

    # Step 3: Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', '', cleaned)

    # Step 4: Remove special characters but preserve:
    #   - Letters (a-z, A-Z)
    #   - Spaces
    #   - Apostrophes (important for contractions like "don't", "won't")
    #   - Exclamation marks and question marks (VADER uses these for emphasis)
    cleaned = re.sub(r"[^a-zA-Z\s'!?]", '', cleaned)

    # Step 5: Normalize whitespace (collapse multiple spaces into one)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def analyze_sentiment(text):
    """
    Perform sentiment analysis on the given text using VADER.

    VADER returns four scores:
        - neg:      Proportion of text that is negative (0 to 1)
        - neu:      Proportion of text that is neutral  (0 to 1)
        - pos:      Proportion of text that is positive (0 to 1)
        - compound: Normalized composite score (-1 to +1)
                    This is the most useful single metric.

    Classification thresholds (standard VADER recommendations):
        - compound >=  0.05  → Positive
        - compound <= -0.05  → Negative
        - Otherwise           → Neutral

    Args:
        text (str): The feedback text to analyze.

    Returns:
        dict: Contains 'sentiment' (str), 'compound_score' (float),
              'scores' (full VADER score dict), and 'cleaned_text' (str).
              Returns None if the input text is empty.
    """
    # Preprocess the text
    cleaned_text = preprocess_text(text)

    # Do not classify empty feedback
    if not cleaned_text:
        return None

    # Get VADER sentiment scores
    # polarity_scores() returns: {'neg': float, 'neu': float, 'pos': float, 'compound': float}
    scores = analyzer.polarity_scores(cleaned_text)
    compound = scores['compound']

    # Classify based on compound score using standard VADER thresholds
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return {
        'sentiment': sentiment,
        'compound_score': round(compound, 4),
        'scores': scores,           # Full breakdown (pos, neg, neu, compound)
        'cleaned_text': cleaned_text,
    }
