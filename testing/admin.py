"""
Настройка Django Admin для удобной работы преподавателей с результатами тестирования.

Возможности:
  - Просмотр всех абитуриентов с баллами (общий + по предметам)
  - Детализация ответов: на какой вопрос ответил верно/неверно
  - Фильтрация по классу, варианту, дате
  - Поиск по ФИО и ПИН
  - Управление вариантами тестов и вопросами
"""
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.db.models import Prefetch

from .models import (
    Subject, TestVariant, Question, AnswerOption,
    Abiturient, TestResult, AbiturientAnswer
)


# ───────────────────────────────────────────────────────────────
#  Inline-классы для вложенного редактирования
# ───────────────────────────────────────────────────────────────

class AnswerOptionInline(admin.TabularInline):
    """4 варианта ответа внутри карточки вопроса."""
    model = AnswerOption
    extra = 4
    min_num = 4
    max_num = 4
    fields = ['text', 'is_correct']


class QuestionInline(admin.StackedInline):
    """Вопросы внутри варианта теста."""
    model = Question
    extra = 0
    show_change_link = True
    fields = ['subject', 'order', 'text']
    ordering = ['subject__order', 'order']


class AbiturientAnswerInline(admin.TabularInline):
    """Детализация ответов абитуриента — только для чтения."""
    model = AbiturientAnswer
    extra = 0
    can_delete = False
    ordering = ['question__subject__order', 'question__order']
    readonly_fields = [
        'get_subject', 'get_question_num', 'get_question_text',
        'get_selected_answer', 'get_correct_answer', 'get_status'
    ]
    fields = [
        'get_subject', 'get_question_num', 'get_question_text',
        'get_selected_answer', 'get_correct_answer', 'get_status'
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def get_subject(self, obj):
        return obj.question.subject.name
    get_subject.short_description = 'Предмет'

    def get_question_num(self, obj):
        return f'№{obj.question.order}'
    get_question_num.short_description = '№'

    def get_question_text(self, obj):
        return obj.question.text[:120]
    get_question_text.short_description = 'Вопрос'

    def get_selected_answer(self, obj):
        if obj.selected_option:
            return obj.selected_option.text[:80]
        return mark_safe('<em style="color:#94a3b8">Не ответил</em>')
    get_selected_answer.short_description = 'Ответ абитуриента'

    def get_correct_answer(self, obj):
        correct = obj.question.options.filter(is_correct=True).first()
        if correct:
            return correct.text[:80]
        return '—'
    get_correct_answer.short_description = 'Правильный ответ'

    def get_status(self, obj):
        if obj.is_correct:
            return mark_safe('<span style="color:#16a34a;font-weight:700;font-size:16px">✓</span>')
        if obj.selected_option is None:
            return mark_safe('<span style="color:#94a3b8;font-size:16px">—</span>')
        return mark_safe('<span style="color:#dc2626;font-weight:700;font-size:16px">✗</span>')
    get_status.short_description = 'Итог'


class TestResultInline(admin.StackedInline):
    """Итоговые баллы внутри карточки абитуриента."""
    model = TestResult
    extra = 0
    can_delete = False
    readonly_fields = [
        'total_score', 'english_score', 'math_score', 'russian_score', 'completed_at'
    ]
    verbose_name = 'Итоговые баллы'
    verbose_name_plural = 'Итоговые баллы'

    def has_add_permission(self, request, obj=None):
        return False


# ───────────────────────────────────────────────────────────────
#  ModelAdmin — основные модели
# ───────────────────────────────────────────────────────────────

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    ordering = ['order']


@admin.register(TestVariant)
class TestVariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'is_active', 'get_question_count', 'pdf_link', 'created_at']
    list_filter = ['is_active', 'grade']
    inlines = [QuestionInline]

    def get_question_count(self, obj):
        return obj.questions.count()
    get_question_count.short_description = 'Кол-во вопросов'

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank">📄 Скачать PDF</a>', obj.pdf_file.url
            )
        return '—'
    pdf_link.short_description = 'PDF-документ'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['get_variant', 'get_subject', 'order', 'short_text', 'has_correct_answer']
    list_filter = ['variant', 'subject']
    search_fields = ['text']
    inlines = [AnswerOptionInline]
    ordering = ['variant', 'subject__order', 'order']

    def get_variant(self, obj):
        return obj.variant.name
    get_variant.short_description = 'Вариант'
    get_variant.admin_order_field = 'variant__name'

    def get_subject(self, obj):
        return obj.subject.name
    get_subject.short_description = 'Предмет'
    get_subject.admin_order_field = 'subject__order'

    def short_text(self, obj):
        return obj.text[:90] + ('…' if len(obj.text) > 90 else '')
    short_text.short_description = 'Текст вопроса'

    def has_correct_answer(self, obj):
        ok = obj.options.filter(is_correct=True).exists()
        if ok:
            return mark_safe('<span style="color:green">✓ Есть</span>')
        return mark_safe('<span style="color:red">✗ Нет</span>')
    has_correct_answer.short_description = 'Верный ответ'


