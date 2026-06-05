"""
Загрузка вопросов по Математике (Алгебра) из PDF-файлов.
Вариант А1 → '9 класс — Вариант 1'
Вариант Б2 → '9 класс — Вариант 2'

Запуск: py load_math_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcollege.settings')
django.setup()

from testing.models import Subject, TestVariant, Question, AnswerOption

mat, _ = Subject.objects.get_or_create(name='Математика', defaults={'order': 2})

# ── SVG-графики для вопроса 15 (параболы) ──────────────────────────
# А: вершина (-2, 0) — y=(x+2)²   ← правильный ответ для А1
# Б: вершина (0, -2) — y=x²-2     ← отвлекатель
# В: вершина (0, 2), ветви вниз    ← отвлекатель
# Г: вершина (2, 0)  — y=(x-2)²   ← правильный ответ для Б2

SVG_A = (
    '<svg viewBox="0 0 160 100" width="150" height="95" xmlns="http://www.w3.org/2000/svg" '
    'style="display:block;margin:4px auto">'
    '<line x1="8" y1="75" x2="152" y2="75" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="150,72 157,75 150,78" fill="#555"/>'
    '<text x="154" y="79" font-size="10" fill="#555">x</text>'
    '<line x1="80" y1="8" x2="80" y2="92" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="77,10 80,3 83,10" fill="#555"/>'
    '<text x="83" y="12" font-size="10" fill="#555">y</text>'
    '<line x1="56" y1="72" x2="56" y2="78" stroke="#555" stroke-width="1"/>'
    '<text x="49" y="89" font-size="10" fill="#555">-2</text>'
    '<text x="82" y="89" font-size="10" fill="#555">0</text>'
    '<polyline points="32,27 44,63 56,75 68,63 80,27" '
    'stroke="#2563eb" stroke-width="2.2" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

SVG_B = (
    '<svg viewBox="0 0 160 100" width="150" height="95" xmlns="http://www.w3.org/2000/svg" '
    'style="display:block;margin:4px auto">'
    '<line x1="8" y1="60" x2="152" y2="60" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="150,57 157,60 150,63" fill="#555"/>'
    '<text x="154" y="64" font-size="10" fill="#555">x</text>'
    '<line x1="80" y1="5" x2="80" y2="95" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="77,7 80,0 83,7" fill="#555"/>'
    '<text x="83" y="12" font-size="10" fill="#555">y</text>'
    '<line x1="77" y1="76" x2="83" y2="76" stroke="#555" stroke-width="1"/>'
    '<text x="64" y="80" font-size="10" fill="#555">-2</text>'
    '<text x="82" y="74" font-size="10" fill="#555">0</text>'
    '<polyline points="56,4 64,44 72,68 80,76 88,68 96,44 104,4" '
    'stroke="#2563eb" stroke-width="2.2" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

SVG_C = (
    '<svg viewBox="0 0 160 100" width="150" height="95" xmlns="http://www.w3.org/2000/svg" '
    'style="display:block;margin:4px auto">'
    '<line x1="8" y1="75" x2="152" y2="75" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="150,72 157,75 150,78" fill="#555"/>'
    '<text x="154" y="79" font-size="10" fill="#555">x</text>'
    '<line x1="80" y1="8" x2="80" y2="92" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="77,10 80,3 83,10" fill="#555"/>'
    '<text x="83" y="12" font-size="10" fill="#555">y</text>'
    '<line x1="77" y1="55" x2="83" y2="55" stroke="#555" stroke-width="1"/>'
    '<text x="85" y="59" font-size="10" fill="#555">2</text>'
    '<text x="82" y="89" font-size="10" fill="#555">0</text>'
    '<polyline points="60,95 70,65 80,55 90,65 100,95" '
    'stroke="#2563eb" stroke-width="2.2" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

SVG_D = (
    '<svg viewBox="0 0 160 100" width="150" height="95" xmlns="http://www.w3.org/2000/svg" '
    'style="display:block;margin:4px auto">'
    '<line x1="8" y1="75" x2="152" y2="75" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="150,72 157,75 150,78" fill="#555"/>'
    '<text x="154" y="79" font-size="10" fill="#555">x</text>'
    '<line x1="80" y1="8" x2="80" y2="92" stroke="#555" stroke-width="1.5"/>'
    '<polygon points="77,10 80,3 83,10" fill="#555"/>'
    '<text x="83" y="12" font-size="10" fill="#555">y</text>'
    '<line x1="104" y1="72" x2="104" y2="78" stroke="#555" stroke-width="1"/>'
    '<text x="100" y="89" font-size="10" fill="#555">2</text>'
    '<text x="82" y="89" font-size="10" fill="#555">0</text>'
    '<polyline points="80,27 92,63 104,75 116,63 128,27" '
    'stroke="#2563eb" stroke-width="2.2" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

# ════════════════════════════════════════════════════════════════════
#  АЛГЕБРА — 9 класс, Вариант А1
#  Ключ: 1В 2Г 3В 4Г 5Г 6Г 7Б 8Г 9В 10Б 11А 12В 13Б 14Б 15А 16В 17В 18Б 19В 20Б
#  Формат: (текст_вопроса, [опция_A, Б, В, Г], индекс_правильного_0)
# ════════════════════════════════════════════════════════════════════
MAT_9_A1 = [
    # 1 → В (index 2)
    ("Вычислите: $-12-15:(-3)=$",
     ["$9$", "$-9$", "$-7$", "$7$"],
     2),

    # 2 → Г (index 3)
    (r"Вычислите: $2\dfrac{4}{7}+2{,}4$",
     [r"$4\dfrac{8}{17}$", r"$4\dfrac{34}{35}$", r"$4\dfrac{8}{10}$", r"$4\dfrac{8}{35}$"],
     3),

    # 3 → В (index 2)
    (r"Упростите выражение: $\dfrac{(a^3)^8 \cdot a^3}{a^{20}}$",
     [r"$a^7$", r"$a^6$", r"$a^{-3}$", r"$a^{13}$"],
     2),

    # 4 → Г (index 3)
    (r"Найдите значение выражения: $\sqrt{81}-2\sqrt[4]{81}$",
     ["$15$", "$6$", "$3$", "$-9$"],
     3),

    # 5 → Г (index 3)
    (r"Вычислите: $2\cos\dfrac{\pi}{6}\cdot\operatorname{ctg}\dfrac{\pi}{3}-\sin\dfrac{\pi}{2}$",
     ["$2$", "$0$", r"$-0{,}5$", r"$\dfrac{\sqrt{3}}{2}-1$"],
     3),

    # 6 → Г (index 3)
    (r"Сократите дробь при допустимых значениях $a$: $\dfrac{25-a^2}{15-3a}$",
     [r"$\dfrac{a+5}{3}$", r"$\dfrac{5-a}{3}$", r"$\dfrac{5+a}{5}$", r"$\dfrac{5-a}{3-3a}$"],
     3),

    # 7 → Б (index 1)
    ("Решите уравнение: $(-3)^2+(-3)t=24$",
     ["$-11$", "$-5$", "$-8$", "$-10$"],
     1),

    # 8 → Г (index 3)
    (r"Решите систему уравнений: $\begin{cases}2x-3y=4\\6x+3y=12\end{cases}$",
     [r"$(5;\,2)$", r"$(0;\,4)$", r"$(2;\,0)$", r"$(2;\,1)$"],
     3),

    # 9 → В (index 2)
    ("Решите неравенство: $-2x+12>3x-3$",
     [r"$[3;\,+\infty)$", r"$(3;\,+\infty)$", r"$(-\infty;\,3)$", r"$(-\infty;\,3]$"],
     2),

    # 10 → Б (index 1)
    ("24 кг кокса заменяют 40 кг каменного угля. Сколько килограммов каменного угля заменяют 420 кг кокса?",
     ["$252$", "$700$", "$400$", "$580$"],
     1),

    # 11 → А (index 0)
    (r"Разложите квадратный трёхчлен на множители: $x^2-5x+6$",
     [r"$(x-3)(x-2)$", r"$(x+3)(x+2)$", r"$(x-3)(x+2)$", r"$(x+3)(x-2)$"],
     0),

    # 12 → В (index 2)
    ("Укажите наибольшее целое решение неравенства: $(x-2)(x+3)<0$",
     ["$-4$", "$-2$", "$1$", r"$+\infty$"],
     2),

    # 13 → Б (index 1)
    ("Если $a>b$, выберите верное неравенство.",
     [r"$a-b<0$", r"$2a-2b>0$", r"$\dfrac{1}{a}>\dfrac{1}{b}$", r"$3a<3b$"],
     1),

    # 14 → Б (index 1)
    (r"Вычислите: $(\sqrt{3}-\sqrt{2})^2=$",
     [r"$1-2\sqrt{6}$", r"$5-2\sqrt{6}$", "$1$", r"$1-\sqrt{6}$"],
     1),

    # 15 → А (index 0)
    ("На каком из рисунков изображён график функции $y=(x+2)^2$?",
     [SVG_A, SVG_B, SVG_C, SVG_D],
     0),

    # 16 → В (index 2)
    (r"Найдите область определения функции: $y=\dfrac{x-2}{x^2-1}$",
     [r"$(-\infty;\,-1)\cup(1;\,+\infty)$",
      r"$(-1;\,1)$",
      r"$(-\infty;\,-1)\cup(-1;\,1)\cup(1;\,+\infty)$",
      r"$(-\infty;\,-1]\cup[-1;\,1]\cup[1;\,+\infty)$"],
     2),

    # 17 → В (index 2)
    (r"Вычислите $f\!\left(-\dfrac{1}{2}\right)$, если $f(x)=1+\dfrac{1}{x}$",
     [r"$-1\dfrac{1}{2}$", "$-1$", "$1$", r"$1\dfrac{1}{2}$"],
     2),

    # 18 → Б (index 1)
    (r"В арифметической прогрессии $(a_n)$: $a_1=5$, $a_3=8$. Найдите разность прогрессии.",
     ["$1$", r"$1{,}5$", r"$2{,}5$", "$3$"],
     1),

    # 19 → В (index 2)
    ("Какая из точек принадлежит графику функции $f(x)=-3x+4$?",
     [r"$(5;\,9)$", r"$(-3;\,5)$", r"$(3;\,-5)$", r"$(-2;\,40)$"],
     2),

    # 20 → Б (index 1)
    ("Из пенала, в котором 5 простых и 15 цветных карандашей, достают один карандаш. "
     "Какова вероятность того, что этот карандаш окажется простым?",
     [r"$\dfrac{1}{3}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{5}$", r"$\dfrac{3}{4}$"],
     1),
]

# ════════════════════════════════════════════════════════════════════
#  АЛГЕБРА — 9 класс, Вариант Б2
#  Ключ: 1А 2Г 3А 4Б 5А 6Б 7В 8В 9В 10Б 11В 12Б 13Б 14Б 15Г 16В 17Г 18В 19Б 20Г
# ════════════════════════════════════════════════════════════════════
MAT_9_B2 = [
    # 1 → А (index 0)
    ("Вычислите: $-12-48:(-6)=$",
     ["$4$", "$10$", "$-10$", "$-4$"],
     0),

    # 2 → Г (index 3)
    (r"Вычислите: $1\dfrac{2}{3}+3{,}2$",
     [r"$4\dfrac{4}{15}$", r"$4\dfrac{4}{10}$", r"$4{,}4$", r"$4\dfrac{13}{15}$"],
     3),

    # 3 → А (index 0)
    (r"Упростите выражение: $\dfrac{(a^4)^3 \cdot a^4}{a^{16}}$",
     ["$1$", r"$a^{-5}$", r"$a^{32}$", r"$a^{12}$"],
     0),

    # 4 → Б (index 1)
    (r"Найдите значение выражения: $\sqrt{16}-2\sqrt[4]{16}$",
     ["$-8$", "$-4$", "$0$", "$12$"],
     1),

    # 5 → А (index 0)
    (r"Вычислите: $2\sin\dfrac{\pi}{3}\cdot\operatorname{tg}\dfrac{\pi}{6}-\cos\pi$",
     ["$2$", "$0$", r"$-0{,}5$", r"$\dfrac{\sqrt{3}}{3}+1$"],
     0),

    # 6 → Б (index 1)
    (r"Сократите дробь при допустимых значениях $a$: $\dfrac{3a-12}{a^2-16}$",
     [r"$\dfrac{3}{a-4}$", r"$\dfrac{3}{a+4}$", r"$\dfrac{4}{a-4}$", r"$-\dfrac{1}{a-4}$"],
     1),

    # 7 → В (index 2)
    (r"Решите уравнение: $\dfrac{2x-1}{3}=7$",
     ["$1$", "$21$", "$11$", "$33$"],
     2),

    # 8 → В (index 2)
    (r"Решите систему уравнений: $\begin{cases}3x-2y=6\\5x+2y=10\end{cases}$",
     [r"$(4;\,3)$", r"$(0;\,-3)$", r"$(2;\,0)$", r"$(0;\,5)$"],
     2),

    # 9 → В (index 2)
    ("Решите неравенство: $-3x+12>5x-4$",
     [r"$[2;\,+\infty)$", r"$(2;\,+\infty)$", r"$(-\infty;\,2)$", r"$(-\infty;\,2]$"],
     2),

    # 10 → Б (index 1)
    ("За 4 ч токарь изготовит 34 детали. Сколько деталей он изготовит за 14 ч "
     "при той же производительности?",
     ["$44$", "$119$", "$340$", "$112$"],
     1),

    # 11 → В (index 2)
    (r"Разложите квадратный трёхчлен на множители: $x^2+5x-24$",
     [r"$(x-3)(x-8)$", r"$(x+3)(x+8)$", r"$(x-3)(x+8)$", r"$(x+3)(x-8)$"],
     2),

    # 12 → Б (index 1)
    ("Укажите наибольшее целое решение неравенства: $(x+2)(x-3)<0$",
     ["$4$", "$2$", "$-1$", r"$+\infty$"],
     1),

    # 13 → Б (index 1)
    ("Если $a>b$, выберите верное неравенство.",
     [r"$b-a>0$", r"$-2a+2b<0$", r"$\dfrac{1}{a}>\dfrac{1}{b}$", r"$3a<3b$"],
     1),

    # 14 → Б (index 1)
    (r"Вычислите: $C_n=(-1)^n\cdot n+(-1)^{n+1}\cdot(n+1)$",
     ["$201$", "$-1$", "$100$", "$1$"],
     1),

    # 15 → Г (index 3)
    ("На каком из рисунков изображён график функции $y=(x-2)^2$?",
     [SVG_A, SVG_B, SVG_C, SVG_D],
     3),

    # 16 → В (index 2)
    (r"Найдите область определения функции: $y=\dfrac{x-3}{x^2-4}$",
     [r"$(-\infty;\,-2)\cup(2;\,+\infty)$",
      r"$(-2;\,2)$",
      r"$(-\infty;\,-2)\cup(-2;\,2)\cup(2;\,+\infty)$",
      r"$(-\infty;\,-2]\cup[-2;\,2]\cup[2;\,+\infty)$"],
     2),

    # 17 → Г (index 3)
    (r"Вычислите $f\!\left(-\dfrac{1}{3}\right)$, если $f(x)=2+\dfrac{2}{x}$",
     ["$8$", r"$2\dfrac{2}{3}$", r"$-1\dfrac{1}{3}$", "$-4$"],
     3),

    # 18 → В (index 2)
    (r"В арифметической прогрессии $(a_n)$: $a_1=5$, $a_3=9$. Найдите разность прогрессии.",
     ["$1$", r"$1{,}5$", "$2$", "$4$"],
     2),

    # 19 → Б (index 1)
    ("Какая из точек принадлежит графику функции $f(x)=-4x+3$?",
     [r"$(-1;\,1)$", r"$(2;\,-5)$", r"$(-5;\,17)$", r"$(1;\,1)$"],
     1),

    # 20 → Г (index 3)
    ("Из 30 книг на полке 5 учебников, остальные — художественные произведения. "
     "Наугад берут одну книгу. Какова вероятность того, что она не окажется учебником?",
     [r"$\dfrac{1}{6}$", r"$\dfrac{1}{5}$", r"$\dfrac{3}{5}$", r"$\dfrac{5}{6}$"],
     3),
]


# ── Загрузчик ──────────────────────────────────────────────────────
def add_math_to_variant(variant_name, questions):
    try:
        variant = TestVariant.objects.get(name=variant_name)
    except TestVariant.DoesNotExist:
        print(f'  ОШИБКА: вариант "{variant_name}" не найден. '
              'Сначала запустите load_real_data.py')
        return

    existing = Question.objects.filter(variant=variant, subject=mat).count()
    if existing >= len(questions):
        print(f'  [{variant_name}] Математика уже загружена ({existing} вопр.) — пропуск')
        return

    Question.objects.filter(variant=variant, subject=mat).delete()
    for i, (text, options, correct_idx) in enumerate(questions, start=1):
        q = Question.objects.create(variant=variant, subject=mat, text=text, order=i)
        for j, opt_text in enumerate(options):
            AnswerOption.objects.create(
                question=q, text=opt_text, is_correct=(j == correct_idx)
            )

    print(f'  [{variant_name}] Математика загружена: {len(questions)} вопросов')


print('Загрузка Математики...')
print()
print('9 класс:')
add_math_to_variant('9 класс — Вариант 1', MAT_9_A1)
add_math_to_variant('9 класс — Вариант 2', MAT_9_B2)
print()
print('Готово!')
