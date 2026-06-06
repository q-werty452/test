"""
Data migration: умножает все существующие баллы на 2.
Причина: система перешла на начисление 2 баллов за правильный ответ (было 1).
Применяется автоматически при `python manage.py migrate`.
"""
from django.db import migrations


def double_scores(apps, schema_editor):
    TestResult = apps.get_model('testing', 'TestResult')
    updated = 0
    for result in TestResult.objects.all():
        result.english_score *= 2
        result.math_score    *= 2
        result.russian_score *= 2
        result.total_score   *= 2
        result.save()
        updated += 1
    if updated:
        print(f'\n  Обновлено записей: {updated} (баллы умножены на 2)')


def halve_scores(apps, schema_editor):
    """Откат: делим баллы обратно на 2 (если нужен rollback)."""
    TestResult = apps.get_model('testing', 'TestResult')
    for result in TestResult.objects.all():
        result.english_score //= 2
        result.math_score    //= 2
        result.russian_score //= 2
        result.total_score   //= 2
        result.save()


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_abiturient_phone'),
    ]

    operations = [
        migrations.RunPython(double_scores, reverse_code=halve_scores),
    ]
