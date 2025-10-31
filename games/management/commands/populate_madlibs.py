from django.core.management.base import BaseCommand
from games.models import StoryTemplate, VocabularyWord


class Command(BaseCommand):
    help = 'Populate database with story templates and vocabulary for Mad Libs game'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating Mad Libs data...'))

        # Clear existing data
        StoryTemplate.objects.all().delete()
        VocabularyWord.objects.all().delete()

        # Create story templates
        self.create_story_templates()

        # Create vocabulary
        self.create_vocabulary()

        self.stdout.write(self.style.SUCCESS('✅ Successfully populated Mad Libs data!'))

    def create_story_templates(self):
        """Create Halloween-themed story templates."""

        templates = [
            {
                'title': 'The Raven (Edgar Allan Poe)',
                'author': 'Edgar Allan Poe',
                'difficulty': 'medium',
                'word_count': 10,
                'original_text': 'Once upon a midnight dreary, while I pondered, weak and weary, Over many a quaint and curious volume of forgotten lore...',
                'template_text': '''Once upon a [ADJECTIVE] midnight, while I [VERB], [ADJECTIVE] and [ADJECTIVE],
Over many a [ADJECTIVE] and [ADJECTIVE] volume of forgotten [NOUN].
While I [VERB], nearly [VERB], suddenly there came a [NOUN],
As of someone [ADVERB] [VERB] at my chamber [NOUN].'''
            },
            {
                'title': 'Trick or Treat Night',
                'author': 'ShriekedIn Original',
                'difficulty': 'easy',
                'word_count': 5,
                'original_text': 'A fun Halloween adventure about dressing up in costume and going trick-or-treating around the neighborhood collecting candy.',
                'template_text': '''On Halloween night, I dressed up as a [NOUN] and went trick-or-treating.
My costume was so [ADJECTIVE] that everyone [VERB] when they saw me!
I collected candy in my [ADJECTIVE] [NOUN] and had a [ADJECTIVE] time!'''
            },
            {
                'title': 'The Haunted House',
                'author': 'ShriekedIn Original',
                'difficulty': 'easy',
                'word_count': 8,
                'original_text': 'A spooky tale about an old house at the end of the street that everyone says is haunted by mysterious creatures.',
                'template_text': '''There was an old [ADJECTIVE] house at the end of [NOUN] Street.
Everyone said it was [ADJECTIVE] by a [NOUN] and a [NOUN].
One night, I [ADVERB] walked up to the [ADJECTIVE] door and heard someone [VERB].
I [VERB] away as fast as I could!'''
            },
            {
                'title': 'The Friendly Ghost',
                'author': 'ShriekedIn Original',
                'difficulty': 'easy',
                'word_count': 7,
                'original_text': 'A heartwarming story about a friendly ghost who loves making friends with children every Halloween.',
                'template_text': '''Once there was a [ADJECTIVE] ghost named [NOUN].
Unlike other ghosts, [NOUN] was very [ADJECTIVE] and loved to [VERB].
Every Halloween, [NOUN] would [ADVERB] [VERB] around the neighborhood,
making friends with all the [ADJECTIVE] children.'''
            },
            {
                'title': 'The Tell-Tale Heart (Edgar Allan Poe)',
                'author': 'Edgar Allan Poe',
                'difficulty': 'hard',
                'word_count': 15,
                'original_text': 'True! Nervous, very, very dreadfully nervous I had been and am; but why will you say that I am mad?',
                'template_text': '''True! [ADJECTIVE], very, very [ADVERB] [ADJECTIVE] I had been and am!
But why will you say that I am [ADJECTIVE]?
The [NOUN] sharpened my senses, not [VERB] them.
Above all was the sense of [NOUN] [ADJECTIVE].
I heard all things in the [NOUN] and in the [NOUN].
I heard many things in [NOUN].
How, then, am I [ADJECTIVE]?
[VERB] how [ADVERB] I [VERB]!
Observe how [ADVERB], how [ADVERB], how [ADVERB] I proceeded!'''
            },
            {
                'title': 'The Witch\'s Brew',
                'author': 'ShriekedIn Original',
                'difficulty': 'medium',
                'word_count': 10,
                'original_text': 'A magical story about a witch brewing a mysterious potion in her cauldron with strange ingredients.',
                'template_text': '''In a [ADJECTIVE] cauldron, the old witch began to [VERB].
First, she added three [ADJECTIVE] [NOUN] and a pinch of [NOUN].
Then she [ADVERB] stirred in some [ADJECTIVE] [NOUN].
The potion bubbled and turned [ADJECTIVE]!
"Perfect!" she cackled [ADVERB]. "Now anyone who drinks this will [VERB] like a [NOUN]!"'''
            },
            {
                'title': 'Graveyard at Midnight',
                'author': 'ShriekedIn Original',
                'difficulty': 'medium',
                'word_count': 12,
                'original_text': 'A chilling encounter in a foggy graveyard at midnight where mysterious sounds and figures appear among the tombstones.',
                'template_text': '''The old graveyard was [ADJECTIVE] and [ADJECTIVE] at midnight.
Fog [ADVERB] [VERB] between the [ADJECTIVE] tombstones.
Suddenly, I heard a [ADJECTIVE] [NOUN] coming from behind a [NOUN].
My heart began to [VERB] [ADVERB].
I wanted to [VERB], but my [ADJECTIVE] legs wouldn't move!
Then I saw it—a [ADJECTIVE] figure [VERB] toward me!'''
            }
        ]

        for data in templates:
            StoryTemplate.objects.create(**data)
            self.stdout.write(f'  ✓ Created template: {data["title"]}')

    def create_vocabulary(self):
        """Create Halloween-themed vocabulary words."""

        # Nouns (Halloween themed)
        nouns = [
            'ghost', 'witch', 'vampire', 'zombie', 'skeleton', 'pumpkin', 'cauldron',
            'broomstick', 'graveyard', 'tombstone', 'haunted_house', 'spider', 'bat',
            'black_cat', 'werewolf', 'monster', 'goblin', 'ghoul', 'phantom', 'specter',
            'shadow', 'moon', 'night', 'darkness', 'fog', 'mist', 'castle', 'dungeon',
            'coffin', 'crypt', 'potion', 'spell', 'wand', 'candy', 'costume', 'mask',
            'door', 'window', 'stairs', 'hallway', 'room', 'attic', 'basement', 'forest',
            'tree', 'owl', 'rat', 'scream', 'whisper', 'laugh', 'howl'
        ]

        # Adjectives
        adjectives = [
            'spooky', 'creepy', 'haunted', 'eerie', 'mysterious', 'frightening', 'scary',
            'dark', 'ghostly', 'wicked', 'evil', 'sinister', 'gloomy', 'shadowy', 'ominous',
            'ancient', 'old', 'abandoned', 'lonely', 'silent', 'quiet', 'loud', 'terrible',
            'horrible', 'dreadful', 'awful', 'hideous', 'gruesome', 'macabre', 'ghastly',
            'pale', 'cold', 'frozen', 'dead', 'lifeless', 'strange', 'weird', 'bizarre',
            'peculiar', 'odd', 'unusual', 'twisted', 'crooked', 'bent', 'broken', 'shattered',
            'bloody', 'rotten', 'decayed', 'moldy', 'dusty'
        ]

        # Verbs
        verbs = [
            'scream', 'haunt', 'frighten', 'lurk', 'cackle', 'howl', 'shriek', 'whisper',
            'disappear', 'float', 'fly', 'cast', 'brew', 'transform', 'vanish', 'appear',
            'creep', 'crawl', 'sneak', 'hide', 'watch', 'follow', 'chase', 'run', 'walk',
            'stumble', 'trip', 'fall', 'climb', 'jump', 'dance', 'spin', 'twirl', 'shake',
            'shiver', 'tremble', 'quake', 'shudder', 'gasp', 'sob', 'cry', 'laugh', 'giggle',
            'moan', 'groan', 'wail', 'howl', 'yell', 'call', 'summon'
        ]

        # Adverbs
        adverbs = [
            'mysteriously', 'frighteningly', 'eerily', 'silently', 'suddenly', 'slowly',
            'spookily', 'wickedly', 'ominously', 'hauntingly', 'darkly', 'gloomily',
            'quickly', 'rapidly', 'swiftly', 'carefully', 'cautiously', 'nervously',
            'anxiously', 'fearfully', 'terribly', 'horribly', 'dreadfully', 'awfully',
            'strangely', 'oddly', 'weirdly', 'bizarrely', 'quietly', 'loudly', 'softly',
            'gently', 'roughly', 'violently', 'wildly', 'madly', 'crazily'
        ]

        # Create vocabulary words
        for word in nouns:
            VocabularyWord.objects.get_or_create(
                word=word,
                part_of_speech='noun',
                defaults={
                    'category': 'halloween',
                    'is_kid_friendly': True
                }
            )

        for word in adjectives:
            VocabularyWord.objects.get_or_create(
                word=word,
                part_of_speech='adjective',
                defaults={
                    'category': 'spooky',
                    'is_kid_friendly': True
                }
            )

        for word in verbs:
            VocabularyWord.objects.get_or_create(
                word=word,
                part_of_speech='verb',
                defaults={
                    'category': 'halloween',
                    'is_kid_friendly': True
                }
            )

        for word in adverbs:
            VocabularyWord.objects.get_or_create(
                word=word,
                part_of_speech='adverb',
                defaults={
                    'category': 'spooky',
                    'is_kid_friendly': True
                }
            )

        self.stdout.write(f'  ✓ Created {len(nouns)} nouns')
        self.stdout.write(f'  ✓ Created {len(adjectives)} adjectives')
        self.stdout.write(f'  ✓ Created {len(verbs)} verbs')
        self.stdout.write(f'  ✓ Created {len(adverbs)} adverbs')
        self.stdout.write(f'  ✓ Total: {len(nouns) + len(adjectives) + len(verbs) + len(adverbs)} vocabulary words')
