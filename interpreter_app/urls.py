from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("run/", views.run_code_ajax, name="run_code_ajax"),  # Endpoint para ejecutar código
]
