from django.contrib import admin
from django.urls import path
import sitezappers.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('report/<str:link>/', views.report, name='report'),  # Capture the URL parameter
]
