"""
URL configuration for DBP_ml_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import IMG2IMG, get_task_status
urlpatterns = [
    path('img-to-img/', IMG2IMG.as_view(), name='IMG2IMG'),
    path('task-status/<str:task_id>/', get_task_status, name='task_status'),
    # path('img-to-img-with-promt/', IMG2IMG_WITH_PROMT_TEXT.as_view(), name='IMG2IMG_WITH_PROMT_TEXT'),
]