from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from games.models import StoryTemplate, CompletedMadLib
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds database with 10 sample Mad Libs stories for demonstration'

    def handle(self, *args, **kwargs):
        # Sample word sets for different parts of speech
        sample_words = {
            'NOUN': [
                'ghost', 'witch', 'zombie', 'vampire', 'skeleton', 'pumpkin',
                'cauldron', 'broomstick', 'coffin', 'graveyard', 'mansion',
                'werewolf', 'mummy', 'spider', 'bat', 'owl', 'black cat'
            ],
            'ADJECTIVE': [
                'spooky', 'creepy', 'haunted', 'eerie', 'mysterious', 'dark',
                'scary', 'frightening', 'shadowy', 'ancient', 'cursed',
                'wicked', 'sinister', 'ghastly', 'gloomy', 'terrifying'
            ],
            'VERB': [
                'haunted', 'frightened', 'screamed', 'disappeared', 'crept',
                'whispered', 'howled', 'vanished', 'lurked', 'trembled',
                'shivered', 'rattled', 'echoed', 'floated', 'groaned'
            ],
            'ADVERB': [
                'mysteriously', 'suddenly', 'quietly', 'slowly', 'eerily',
                'darkly', 'silently', 'swiftly', 'ominously', 'strangely',
                'wickedly', 'frighteningly', 'cautiously', 'desperately'
            ]
        }

        # Get all active templates
        templates = list(StoryTemplate.objects.filter(is_active=True))

        if not templates:
            self.stdout.write(self.style.ERROR('No active story templates found. Run populate_madlibs first.'))
            return

        # Get admin user for some stories (or create anonymous)
        try:
            admin_user = User.objects.filter(is_staff=True).first()
        except:
            admin_user = None

        stories_created = 0

        for i in range(10):
            # Randomly select a template
            template = random.choice(templates)

            # Get placeholders from template
            placeholders = template.get_placeholders()

            # Build user_words dictionary and completed text
            user_words = {}
            completed_text = template.template_text

            for idx, placeholder in enumerate(placeholders, 1):
                # Get a random word of the appropriate type
                word_type = placeholder.split('_')[0]  # Get NOUN, ADJECTIVE, etc.
                word = random.choice(sample_words.get(word_type, ['mystery']))

                # Store in user_words
                field_name = f'{placeholder}_{idx}'
                user_words[field_name] = word

                # Replace in completed text
                completed_text = completed_text.replace(f'[{placeholder}]', word, 1)

            # Randomly assign user or make anonymous (70% anonymous, 30% with user)
            story_user = None
            if admin_user and random.random() > 0.7:
                story_user = admin_user

            # Create story with varied creation time (spread over last 3 days)
            hours_ago = random.randint(1, 72)
            created_at = timezone.now() - timedelta(hours=hours_ago)

            # Create the completed story
            story = CompletedMadLib.objects.create(
                user=story_user,
                template=template,
                completed_text=completed_text,
                user_words=user_words,
                is_public=False
            )

            # Manually set created_at to vary the times
            story.created_at = created_at
            story.view_count = random.randint(0, 25)
            story.save()

            stories_created += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Created story {stories_created}/10: "{template.title}" '
                    f'(share_code: {story.share_code})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎃 Successfully created {stories_created} sample Mad Libs stories!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'View them at: /games/'
            )
        )
