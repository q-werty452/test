"""
Логика обработки запросов системы тестирования.

Маршрут пользователя:
  /  (register_view)  →  /test/ (test_view)  →  POST /test/submit/ (submit_test_view)  →  /complete/ (complete_view)
"""
import json
import time
import random

from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.db import transaction

from .models import TestVariant, Question, AnswerOption, Abiturient, TestResult, AbiturientAnswer, Subject, SiteSettings
from .forms import AbiturientRegistrationForm

# Продолжительность теста в секундах (берём из settings, по умолчанию 90 минут)
TEST_DURATION = getattr(settings, 'TEST_DURATION_SECONDS', 5400)


def _build_subject_counts_json():
    """Возвращает JSON со структурой вопросов по предметам для каждого класса."""
    subject_counts = {}
    for grade in ['9', '11']:
        variant = TestVariant.objects.filter(grade=grade, is_active=True).first()
        if variant:
            counts = {}
            for subj in Subject.objects.order_by('order'):
                cnt = Question.objects.filter(variant=variant, subject=subj).count()
                if cnt:
                    counts[subj.name] = cnt
            counts['total'] = sum(counts.values())
            subject_counts[grade] = counts
    return json.dumps(subject_counts, ensure_ascii=False)


def register_view(request):
    """
    Страница регистрации абитуриента.

    GET  — отображает форму регистрации.
    POST — валидирует форму, выбирает случайный вариант теста,
           сохраняет абитуриента в БД и записывает сессию.
    """
    # Если у пользователя уже есть активная сессия — перенаправляем
    if request.session.get('abiturient_id'):
        abiturient_id = request.session['abiturient_id']
        try:
            ab = Abiturient.objects.get(id=abiturient_id)
            if ab.is_completed:
                return redirect('complete')
            return redirect('test')
        except Abiturient.DoesNotExist:
            request.session.flush()

    site = SiteSettings.get()
    code_required = bool(site.access_code)
    code_error = None

    if request.method == 'POST':
        # Проверка кода доступа (если задан)
        if code_required:
            entered = request.POST.get('access_code', '').strip()
            if entered.upper() != site.access_code.upper():
                code_error = 'Неверный код доступа. Уточните у преподавателя.'
                form = AbiturientRegistrationForm(request.POST)
                return render(request, 'testing/register.html', {
                    'form': form,
                    'code_required': code_required,
                    'code_error': code_error,
                    'subject_counts_json': _build_subject_counts_json(),
                })

        form = AbiturientRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем абитуриента (без записи в БД) чтобы получить grade
            abiturient = form.save(commit=False)

            # Получаем активные варианты для класса абитуриента
            active_variants = list(
                TestVariant.objects.filter(is_active=True, grade=abiturient.grade)
            )
            if not active_variants:
                form.add_error(None,
                    f'Нет доступных вариантов теста для {abiturient.get_grade_display()}. '
                    'Пожалуйста, обратитесь к администратору.'
                )
                return render(request, 'testing/register.html', {
                    'form': form,
                    'subject_counts_json': _build_subject_counts_json(),
                })

            # Случайно выбираем вариант (согласно ТЗ — random.choice)
            chosen_variant = random.choice(active_variants)
            abiturient.test_variant = chosen_variant
            abiturient.save()

            # Записываем данные в сессию
            request.session['abiturient_id'] = abiturient.id
            request.session['variant_id'] = chosen_variant.id
            # Unix-timestamp старта — используется для расчёта оставшегося времени
            request.session['test_start_time'] = int(time.time())
            request.session.modified = True

            return redirect('test')
    else:
        form = AbiturientRegistrationForm()

    return render(request, 'testing/register.html', {
        'form': form,
        'code_required': code_required,
        'code_error': code_error,
        'subject_counts_json': _build_subject_counts_json(),
    })


@never_cache
def test_view(request):
    """
    Страница прохождения теста.

    Загружает вопросы выбранного варианта, НЕ включая поле `is_correct` —
    правильные ответы никогда не передаются на фронтенд.
    Рассчитывает оставшееся время и передаёт его в шаблон для JS-таймера.
    """
    abiturient_id = request.session.get('abiturient_id')
    variant_id = request.session.get('variant_id')
    start_time = request.session.get('test_start_time')

    # Нет активной сессии — на страницу регистрации
    if not all([abiturient_id, variant_id, start_time]):
        return redirect('register')

    try:
        abiturient = Abiturient.objects.get(id=abiturient_id)
    except Abiturient.DoesNotExist:
        request.session.flush()
        return redirect('register')

    # Тест уже завершён
    if abiturient.is_completed:
        return redirect('complete')

    # Рассчитываем оставшееся время
    elapsed = int(time.time()) - start_time
    remaining_seconds = max(0, TEST_DURATION - elapsed)

    # Загружаем предметы с вопросами для данного варианта.
    # БЕЗОПАСНОСТЬ: values() передаёт только id и text — is_correct исключён.
    variant = get_object_or_404(TestVariant, id=variant_id)
    subjects = Subject.objects.filter(
        questions__variant=variant
    ).distinct().order_by('order')

    subjects_data = []
    for subject in subjects:
        questions_qs = (
            Question.objects
            .filter(variant=variant, subject=subject)
            .prefetch_related('options')
            .order_by('order')
        )

        questions_data = []
        for q in questions_qs:
            # Формируем список вариантов ответа с буквой (A/B/C/D)
            options_data = []
            for idx, opt in enumerate(q.options.all()):
                options_data.append({
                    'id': opt.id,
                    'text': opt.text,
                    'letter': chr(65 + idx),  # A, B, C, D
                })
            questions_data.append({
                'id': q.id,
                'text': q.text,
                'order': q.order,
                'options': options_data,
            })

        # CSS-класс блока для окраски по предмету
        name_lower = subject.name.lower()
        if 'англ' in name_lower or 'english' in name_lower:
            css_class = 'english'
        elif 'мат' in name_lower or 'math' in name_lower:
            css_class = 'math'
        elif 'рус' in name_lower or 'russian' in name_lower:
            css_class = 'russian'
        else:
            css_class = 'default'

        subjects_data.append({
            'subject': subject,
            'questions': questions_data,
            'css_class': css_class,
        })

    context = {
        'abiturient': abiturient,
        'subjects_data': subjects_data,
        'remaining_seconds': remaining_seconds,
        'variant': variant,
        'total_questions': sum(len(s['questions']) for s in subjects_data),
    }
    return render(request, 'testing/test.html', context)


