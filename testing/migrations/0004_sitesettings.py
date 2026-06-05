from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_testvariant_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('exam_is_active', models.BooleanField(default=False, verbose_name='Тестирование открыто')),
                ('access_code', models.CharField(blank=True, default='', help_text='Если пусто — код не требуется.', max_length=30, verbose_name='Код доступа для студентов')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Настройки экзамена'},
        ),
    ]
