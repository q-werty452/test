from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_add_birth_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='abiturient',
            name='phone',
            field=models.CharField(default='', max_length=30, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]
