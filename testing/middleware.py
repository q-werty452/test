from django.shortcuts import render


# Пути, которые всегда доступны (не блокируются)
_ALWAYS_OPEN = ('/staff/', '/admin/', '/static/', '/media/')


class ExamGateMiddleware:
    """
    Блокирует студенческую часть сайта когда экзамен выключен.
    Панель сотрудников и статика — всегда доступны.
    Активные сессии (студент уже в тесте) могут продолжать и сдавать.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Служебные пути пропускаем без проверки
        if any(request.path.startswith(p) for p in _ALWAYS_OPEN):
            return self.get_response(request)

        # Студент уже в активной сессии — разрешаем продолжить тест и сдать
        if request.session.get('abiturient_id') and request.path != '/':
            return self.get_response(request)

        # Страница завершения всегда доступна
        if request.path == '/complete/':
            return self.get_response(request)

        # Импортируем здесь чтобы избежать circular import при старте
        from .models import SiteSettings
        settings = SiteSettings.get()

        if not settings.exam_is_active:
            return render(request, 'testing/closed.html', status=200)

        return self.get_response(request)
