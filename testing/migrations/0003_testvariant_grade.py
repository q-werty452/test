from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_abiturient_violations_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='testvariant',
            name='grade',
            field=models.CharField(
                choices=[('9', '9 класс'), ('11', '11 класс')],
                default='9',
                max_length=2,
                verbose_name='Класс',
            ),
        ),
    ]
