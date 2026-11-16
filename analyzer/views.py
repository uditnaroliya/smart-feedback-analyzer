"""
Views for the Smart Feedback Analyzer.

Handles:
    - Displaying the dashboard (home page)
    - Processing feedback submissions and performing sentiment analysis
    - Deleting individual feedback records from history
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Feedback
from .nlp_utils import analyze_sentiment


def home(request):
    """
    Home page / Dashboard view.

    GET:  Renders the dashboard with statistics, feedback form, and history.
    POST: Processes the submitted feedback text through NLP pipeline,
          saves the result, and displays the analysis outcome.
    """
    result = None  # Holds the sentiment analysis result for display

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text', '').strip()

        # Do not classify empty feedback
        if not feedback_text:
            messages.warning(request, 'Please enter some feedback text before analyzing.')
        else:
            # Perform NLP-based sentiment analysis
            result = analyze_sentiment(feedback_text)

            if result:
                # Save the feedback and analysis result to the database
                Feedback.objects.create(
                    feedback_text=feedback_text,
                    sentiment=result['sentiment'],
                    compound_score=result['compound_score'],
                )
                messages.success(request, 'Feedback analyzed and saved successfully!')
            else:
                messages.warning(
                    request,
                    'Could not analyze the feedback. Please enter valid text.'
                )

    # ─── Dashboard Statistics ─────────────────────────────────────────────
    all_feedback = Feedback.objects.all()
    total_count = all_feedback.count()
    positive_count = all_feedback.filter(sentiment='Positive').count()
    negative_count = all_feedback.filter(sentiment='Negative').count()
    neutral_count = all_feedback.filter(sentiment='Neutral').count()

    # ─── Feedback History (most recent first, via model ordering) ─────────
    history = all_feedback[:20]  # Show last 20 entries

    context = {
        'result': result,
        'history': history,
        'total_count': total_count,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
    }
    return render(request, 'analyzer/index.html', context)


def delete_feedback(request, pk):
    """
    Delete a single feedback record from the history.

    Args:
        pk: Primary key of the Feedback record to delete.
    """
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    messages.info(request, 'Feedback record deleted.')
    return redirect('home')
