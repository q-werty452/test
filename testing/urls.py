from django.urls import path
from . import views
from . import staff_views

urlpatterns = [
    # ── Абитуриент ──
    path('', views.register_view, name='register'),
    path('test/', views.test_view, name='test'),
    path('test/submit/', views.submit_test_view, name='submit_test'),
    path('test/violation/', views.log_violation_view, name='log_violation'),
    path('complete/', views.complete_view, name='complete'),

    # ── Портал сотрудников ──
    path('staff/login/',  staff_views.staff_login_view,  name='staff_login'),
    path('staff/logout/', staff_views.staff_logout_view, name='staff_logout'),
    path('staff/',        staff_views.staff_dashboard_view, name='staff_dashboard'),
    path('staff/student/<int:pk>/',
         staff_views.staff_student_detail_view, name='staff_student_detail'),
    path('staff/student/<int:pk>/print/',
         staff_views.staff_print_report_view, name='staff_print_report'),
    path('staff/export/excel/',
         staff_views.export_excel_view, name='export_excel'),
    path('staff/exam/settings/',
         staff_views.exam_settings_view, name='exam_settings'),
]