# ───────────────────────────────────────────────────────────────
#  Абитуриенты и результаты
# ───────────────────────────────────────────────────────────────

@admin.register(Abiturient)
class AbiturientAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'get_doc_number', 'school', 'grade', 'test_variant',
        'started_at', 'is_completed',
        'total_score_badge', 'english_badge', 'math_badge', 'russian_badge',
        'violations_badge',
    ]
    list_filter = ['grade', 'is_completed', 'test_variant', 'started_at']
    search_fields = ['last_name', 'first_name', 'middle_name', 'pin', 'birth_certificate', 'school']
    readonly_fields = ['started_at', 'finished_at', 'test_variant', 'is_completed', 'pin', 'birth_certificate', 'violations_count']
    ordering = ['-started_at']
    date_hierarchy = 'started_at'
    inlines = [TestResultInline, AbiturientAnswerInline]

    fieldsets = (
        ('Личные данные', {
            'fields': (('last_name', 'first_name', 'middle_name'),
                       ('birth_date', 'grade'), 'school', ('pin', 'birth_certificate'))
        }),
        ('Данные тестирования', {
            'fields': ('test_variant', 'is_completed', 'started_at', 'finished_at', 'violations_count')
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'ФИО'
    full_name.admin_order_field = 'last_name'

    def get_doc_number(self, obj):
        return obj.doc_number
    get_doc_number.short_description = 'Документ'

    def _get_score(self, obj, field):
        if hasattr(obj, 'result'):
            return getattr(obj.result, field)
        return None

    def _score_badge(self, score, max_score=20, color_thresholds=(14, 10)):
        if score is None:
            return mark_safe('<span style="color:#94a3b8">—</span>')
        high, mid = color_thresholds
        color = '#16a34a' if score >= high else ('#d97706' if score >= mid else '#dc2626')
        return format_html(
            '<strong style="color:{}">{}/{}</strong>', color, score, max_score
        )

    def total_score_badge(self, obj):
        s = self._get_score(obj, 'total_score')
        return self._score_badge(s, max_score=60, color_thresholds=(42, 30))
    total_score_badge.short_description = 'Итого'

    def english_badge(self, obj):
        return self._score_badge(self._get_score(obj, 'english_score'))
    english_badge.short_description = 'Англ.'

    def math_badge(self, obj):
        return self._score_badge(self._get_score(obj, 'math_score'))
    math_badge.short_description = 'Мат.'

    def russian_badge(self, obj):
        return self._score_badge(self._get_score(obj, 'russian_score'))
    russian_badge.short_description = 'Рус.'

    def violations_badge(self, obj):
        v = obj.violations_count
        if v == 0:
            return mark_safe('<span style="color:#16a34a;font-weight:600">0</span>')
        if v == 1:
            return mark_safe('<span style="color:#d97706;font-weight:700">⚠ 1</span>')
        return format_html('<span style="color:#dc2626;font-weight:700">🚫 {}</span>', v)
    violations_badge.short_description = 'Нарушения'
    violations_badge.admin_order_field = 'violations_count'

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('result', 'test_variant')
        )


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name', 'get_pin', 'get_school', 'get_grade',
        'get_variant',
        'total_score_badge', 'english_score', 'math_score', 'russian_score',
        'completed_at',
    ]
    list_filter = ['completed_at', 'abiturient__grade', 'abiturient__test_variant']
    search_fields = ['abiturient__last_name', 'abiturient__first_name', 'abiturient__pin']
    readonly_fields = [
        'abiturient', 'total_score', 'english_score', 'math_score',
        'russian_score', 'completed_at'
    ]
    ordering = ['-completed_at']
    date_hierarchy = 'completed_at'

    def get_full_name(self, obj):
        return obj.abiturient.full_name
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'abiturient__last_name'

    def get_pin(self, obj):
        return obj.abiturient.doc_number
    get_pin.short_description = 'Документ'

    def get_school(self, obj):
        return obj.abiturient.school
    get_school.short_description = 'Школа'

    def get_grade(self, obj):
        return obj.abiturient.get_grade_display()
    get_grade.short_description = 'Класс'
    get_grade.admin_order_field = 'abiturient__grade'

    def get_variant(self, obj):
        if obj.abiturient.test_variant:
            return obj.abiturient.test_variant.name
        return '—'
    get_variant.short_description = 'Вариант'

    def total_score_badge(self, obj):
        s = obj.total_score
        color = '#16a34a' if s >= 42 else ('#d97706' if s >= 30 else '#dc2626')
        return format_html('<strong style="color:{};font-size:15px">{}/60</strong>', color, s)
    total_score_badge.short_description = 'Итого'
    total_score_badge.admin_order_field = 'total_score'

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('abiturient', 'abiturient__test_variant')
        )
