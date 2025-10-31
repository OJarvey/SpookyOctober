# Halloween Games Feature Specification

**Status**: Draft
**Created**: 31 October 2025
**Target Audience**: Kids & Teachers (Educational + Fun)
**Technical Focus**: Django, Python, Database-heavy, Minimal JS/styling

---

## 🎯 Project Overview

A collection of Halloween-themed educational games integrated into ShriekedIn. Primary focus on a **Mad Libs** game using classic Halloween literature (Edgar Allan Poe, etc.) with additional simple games as stretch goals.

**Educational Value**: Teaches grammar (parts of speech) in an engaging, Halloween-themed context.

---

## 🎮 Game 1: Spooky Mad Libs (MVP)

### Description

Users fill in parts of speech (adjectives, nouns, verbs, etc.) to create humorous or creepy variations of classic Halloween literature. Can manually enter words OR let the app randomly select from a Halloween vocabulary database.

### User Stories

1. **As a student**, I want to enter my own words to create a funny Halloween story
2. **As a student**, I want the app to choose random spooky words for me
3. **As a teacher**, I want to display completed Mad Libs in class
4. **As a teacher**, I want to save and share student-created Mad Libs

### Features

#### Core Features (Phase 1)
- **Story Template Library**: Pre-built templates from public domain literature
  - Edgar Allan Poe excerpts ("The Raven", "The Tell-Tale Heart")
  - Classic Halloween poems
  - Spooky short stories

- **Word Input Interface**: Simple form where users enter words by part of speech
  - Clear labels: "Enter a NOUN (person, place, or thing)"
  - "Random Word" button for each field
  - Preview mode before finalizing

- **Halloween Vocabulary Database**: Pre-populated word lists
  - Nouns: ghost, witch, cauldron, graveyard, pumpkin, etc.
  - Adjectives: spooky, creepy, haunted, eerie, ghostly, etc.
  - Verbs: scream, haunt, frighten, lurk, cackle, etc.
  - Adverbs: mysteriously, frighteningly, eerily, etc.

- **Result Display**: Show completed story with blanks filled in
  - Highlight user-entered words in different color
  - "Play Again" button
  - "Share" button (copy link)

#### Enhanced Features (Phase 2)
- Save completed Mad Libs to user account
- Gallery of public Mad Libs (moderated)
- "Print" button for classroom use
- Difficulty levels (Easy: 5 blanks, Medium: 10 blanks, Hard: 15+ blanks)
- Teacher dashboard: Create custom templates

### Database Schema

```python
# Models

class StoryTemplate(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)  # e.g., "Edgar Allan Poe"
    original_text = models.TextField()
    template_text = models.TextField()  # Text with [NOUN], [ADJECTIVE] placeholders
    difficulty = models.CharField(max_length=20)  # easy, medium, hard
    word_count = models.IntegerField()  # number of blanks
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class VocabularyWord(models.Model):
    word = models.CharField(max_length=100)
    part_of_speech = models.CharField(max_length=20)  # noun, verb, adjective, adverb
    category = models.CharField(max_length=50)  # halloween, spooky, classic
    is_kid_friendly = models.BooleanField(default=True)

class CompletedMadLib(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(StoryTemplate, on_delete=models.CASCADE)
    completed_text = models.TextField()
    user_words = models.JSONField()  # Store the words used
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    share_code = models.CharField(max_length=20, unique=True)  # For sharing
```

### URL Routes

```python
# urls.py
path('games/', views.games_home, name='games_home'),
path('games/madlibs/', views.madlibs_list, name='madlibs_list'),
path('games/madlibs/<int:template_id>/', views.madlibs_play, name='madlibs_play'),
path('games/madlibs/<int:template_id>/submit/', views.madlibs_submit, name='madlibs_submit'),
path('games/madlibs/result/<str:share_code>/', views.madlibs_result, name='madlibs_result'),
path('api/random-word/<str:part_of_speech>/', views.api_random_word, name='api_random_word'),
```

### API Endpoints

```python
# GET /api/random-word/noun/
# Returns: {"word": "graveyard", "part_of_speech": "noun"}

# POST /games/madlibs/<id>/submit/
# Body: {"noun_1": "ghost", "adjective_1": "creepy", ...}
# Returns: {"share_code": "abc123", "completed_text": "..."}
```

### Frontend Requirements (Minimal)

- Simple form with labeled inputs
- One button per input: "Random Word" (triggers AJAX call)
- Result page with styled text display
- NO complex animations or image manipulation
- Basic Tailwind CSS styling (consistent with site)

### Sample Story Template

```
Original: "Once upon a midnight dreary, while I pondered, weak and weary..."

Template: "Once upon a [ADJECTIVE] [NOUN], while I [VERB], [ADJECTIVE] and [ADJECTIVE]..."

User fills in:
- ADJECTIVE: spooky
- NOUN: night
- VERB: wandered
- ADJECTIVE: tired
- ADJECTIVE: scared

Result: "Once upon a spooky night, while I wandered, tired and scared..."
```

---

## 🎮 Game 2: Bobbing for Apples (Stretch Goal)

### Description

Simple keyboard/mouse game where player tries to "catch" floating apples by clicking or pressing a key before time runs out.

### Technical Notes

- **Minimal approach**: Use HTML/CSS for positioning, basic JavaScript for clicking
- Track score in session/database
- Leaderboard (optional)

### Implementation Priority

- **Phase 3** (after Mad Libs is complete)
- Can be built as standalone page with minimal Django integration

