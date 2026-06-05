"""
Загрузка реальных вариантов тестов из PDF-файлов.
Английский язык: все 4 варианта (9 кл. V1/V2, 11 кл. VA/VB) — вопросы извлечены из PDF.
Математика и Русский язык: нужно добавить вручную (PDF недоступны для автоматического чтения).

Запуск: py load_real_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcollege.settings')
django.setup()

from testing.models import Subject, TestVariant, Question, AnswerOption

# ─── Предметы ───
eng, _ = Subject.objects.get_or_create(name='Английский язык', defaults={'order': 1})
mat, _ = Subject.objects.get_or_create(name='Математика',      defaults={'order': 2})
rus, _ = Subject.objects.get_or_create(name='Русский язык',    defaults={'order': 3})

# ════════════════════════════════════════════════════════════════
#  АНГЛИЙСКИЙ ЯЗЫК — 9 класс, Вариант 1
# ════════════════════════════════════════════════════════════════
# (текст вопроса, [A, B, C, ...], индекс_правильного_0)
ENG_9_V1 = [
    ("They ___ Spanish. They are Mexican.",
     ["aren't", "not", "am not"], 0),
    ("Ferrari is a ___",
     ["car fast", "fast car", "fastest car"], 1),
    ("He ___ a shower before breakfast",
     ["always has", "has always", "have always"], 0),
    ("They ___ meat.",
     ["don't eats", "doesn't eat", "don't eat"], 2),
    ("I hate ___ at the weekend.",
     ["study", "to study", "studying"], 2),
    ("___ park here?",
     ["Can I", "Do I can", "Am I"], 0),
    ("Where ___ you yesterday at six o'clock?",
     ["was", "were", "was not"], 1),
    ("There aren't ___ windows.",
     ["some", "any", "none"], 1),
    ("We ___ lunch at a great restaurant last Sunday.",
     ["haved", "have", "had"], 2),
    ("___ the film?",
     ["Did you like", "Liked you", "Does you like"], 0),
    ("What is 'Bonjour' ___ English?",
     ["of", "in", "to"], 1),
    ("She is Brazilian. ___ name is Daniela.",
     ["his", "her", "your"], 1),
    ("I ___ early.",
     ["usually get up", "get usually up", "get up usually"], 0),
    ("Circle the different word: brother, grandfather, niece, uncle",
     ["brother", "grandfather", "niece", "uncle"], 2),
    ("This is my ___ house.",
     ["parent's", "parents", "parents'"], 2),
    ("The weather is cold, but ___ raining.",
     ["it doesn't", "it not", "it isn't"], 2),
    ("The sun ___! Let's go for a walk.",
     ["shine", "shines", "is shining"], 2),
    ("A: ___ hungry?  B: Yes. What's for dinner?",
     ["Are you", "Have you", "Do you"], 0),
    ("Is your sister at home? I need to speak to ___.",
     ["him", "her", "she"], 1),
    ("A: What ___?  B: I'm a nurse.",
     ["are you doing", "do you do", "do you"], 1),
    ("Fill the gap: She was in a hurry ___ she was driving fast.",
     ["because", "although", "so"], 2),
    ("A post office is a place ___ you can buy stamps.",
     ["who", "which", "where"], 2),
    ("I am very stressed today. I have ___ work.",
     ["too many", "too much", "enough"], 1),
    ("Complete: I love ___ breakfast in bed.",
     ["having", "to have", "have"], 0),
    ("You ___ buy a ticket before you get on the bus. It costs $4.",
     ["have to", "can", "don't have to"], 0),
]

# ════════════════════════════════════════════════════════════════
#  АНГЛИЙСКИЙ ЯЗЫК — 9 класс, Вариант 2
# ════════════════════════════════════════════════════════════════
ENG_9_V2 = [
    ("___ at home last night.",
     ["is", "were", "was"], 2),
    ("I ___ go to the gym yesterday.",
     ["didn't", "doesn't", "don't"], 0),
    ("___ there any books?",
     ["Aren't", "Is", "Are"], 2),
    ("They ___ talking at the moment.",
     ["isn't", "are", "am"], 1),
    ("What time ___ he usually go to bed?",
     ["does", "do", "did"], 0),
    ("How ___ help you?",
     ["can I", "do I can", "am I"], 0),
    ("I hate ___ TV.",
     ["to watch", "watched", "watching"], 2),
    ("It is my ___ house.",
     ["parent", "parents'", "parent's"], 1),
    ("___ your T-shirts?",
     ["those", "this", "that"], 0),
    ("___ is that?  My brother Adrian.",
     ["What", "Who", "Where"], 1),
    ("She ___ already read the book.",
     ["have", "haven't", "has"], 2),
    ("He speaks English ___.",
     ["good", "well", "bad"], 1),
    ("It is ___ longest river in ___ world.",
     ["the, the", "the, a", "a, the"], 0),
    ("The tigers are ___ animals in the zoo.",
     ["more dangerous", "dangerousest", "the most dangerous"], 2),
    ("We need ___ apples for today.",
     ["any", "some", "much"], 1),
    ("Do your children drink any milk?  No, ___.",
     ["not much", "not many", "a few"], 0),
    ("Milan is ___ from the sea ___ Rome.",
     ["farther, than", "further, than", "the, furthest"], 0),
    ("My brother studies math ___ Manchester University.",
     ["in", "on", "at"], 2),
    ("She usually ___ to cinema on Sundays.",
     ["goes", "going", "go"], 0),
    ("___ do you live with?",
     ["where", "what", "who"], 2),
    ("She couldn't sleep, ___ she was very tired.",
     ["because", "although", "so"], 1),
    ("She is the woman ___ catches the same bus as me.",
     ["who", "which", "where"], 0),
    ("I am not very fit. I don't do ___ exercise.",
     ["too many", "too much", "enough"], 2),
    ("She enjoys ___ in an office.",
     ["working", "work", "to work"], 0),
    ("You ___ tidy the room before she goes out.",
     ["have to", "must to", "does not have to"], 0),
]

# ════════════════════════════════════════════════════════════════
#  АНГЛИЙСКИЙ ЯЗЫК — 11 класс, Вариант A
# ════════════════════════════════════════════════════════════════
# Answer key: 1b,2b,3b,4c,5a,6a,7b,8b,9b,10a,11a,12b,13a,14a,15b,16a,17b,18b,19c,20a,21a,22a,23b,24b,25a
ENG_11_VA = [
    ("My brother ___ to school every day.",
     ["go", "goes", "going"], 1),
    ("They ___ TV when I called them.",
     ["watched", "were watching", "watch"], 1),
    ("I have lived here ___ five years.",
     ["since", "for", "from"], 1),
    ("If it rains tomorrow, we ___ at home.",
     ["stay", "stayed", "will stay"], 2),
    ("She is ___ than her sister.",
     ["taller", "tallest", "more tall"], 0),
    ("I don't know ___ he will come.",
     ["if", "because", "although"], 0),
    ("The letter ___ yesterday.",
     ["sent", "was sent", "is sent"], 1),
    ("We enjoyed ___ in the sea.",
     ["swim", "swimming", "swam"], 1),
    ("There aren't ___ apples left.",
     ["much", "many", "a little"], 1),
    ("Which sentence is correct?",
     ["He doesn't like coffee.", "He don't like coffee.", "He not likes coffee."], 0),
    ("I ___ my homework before dinner yesterday.",
     ["finished", "have finished", "finishing"], 0),
    ("The opposite of 'easy' is:",
     ["simple", "difficult", "comfortable"], 1),
    ("Have you ever ___ to Kazakhstan?",
     ["been", "went", "go"], 0),
    ("She apologized ___ being late.",
     ["for", "at", "on"], 0),
    ("If I ___ more time, I would learn Spanish.",
     ["have", "had", "will have"], 1),
    ("The students ___ study hard usually get good grades.",
     ["who", "which", "where"], 0),
    ("We ___ this movie already.",
     ["saw", "have seen", "seeing"], 1),
    ("He is interested ___ technology.",
     ["on", "in", "at"], 1),
    ("By the time we arrived, the concert ___.",
     ["started", "has started", "had started"], 2),
    ("Which word is closest in meaning to 'brave'?",
     ["courageous", "nervous", "selfish"], 0),
    ("She asked me where I ___.",
     ["live", "life", "living"], 0),
    ("The weather was cold, ___ we went for a walk.",
     ["but", "because", "so"], 0),
    ("This is the ___ book I have ever read.",
     ["more interesting", "most interesting", "interesting"], 1),
    ("Neither my brother nor my friends ___ at home.",
     ["is", "are", "was"], 1),
    ("Choose the correct sentence:",
     ["I am looking forward to meeting you.",
      "I am looking forward to meet you.",
      "I look forward meet you."], 0),
]

# ════════════════════════════════════════════════════════════════
#  АНГЛИЙСКИЙ ЯЗЫК — 11 класс, Вариант B
# ════════════════════════════════════════════════════════════════
# Answer key: 1b,2b,3b,4c,5a,6a,7b,8c,9b,10a,11a,12a,13b,14a,15b,16a,17b,18b,19c,20a,21b,22b,23a,24a,25a
ENG_11_VB = [
    ("My father ___ at a bank.",
     ["work", "works", "working"], 1),
    ("They ___ dinner when I arrived.",
     ["had", "were having", "have"], 1),
    ("She has studied English ___ three years.",
     ["since", "for", "during"], 1),
    ("If we leave now, we ___ on time.",
     ["arrive", "arrived", "will arrive"], 2),
    ("This exercise is ___ than the last one.",
     ["easier", "easiest", "more easy"], 0),
    ("Do you know ___ she passed the test?",
     ["if", "because", "while"], 0),
    ("The classroom ___ last month.",
     ["painted", "was painted", "is painting"], 1),
    ("He enjoys ___ football with his friends.",
     ["play", "played", "playing"], 2),
    ("There isn't ___ milk in the fridge.",
     ["many", "much", "few"], 1),
    ("Which sentence is correct?",
     ["She doesn't watch TV often.",
      "She don't watch TV often.",
      "She not watches TV often."], 0),
    ("We ___ lunch at home yesterday.",
     ["had", "have had", "having"], 0),
    ("The opposite of 'expensive' is:",
     ["cheap", "large", "modern"], 0),
    ("Have you ever ___ a famous person?",
     ["meet", "met", "meeting"], 1),
    ("He thanked me ___ my help.",
     ["for", "on", "at"], 0),
    ("If I ___ a car, I would drive to work.",
     ["have", "had", "will have"], 1),
    ("The woman ___ teaches us English is very kind.",
     ["who", "which", "where"], 0),
    ("They ___ their project already.",
     ["finished", "have finished", "finishing"], 1),
    ("She is good ___ mathematics.",
     ["on", "at", "in"], 1),
    ("By the time I got to the station, the train ___.",
     ["left", "has left", "had left"], 2),
    ("Which word is closest in meaning to 'honest'?",
     ["truthful", "angry", "lazy"], 0),
    ("He told me that he ___ busy.",
     ["is", "was", "be"], 1),
    ("It was raining, ___ they continued playing outside.",
     ["because", "but", "so"], 1),
    ("This is the ___ movie I have ever seen.",
     ["most exciting", "more exciting", "exciting"], 0),
    ("Neither my parents nor my sister ___ at home.",
     ["is", "are", "was"], 0),
    ("Choose the correct sentence:",
     ["She is interested in learning languages.",
      "She is interested to learn languages.",
      "She interested in learning languages."], 0),
]


def load_variant(name, grade, eng_questions):
    variant, created = TestVariant.objects.get_or_create(
        name=name,
        defaults={'grade': grade, 'is_active': True}
    )
    if not created:
        variant.grade = grade
        variant.save(update_fields=['grade'])

    existing = Question.objects.filter(variant=variant, subject=eng).count()
    if existing >= len(eng_questions):
        print(f'  [{name}] Английский уже загружен ({existing} вопросов) — пропуск')
        return

    Question.objects.filter(variant=variant, subject=eng).delete()
    for i, (text, options, correct_idx) in enumerate(eng_questions, start=1):
        q = Question.objects.create(variant=variant, subject=eng, text=text, order=i)
        for j, opt_text in enumerate(options):
            AnswerOption.objects.create(question=q, text=opt_text, is_correct=(j == correct_idx))

    print(f'  [{name}] Английский загружен: {len(eng_questions)} вопросов')


print('Загрузка вариантов тестов...')
print()

print('9 класс:')
load_variant('9 класс — Вариант 1', '9', ENG_9_V1)
load_variant('9 класс — Вариант 2', '9', ENG_9_V2)

print()
print('11 класс:')
load_variant('11 класс — Вариант A', '11', ENG_11_VA)
load_variant('11 класс — Вариант B', '11', ENG_11_VB)

print()
print('=' * 55)
print('ВАЖНО: нужно добавить вручную:')
print('  • Русский язык (20 вопросов × 4 варианта)')
print('    PDF-сканы не читаются автоматически — добавьте')
print('    через Django admin или отдельный скрипт.')
print('  • Математика (20 вопросов × 4 варианта)')
print('    PDF-файлы не предоставлены.')
print('=' * 55)
print()
print('Готово!')
