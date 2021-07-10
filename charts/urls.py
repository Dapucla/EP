from . import views
from django.urls import path

urlpatterns = [
    path('chart/', views.PostList.as_view(), name='home'),
]