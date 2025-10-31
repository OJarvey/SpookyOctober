from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import StoryTemplate, VocabularyWord, CompletedMadLib
import re
import random


def games_home(request):
    """
    Games homepage with links to available games.
    """
    context = {
        'total_templates': StoryTemplate.objects.filter(is_active=True).count(),
        'total_words': VocabularyWord.objects.count(),
        'total_completed': CompletedMadLib.objects.count(),
    }
    return render(request, 'games/games_home.html', context)


def madlibs_list(request):
    """
    List all available Mad Libs story templates.
    """
    templates = StoryTemplate.objects.filter(is_active=True)

    # Filter by difficulty if provided
    difficulty = request.GET.get('difficulty')
    if difficulty in ['easy', 'medium', 'hard']:
        templates = templates.filter(difficulty=difficulty)

    context = {
        'templates': templates,
        'selected_difficulty': difficulty,
    }
    return render(request, 'games/madlibs_list.html', context)


def madlibs_play(request, template_id):
    """
    Display form to play a specific Mad Libs template.
    """
    template = get_object_or_404(StoryTemplate, id=template_id, is_active=True)

    # Extract placeholders and create numbered list
    placeholders = template.get_placeholders()

    # Create a list of unique placeholders with indices
    placeholder_list = []
    seen = {}
    for i, placeholder in enumerate(placeholders, 1):
        # Track how many times we've seen this placeholder type
        if placeholder not in seen:
            seen[placeholder] = 1
        else:
            seen[placeholder] += 1

        placeholder_list.append({
            'index': i,
            'type': placeholder.lower(),
            'label': placeholder,
            'field_name': f'{placeholder}_{i}'
        })

    context = {
        'template': template,
        'placeholders': placeholder_list,
    }
    return render(request, 'games/madlibs_play.html', context)


def madlibs_submit(request, template_id):
    """
    Process submitted Mad Libs form and generate completed story.
    """
    if request.method != 'POST':
        return redirect('games:madlibs_play', template_id=template_id)

    template = get_object_or_404(StoryTemplate, id=template_id, is_active=True)

    # Get all form data
    user_words = {}
    for key, value in request.POST.items():
        if key.startswith(('NOUN_', 'ADJECTIVE_', 'VERB_', 'ADVERB_')):
            user_words[key] = value.strip()

    # Replace placeholders in template with user words
    completed_text = template.template_text

    # Replace each placeholder with the corresponding user word
    for i, placeholder in enumerate(template.get_placeholders(), 1):
        field_name = f'{placeholder}_{i}'
        user_word = user_words.get(field_name, '[MISSING]')

        # Replace the first occurrence of [PLACEHOLDER]
        completed_text = completed_text.replace(f'[{placeholder}]', user_word, 1)

    # Create CompletedMadLib
    completed_madlib = CompletedMadLib.objects.create(
        user=request.user if request.user.is_authenticated else None,
        template=template,
        completed_text=completed_text,
        user_words=user_words,
        is_public=False  # Could add checkbox in form
    )

    messages.success(request, 'Your Mad Libs story is ready!')
    return redirect('games:madlibs_result', share_code=completed_madlib.share_code)


def madlibs_result(request, share_code):
    """
    Display completed Mad Libs story.
    """
    madlib = get_object_or_404(CompletedMadLib, share_code=share_code)

    # Increment view count
    madlib.view_count += 1
    madlib.save(update_fields=['view_count'])

    context = {
        'madlib': madlib,
    }
    return render(request, 'games/madlibs_result.html', context)


@require_http_methods(["GET"])
def api_random_word(request, part_of_speech):
    """
    API endpoint to get a random word of a specific part of speech.

    GET /api/random-word/noun/
    Returns: {"word": "ghost", "part_of_speech": "noun"}
    """
    # Validate part of speech
    valid_pos = ['noun', 'verb', 'adjective', 'adverb']
    if part_of_speech not in valid_pos:
        return JsonResponse({
            'error': f'Invalid part of speech. Must be one of: {", ".join(valid_pos)}'
        }, status=400)

    # Get kid-friendly words only
    words = VocabularyWord.objects.filter(
        part_of_speech=part_of_speech,
        is_kid_friendly=True
    )

    if not words.exists():
        return JsonResponse({
            'error': f'No {part_of_speech} words available'
        }, status=404)

    # Get random word
    word = random.choice(words)

    return JsonResponse({
        'word': word.word,
        'part_of_speech': word.part_of_speech,
    })
