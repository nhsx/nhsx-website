from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuthorIndexView.as_view(), name='index'),
    path('create/', views.AuthorCreateView.as_view(), name='create'),
    path('edit/<slug:slug>', views.AuthorUpdateView.as_view(), name='edit'),
]
