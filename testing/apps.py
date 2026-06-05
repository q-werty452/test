from django.apps import AppConfig


class TestingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testing'
    verbose_name = 'Тестирование абитуриентов'

    def ready(self):
        from django.db.backends.signals import connection_created

        def enable_wal(sender, connection, **kwargs):
            if connection.vendor == 'sqlite':
                with connection.cursor() as cursor:
                    # WAL-режим: несколько читателей + 1 писатель одновременно
                    cursor.execute('PRAGMA journal_mode=WAL;')
                    cursor.execute('PRAGMA synchronous=NORMAL;')
                    cursor.execute('PRAGMA cache_size=-64000;')  # 64 МБ кэша

        connection_created.connect(enable_wal)