@require_http_methods(['POST'])
@transaction.atomic
def submit_test_view(request):
    """
    Приём и обработка ответов абитуриента.

    1. Извлекаем ответы из POST-данных.
    2. Сравниваем с правильными ответами в БД.
    3. Рассчитываем баллы по каждому предмету и суммарный балл.
    4. Сохраняем TestResult и детальные AbiturientAnswer.
    5. Помечаем тест как завершённый, очищаем сессию.
    """
    abiturient_id = request.session.get('abiturient_id')
    variant_id = request.session.get('variant_id')

    if not abiturient_id:
        return redirect('register')

    try:
        # select_for_update — блокируем строку для защиты от двойного submit
        abiturient = Abiturient.objects.select_for_update().get(id=abiturient_id)
    except Abiturient.DoesNotExist:
        return redirect('register')

    # Защита от повторной отправки (например, двойной клик или повторный POST)
    if abiturient.is_completed:
        return redirect('complete')

    # Получаем все вопросы этого варианта с информацией о предмете
    questions = (
        Question.objects
        .filter(variant_id=variant_id)
        .select_related('subject')
        .prefetch_related('options')
    )

    # Словарь для накопления баллов по предметам: {subject_id: score}
    subject_scores = {}
    # Список объектов для массовой вставки
    abiturient_answers = []

    for question in questions:
        subj_id = question.subject_id
        if subj_id not in subject_scores:
            subject_scores[subj_id] = {'subject': question.subject, 'score': 0}

        # Получаем выбранный вариант ответа из POST
        raw_option_id = request.POST.get(f'answer_{question.id}')
        selected_option = None
        is_correct = False

        if raw_option_id:
            try:
                selected_option = AnswerOption.objects.get(
                    id=int(raw_option_id),
                    question=question  # дополнительная проверка принадлежности
                )
                is_correct = selected_option.is_correct
                if is_correct:
                    subject_scores[subj_id]['score'] += 2
            except (AnswerOption.DoesNotExist, ValueError, TypeError):
                # Некорректный ID или вариант не принадлежит этому вопросу
                pass

        abiturient_answers.append(AbiturientAnswer(
            abiturient=abiturient,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
        ))

    # Массово сохраняем все ответы одним запросом
    AbiturientAnswer.objects.bulk_create(
        abiturient_answers,
        ignore_conflicts=True  # безопасно при повторном вызове
    )

    # Распределяем баллы по трём предметам на основе названия
    english_score = math_score = russian_score = 0

    for subj_id, data in subject_scores.items():
        name_lower = data['subject'].name.lower()
        score = data['score']
        if 'англ' in name_lower or 'english' in name_lower:
            english_score = score
        elif 'мат' in name_lower or 'math' in name_lower:
            math_score = score
        elif 'рус' in name_lower or 'russian' in name_lower:
            russian_score = score

    total_score = english_score + math_score + russian_score

    # Сохраняем итоговый результат
    TestResult.objects.create(
        abiturient=abiturient,
        total_score=total_score,
        english_score=english_score,
        math_score=math_score,
        russian_score=russian_score,
    )

    # Помечаем тест завершённым
    abiturient.is_completed = True
    abiturient.finished_at = timezone.now()
    abiturient.save(update_fields=['is_completed', 'finished_at'])

    # Очищаем сессию — абитуриент не сможет вернуться к тесту
    request.session.flush()

    return redirect('complete')


@never_cache
def complete_view(request):
    """Страница подтверждения завершения теста. Результаты НЕ показываются."""
    request.session.flush()
    return render(request, 'testing/complete.html')


@require_http_methods(['POST'])
def log_violation_view(request):
    """
    Фиксирует нарушение антишпаргалочной системы (смена вкладки, потеря фокуса и т.д.).
    Инкрементирует счётчик нарушений у абитуриента в БД.
    """
    abiturient_id = request.session.get('abiturient_id')
    if not abiturient_id:
        return JsonResponse({'ok': False}, status=403)

    try:
        updated = Abiturient.objects.filter(
            id=abiturient_id, is_completed=False
        ).update(violations_count=F('violations_count') + 1)

        if not updated:
            return JsonResponse({'ok': False}, status=404)

        ab = Abiturient.objects.values('violations_count').get(id=abiturient_id)
        return JsonResponse({'ok': True, 'violations': ab['violations_count']})
    except Exception:
        # Если БД занята (submit выполняется одновременно) — просто игнорируем
        return JsonResponse({'ok': False}, status=503)
