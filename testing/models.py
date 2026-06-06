"""
Модели базы данных для системы тестирования абитуриентов IT COLLEGE.

Схема связей:
  TestVariant ──< Question ──< AnswerOption
  TestVariant <── Abiturient ──> TestResult
  Abiturient ──< AbiturientAnswer >── Question
  Abiturient ──< AbiturientAnswer >── AnswerOption
"""
from django.db import models


class SiteSettings(models.Model):
    """
    Глобальные настройки экзамена. Всегда ровно одна запись (pk=1).
    Управляется через панель сотрудников.
    """
    exam_is_active = models.BooleanField(
        default=False,
        verbose_name='Тестирование открыто'
    )
    access_code = models.CharField(
        max_length=30, blank=True, default='',
        verbose_name='Код доступа для студентов',
        help_text='Если пусто — код не требуется. Сообщите устно в аудитории.'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Настройки экзамена'

    def __str__(self):
        status = 'ОТКРЫТО' if self.exam_is_active else 'ЗАКРЫТО'
        return f'Тестирование: {status}'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Subject(models.Model):
    """Учебный предмет — Английский язык, Математика, Русский язык."""

    name = models.CharField(max_length=100, verbose_name='Название предмета')
    # Определяет порядок блоков на странице теста (1=Английский, 2=Математика, 3=Русский)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['order']

    def __str__(self):
        return self.name


class TestVariant(models.Model):
    """
    Вариант теста — готовый набор вопросов.
    Вариант выбирается случайно при старте из вариантов для класса абитуриента.
    """

    GRADE_CHOICES = [('9', '9 класс'), ('11', '11 класс')]

    name = models.CharField(max_length=100, verbose_name='Название варианта')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, default='9', verbose_name='Класс')
    is_active = models.BooleanField(default=True, verbose_name='Активен для выбора')
    # PDF-оригинал теста для архива методистов
    pdf_file = models.FileField(
        upload_to='test_pdfs/',
        blank=True, null=True,
        verbose_name='PDF-документ теста'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вариант теста'
        verbose_name_plural = 'Варианты теста'
        ordering = ['name']

    def __str__(self):
        return self.name

    def question_count(self):
        return self.questions.count()
    question_count.short_description = 'Кол-во вопросов'


class Question(models.Model):
    """
    Вопрос теста. Привязан к конкретному Варианту и Предмету.
    Поле `order` задаёт нумерацию внутри предмета (1–20).
    """

    variant = models.ForeignKey(
        TestVariant,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Вариант теста'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='questions',
        verbose_name='Предмет'
    )
    text = models.TextField(verbose_name='Текст вопроса')
    order = models.PositiveIntegerField(default=1, verbose_name='Номер вопроса в предмете')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['subject__order', 'order']
        unique_together = [('variant', 'subject', 'order')]

    def __str__(self):
        return f'[{self.variant.name}] {self.subject.name} — вопрос №{self.order}'


class AnswerOption(models.Model):
    """
    Один из четырёх вариантов ответа на вопрос.
    ВАЖНО: поле `is_correct` НИКОГДА не передаётся на фронтенд.
    Проверка правильности выполняется только на бэкенде при submit.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Вопрос'
    )
    text = models.CharField(max_length=1000, verbose_name='Текст варианта ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        marker = '✓' if self.is_correct else '○'
        return f'{marker} {self.question} | {self.text[:60]}'


class Abiturient(models.Model):
    """
    Абитуриент — участник тестирования.
    ПИН уникален — исключает повторное прохождение теста.
    """

    GRADE_CHOICES = [
        ('9', '9 класс'),
        ('11', '11 класс'),
    ]

    # Персональные данные
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    school = models.CharField(max_length=300, verbose_name='Школа / Учебное заведение')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, verbose_name='Класс')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    # Документ удостоверяющий личность — заполняется хотя бы одно из двух полей
    pin = models.CharField(
        max_length=14, blank=True, null=True, unique=True,
        verbose_name='ПИН (паспорт, 14 цифр)'
    )
    birth_certificate = models.CharField(
        max_length=30, blank=True, null=True, unique=True,
        verbose_name='Свидетельство о рождении'
    )

    # Количество зафиксированных нарушений антишпаргалочной системой
    violations_count = models.PositiveSmallIntegerField(default=0, verbose_name='Нарушений зафиксировано')

    # Данные тестирования
    test_variant = models.ForeignKey(
        TestVariant,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Выбранный вариант теста'
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Время начала теста')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Время завершения теста')
    is_completed = models.BooleanField(default=False, verbose_name='Тест завершён')

    class Meta:
        verbose_name = 'Абитуриент'
        verbose_name_plural = 'Абитуриенты'
        ordering = ['-started_at']

    def __str__(self):
        doc = self.pin or self.birth_certificate or '—'
        return f'{self.last_name} {self.first_name} {self.middle_name} ({doc})'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def doc_number(self):
        """Номер документа для отображения: ПИН или свидетельство о рождении."""
        if self.pin:
            return self.pin
        return self.birth_certificate or '—'


class TestResult(models.Model):
    """
    Итоговый результат тестирования.
    OneToOne с Abiturient — один абитуриент, один результат.
    """

    abiturient = models.OneToOneField(
        Abiturient,
        on_delete=models.CASCADE,
        related_name='result',
        verbose_name='Абитуриент'
    )
    # Общий балл = сумма трёх предметных баллов
    total_score = models.PositiveIntegerField(default=0, verbose_name='Общий балл (из 60)')
    english_score = models.PositiveIntegerField(default=0, verbose_name='Английский язык (из 20)')
    math_score = models.PositiveIntegerField(default=0, verbose_name='Математика (из 20)')
    russian_score = models.PositiveIntegerField(default=0, verbose_name='Русский язык (из 20)')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.abiturient.full_name} — {self.total_score}/60 баллов'


class AbiturientAnswer(models.Model):
    """
    Детальная запись: какой ответ абитуриент дал на конкретный вопрос.
    Используется для детальной аналитики в админке.
    """

    abiturient = models.ForeignKey(
        Abiturient,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Абитуриент'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='abiturient_answers',
        verbose_name='Вопрос'
    )
    # None = абитуриент не ответил на вопрос
    selected_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Выбранный вариант ответа'
    )
    is_correct = models.BooleanField(default=False, verbose_name='Ответ верный')

    class Meta:
        verbose_name = 'Ответ абитуриента'
        verbose_name_plural = 'Ответы абитуриентов'
        # Один абитуриент — один ответ на один вопрос
        unique_together = [('abiturient', 'question')]
        ordering = ['question__subject__order', 'question__order']

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f'{status} {self.abiturient.last_name} | {self.question}'
