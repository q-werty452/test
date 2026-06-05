"""
Скрипт для создания демо-данных: предметы, вариант теста, 60 вопросов.
Запуск: py manage.py shell < create_demo_data.py
  или:  py create_demo_data.py  (из директории проекта с настроенным DJANGO_SETTINGS_MODULE)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcollege.settings')
django.setup()

from testing.models import Subject, TestVariant, Question, AnswerOption

# --- Предметы ---
eng, _ = Subject.objects.get_or_create(name='Английский язык', defaults={'order': 1})
mat, _ = Subject.objects.get_or_create(name='Математика',      defaults={'order': 2})
rus, _ = Subject.objects.get_or_create(name='Русский язык',    defaults={'order': 3})
print('Subjects OK')

# --- Вариант 1 ---
v1, _ = TestVariant.objects.get_or_create(name='Вариант №1', defaults={'is_active': True})

if Question.objects.filter(variant=v1).count() >= 60:
    print(f'Data already exists: {Question.objects.filter(variant=v1).count()} questions')
else:
    # Очищаем на случай частичного создания
    Question.objects.filter(variant=v1).delete()

    # (предмет, текст вопроса, [варианты A,B,C,D], индекс правильного 0-based)
    demo = [
        # ─── АНГЛИЙСКИЙ ЯЗЫК (20 вопросов) ───
        (eng, 'She ___ to school every day.', ['go', 'goes', 'going', 'gone'], 1),
        (eng, 'He is ___ than his brother.', ['tall', 'taller', 'tallest', 'more tall'], 1),
        (eng, 'Which sentence is correct?', ['I have saw him', 'I seen him', 'I have seen him', 'I seeing him'], 2),
        (eng, 'The plural of "child" is:', ['childs', 'childes', 'children', 'childrens'], 2),
        (eng, 'What does "enormous" mean?', ['tiny', 'very large', 'ordinary', 'expensive'], 1),
        (eng, 'She is good ___ math.', ['in', 'at', 'on', 'for'], 1),
        (eng, 'Which word is a noun?', ['quickly', 'beautiful', 'freedom', 'run'], 2),
        (eng, 'The past tense of "write" is:', ['writed', 'wrote', 'writ', 'written'], 1),
        (eng, 'If it rains, I ___ stay at home.', ['would', 'will', 'shall', 'can'], 1),
        (eng, 'What is the correct question?', ['What he is doing?', 'What is he doing?', 'What doing is he?', 'He what is doing?'], 1),
        (eng, 'Antonym of "ancient":', ['old', 'modern', 'large', 'slow'], 1),
        (eng, 'I ___ my homework yet.', ['have not done', 'did not do', 'not done', 'do not done'], 0),
        (eng, '"Beautiful" is a:', ['noun', 'verb', 'adjective', 'adverb'], 2),
        (eng, 'She speaks English very ___', ['good', 'goodly', 'well', 'better'], 2),
        (eng, '"He has been studying for 2 hours" — which tense?', ['Past Simple', 'Present Perfect', 'Present Perfect Continuous', 'Past Continuous'], 2),
        (eng, 'Opposite of "success":', ['victory', 'achievement', 'failure', 'progress'], 2),
        (eng, 'Passive: "Someone built this house in 1900":', ['This house built in 1900', 'This house was built in 1900', 'This house has built in 1900', 'This house is built in 1900'], 1),
        (eng, 'She asked me ___ I was going.', ['that', 'what', 'where', 'which'], 2),
        (eng, 'Correct spelling:', ['recieve', 'receive', 'receve', 'recieeve'], 1),
        (eng, 'How many vowels in "education"?', ['3', '4', '5', '6'], 2),
        # ─── МАТЕМАТИКА (20 вопросов) ───
        (mat, '2 в степени 10 равно:', ['512', '1000', '1024', '2048'], 2),
        (mat, '3x + 7 = 22. x =', ['3', '4', '5', '6'], 2),
        (mat, 'Площадь круга радиусом 5 (ответ в виде числа × π):', ['25π', '10π', '5π', '50π'], 0),
        (mat, '√144 =', ['11', '12', '13', '14'], 1),
        (mat, 'a=3, b=4. a² + b² =', ['25', '49', '12', '7'], 0),
        (mat, 'В прямоугольном треугольнике один острый угол 30°. Второй острый угол:', ['30°', '45°', '60°', '90°'], 2),
        (mat, '15% от 200 равно:', ['20', '25', '30', '35'], 2),
        (mat, 'Упростите: (x+2)(x-2) =', ['x²+4', 'x²-4', 'x²-2', 'x²+2'], 1),
        (mat, 'Сумма углов треугольника равна:', ['90°', '180°', '270°', '360°'], 1),
        (mat, '|−7| + |3| =', ['4', '10', '-4', '-10'], 1),
        (mat, 'НОД(12, 18) =', ['3', '6', '9', '12'], 1),
        (mat, '2³ × 2⁴ =', ['2⁷', '2¹²', '4⁷', '4¹²'], 0),
        (mat, 'Периметр квадрата со стороной 7 см:', ['28 см', '21 см', '14 см', '49 см'], 0),
        (mat, 'Какое число следует за −3 на числовой оси?', ['−4', '−2', '0', '3'], 1),
        (mat, 'log₂(8) =', ['2', '3', '4', '8'], 1),
        (mat, 'Производная x³ равна:', ['3x', 'x²', '3x²', '3x⁴'], 2),
        (mat, '5x − 3 = 2x + 9. x =', ['2', '3', '4', '6'], 2),
        (mat, 'Прямоугольник: длина 8 см, ширина 5 см. Площадь =', ['13 см²', '26 см²', '40 см²', '80 см²'], 2),
        (mat, 'sin 90° =', ['0', '0,5', '1', '√2/2'], 2),
        (mat, 'Какое число является простым?', ['9', '15', '17', '21'], 2),
        # ─── РУССКИЙ ЯЗЫК (20 вопросов) ───
        (rus, 'Слово с непроверяемой безударной гласной в корне:', ['вода', 'собака', 'земля', 'гора'], 1),
        (rus, 'В каком слове пишется «нн»?', ['кожаный', 'деревянный', 'стеклянный', 'оловянный'], 1),
        (rus, 'Укажите сложносочинённое предложение:', ['Я читал, пока шёл дождь.', 'Дождь прошёл, и на улице стало свежо.', 'Из-за дождя я остался дома.', 'Я люблю дождь.'], 1),
        (rus, 'Слово с приставкой «пре-»:', ['преграда', 'предел', 'предлог', 'предок'], 0),
        (rus, 'Все слова пишутся с «не» раздельно:', ['Небольшой, нелёгкий', 'Негромкий, небольшой', 'Не громкий, не большой', 'Нелёгкий, недалёкий'], 2),
        (rus, 'Укажите числительное:', ['тройка', 'третий', 'втроём', 'трое'], 3),
        (rus, 'Синоним к слову «храбрый»:', ['злой', 'смелый', 'добрый', 'умный'], 1),
        (rus, 'Предложение с деепричастным оборотом:', ['Книга, лежавшая на столе, была интересной.', 'Прочитав книгу, я лёг спать.', 'Я читал книгу весь вечер.', 'Книга оказалась интересной.'], 1),
        (rus, 'В каком слове буква «е» обозначает два звука?', ['ель', 'мел', 'сел', 'пел'], 0),
        (rus, 'Нужна ли запятая: «Солнце светило ярко и небо было голубым»?', ['Да, перед «и»', 'Да, после «ярко»', 'Запятые не нужны', 'Да, после «светило»'], 0),
        (rus, 'Антоним к слову «рассвет»:', ['утро', 'полдень', 'закат', 'ночь'], 2),
        (rus, 'Слово с чередующейся гласной в корне:', ['бежать', 'загорать', 'писать', 'думать'], 1),
        (rus, 'Глагол несовершенного вида:', ['написать', 'прочитать', 'писать', 'сделать'], 2),
        (rus, 'В каком слове ударение на первом слоге?', ['звонит', 'начать', 'досуг', 'искра'], 3),
        (rus, 'Правильное написание:', ['компания друзей', 'кампания друзей', 'кОмпания друзей', 'кАмпания друзей'], 0),
        (rus, 'Тип речи «описание природы»:', ['повествование', 'описание', 'рассуждение', 'объяснение'], 1),
        (rus, 'Существительное 3-го склонения:', ['стол', 'мать', 'конь', 'окно'], 1),
        (rus, 'Сложноподчинённое предложение:', ['Я пошёл домой и лёг спать.', 'Он улыбнулся, но ничего не сказал.', 'Когда наступит весна, расцветут цветы.', 'Светло и тихо.'], 2),
        (rus, 'В каком предложении есть однородные члены?', ['Дети играли во дворе.', 'Мама пела и танцевала.', 'Я лёг спать рано.', 'Небо потемнело.'], 1),
        (rus, 'Морфема «-ость» является:', ['корнем', 'приставкой', 'суффиксом', 'окончанием'], 2),
    ]

    created = 0
    for subj, text, opts, correct_idx in demo:
        order = Question.objects.filter(variant=v1, subject=subj).count() + 1
        q = Question.objects.create(variant=v1, subject=subj, text=text, order=order)
        for i, opt_text in enumerate(opts):
            AnswerOption.objects.create(question=q, text=opt_text, is_correct=(i == correct_idx))
        created += 1

    print(f'Created {created} questions for "{v1.name}"')
    print(f'  English: {Question.objects.filter(variant=v1, subject=eng).count()}')
    print(f'  Math:    {Question.objects.filter(variant=v1, subject=mat).count()}')
    print(f'  Russian: {Question.objects.filter(variant=v1, subject=rus).count()}')

print('Done!')
