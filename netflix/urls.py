from django.urls import path, URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/<str:username>/',
         views.profile_detail, name="profile_detail_url"),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail_url'),
    path('genres/<slug:slug>/', views.genre_detail, name='genre_detail_url'),
    path('actors/<slug:slug>', views.actor_detail, name="actor_detail_url"),
    path('directors/<slug:slug>', views.director_detail, name="director_detail_url"),
    path('composers/<slug:slug>', views.composer_detail, name="composer_detail_url"),
    path('search/', views.search, name='search'),
    path('register/', views.register, name="register"),
    path("signout/", views.signout, name="signout"),
    path("signin/", views.signin, name="signin"),
    path('sort/', views.sort, name="sort")
]
