
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tag>/', views.index, name='tagfilter'),
    path('<slug:slug>/', views.ArticleView.as_view(), name='viewpost'),
]
