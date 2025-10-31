from django.db import models
from django.contrib.auth.models import User
import secrets
import string


class StoryTemplate(models.Model):
    """
    Halloween-themed story templates for Mad Libs game.
    Templates contain placeholders like [NOUN], [ADJECTIVE], etc.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy (5 blanks)'),
        ('medium', 'Medium (10 blanks)'),
        ('hard', 'Hard (15+ blanks)'),
    ]

    title = models.CharField(max_length=200, help_text="Story title")
    author = models.CharField(max_length=100, help_text="Original author (e.g., Edgar Allan Poe)")
    original_text = models.TextField(help_text="Original unmodified text", blank=True)
    template_text = models.TextField(
        help_text="Text with placeholders like [NOUN], [ADJECTIVE], [VERB], [ADVERB]"
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    word_count = models.IntegerField(help_text="Number of blanks to fill", default=5)
    is_active = models.BooleanField(default=True, help_text="Show in template list")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['difficulty', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"

    def get_placeholders(self):
        """Extract all placeholders from template text."""
        import re
        placeholders = re.findall(r'\[(\w+)\]', self.template_text)
        return placeholders


class VocabularyWord(models.Model):
    """
    Halloween-themed vocabulary for random word generation.
    """
    PART_OF_SPEECH_CHOICES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
    ]

    CATEGORY_CHOICES = [
        ('halloween', 'Halloween'),
        ('spooky', 'Spooky'),
        ('classic', 'Classic'),
        ('silly', 'Silly'),
    ]

    word = models.CharField(max_length=100, help_text="The vocabulary word")
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='halloween')
    is_kid_friendly = models.BooleanField(default=True, help_text="Appropriate for children")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['part_of_speech', 'word']
        unique_together = ['word', 'part_of_speech']

    def __str__(self):
        return f"{self.word} ({self.get_part_of_speech_display()})"


class CompletedMadLib(models.Model):
    """
    Stores completed Mad Libs for sharing and saving.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='completed_madlibs',
        help_text="User who created this (optional for anonymous play)"
    )
    template = models.ForeignKey(StoryTemplate, on_delete=models.CASCADE)
    completed_text = models.TextField(help_text="Story with blanks filled in")
    user_words = models.JSONField(help_text="Dictionary of words used: {'NOUN_1': 'ghost', ...}")
    is_public = models.BooleanField(default=False, help_text="Show in public gallery")
    share_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique code for sharing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0, help_text="Number of times viewed")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{self.template.title} by {username} ({self.share_code})"

    def save(self, *args, **kwargs):
        """Generate unique share code if not set."""
        if not self.share_code:
            self.share_code = self.generate_share_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_share_code(length=8):
        """Generate a random alphanumeric share code."""
        characters = string.ascii_lowercase + string.digits
        while True:
            code = ''.join(secrets.choice(characters) for _ in range(length))
            if not CompletedMadLib.objects.filter(share_code=code).exists():
                return code
