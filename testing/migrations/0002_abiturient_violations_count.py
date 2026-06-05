from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='abiturient',
            name='violations_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Нарушений зафиксировано'),
        ),
    ]
