from django.urls import path
from . import views
# fee_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-student/', views.add_student, name='add_student'),
    path('add_fee/', views.add_fee, name='add_fee'),
    path('slip/<int:student_id>/', views.generate_slip, name='generate_slip'),
]