---

## 🎮 Game 3: Haunted House Builder (Stretch Goal)

### Description

Drag-and-drop or selection-based interface to build a custom haunted house. Choose rooms, decorations, and spooky elements.

### Technical Notes

- **Could use**: Simple form-based approach instead of drag-drop
- User selects from dropdowns: "Living Room", "Add Ghost", "Add Cobwebs"
- Generate a text description or simple visual representation
- Save configurations to database

### Implementation Priority

- **Phase 4** (low priority, complex frontend)

---

## 🎮 Game 4: Trick or Treat Showdown (Stretch Goal)

### Description

Two-player game where players take turns choosing which house to visit. Random chance determines if they get candy or a "trick" (spider, etc.). Player with most candy wins.

### Technical Notes

- Turn-based game state stored in session
- Simple button interface: "House 1", "House 2", "House 3"
- Random outcome generation in Django
- Could be async (Django Channels) or simple refresh-based

### Implementation Priority

- **Phase 5** (fun but complex game logic)

---

## 📋 Implementation Roadmap

### Phase 1: Mad Libs MVP (Priority 1)
**Estimated Time**: 2-3 days

- [x] Design database models
- [ ] Create story templates (5 minimum)
- [ ] Populate vocabulary database (50+ words per part of speech)
- [ ] Build template selection page
- [ ] Build word input form
- [ ] Implement random word API endpoint
- [ ] Build result display page
- [ ] Add basic sharing functionality

### Phase 2: Mad Libs Enhanced
**Estimated Time**: 2 days

- [ ] User accounts integration
- [ ] Save completed Mad Libs
- [ ] Public gallery (moderated)
- [ ] Teacher dashboard
- [ ] Print functionality

### Phase 3: Additional Games
**Estimated Time**: TBD (depends on scope)

- [ ] Bobbing for Apples (simplest)
- [ ] Trick or Treat Showdown (medium)
- [ ] Haunted House Builder (complex, may skip)

---

## 🛠️ Technology Stack

### Required
- **Backend**: Django 5.2.7, Python
- **Database**: PostgreSQL (preferred by developer)
- **Frontend**: Tailwind CSS (already in use)
- **JavaScript**: Minimal - only for AJAX random word fetching

### Optional (Phase 2+)
- Google Sheets API (if vocabulary management by teachers is needed)
- Django Channels (for multiplayer games)

---

## 📊 Success Metrics

1. **Educational Value**: Students understand parts of speech better
2. **Engagement**: Users complete at least 3 Mad Libs per session
3. **Teacher Adoption**: Teachers use in classroom settings
4. **Sharing**: Completed Mad Libs are shared on social media

---

## 🎨 Design Guidelines

### Keeping Developer Happy
- ✅ Database-heavy (lots of models and queries)
- ✅ Django views and forms (Python focus)
- ✅ Minimal JavaScript (only where necessary)
- ✅ No complex image manipulation
- ✅ Simple, clean Tailwind styling (no custom CSS wrestling)

### UI/UX Principles
- Clear, labeled inputs (educational context)
- Big, obvious buttons
- Immediate feedback on actions
- Mobile-friendly (responsive)
- Accessible (screen readers, keyboard navigation)

---

## 📝 Sample Data Seeds

### Story Templates (Starter Pack)

1. **"The Raven" by Edgar Allan Poe** (Excerpt)
2. **"The Tell-Tale Heart" by Edgar Allan Poe** (Excerpt)
3. **Original: "Haunted House Visit"** (Custom template)
4. **Original: "Trick or Treat Night"** (Custom template)
5. **Original: "The Friendly Ghost"** (Kid-friendly version)

### Vocabulary Sample

```python
# Nouns (Halloween themed)
ghost, witch, vampire, zombie, skeleton, pumpkin, cauldron, broomstick,
graveyard, tombstone, haunted_house, spider, bat, black_cat, werewolf,
monster, goblin, ghoul, phantom, specter

# Adjectives
spooky, creepy, haunted, eerie, mysterious, frightening, scary, dark,
ghostly, wicked, evil, sinister, gloomy, shadowy, ominous

# Verbs
scream, haunt, frighten, lurk, cackle, howl, shriek, whisper, disappear,
float, fly, cast (a spell), brew, transform, vanish

# Adverbs
mysteriously, frighteningly, eerily, silently, suddenly, slowly,
spookily, wickedly, ominously, hauntingly
```

---

## 🚀 Getting Started (for Implementation Team)

1. Read this spec thoroughly
2. Review database models
3. Create a new Django app: `python manage.py startapp games`
4. Start with Phase 1, Task 1: Database models
5. Populate vocabulary database using fixtures or admin
6. Build one story template to test
7. Create basic UI following ShriekedIn design patterns
8. Test with real users (teachers/students if possible)

---

## 💡 Future Ideas (Not Committed)

- Achievement badges for completing Mad Libs
- Class competitions (leaderboard by classroom)
- AI-generated story templates (if AI policy changes)
- Multilingual support (Spanish, French vocabulary)
- Audio narration of completed stories
- Integration with Google Classroom

---

## 📞 Questions for Developer?

- How many story templates should we launch with?
- Should vocabulary be kid-friendly only, or have filters?
- Do we need user authentication, or allow anonymous play?
- Should sharing be public by default or opt-in?
- Any specific Poe works you want to include?

---

**Let's make learning grammar spooky fun! 👻📚**
