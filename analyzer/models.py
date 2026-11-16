"""
Models for the Smart Feedback Analyzer.

Stores each feedback submission with its sentiment analysis results.
"""

from django.db import models


class Feedback(models.Model):
    """
    Model to store user feedback along with its sentiment analysis results.

    Fields:
        feedback_text: The original text submitted by the user.
        sentiment:     Classification result — Positive, Negative, or Neutral.
        compound_score: VADER compound score ranging from -1 (most negative)
                        to +1 (most positive).
        created_at:    Timestamp of when the feedback was analyzed.
    """

    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    ]

    feedback_text = models.TextField(help_text="The feedback text entered by the user.")
    sentiment = models.CharField(
        max_length=10,
        choices=SENTIMENT_CHOICES,
        help_text="Sentiment classification: Positive, Negative, or Neutral."
    )
    compound_score = models.FloatField(
        help_text="VADER compound sentiment score (-1 to +1)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the feedback was analyzed."
    )

    class Meta:
        ordering = ['-created_at']  # Most recent feedback first
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f"{self.sentiment} ({self.compound_score:.4f}) — {self.feedback_text[:50]}"
