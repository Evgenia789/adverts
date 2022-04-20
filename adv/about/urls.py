from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('about_us/', views.AboutUsView.as_view(), name='us')
]
