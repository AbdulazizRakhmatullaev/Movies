from unicodedata import category, name
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Actor, Composer, Director, Profile, Genre, Movie
from django.db.models import Q, Max, Count
from django.contrib.auth.hashers import make_password


def index(request):
    movies = Movie.objects.order_by('-date')
    genres = Genre.objects.order_by('title')
    context = {
        'genres': genres, 'movies': movies
    }
    return render(request, 'netflix/index.html', context)


def profile_detail(request, username):
    if not request.user.is_authenticated:
        return redirect('index')
    user = User.objects.get(username__exact=username)
    return render(request, "netflix/profile_detail.html", {"user": user})


def movie_detail(request, slug):
    movie = Movie.objects.get(slug__exact=slug)
    genres = Genre.objects.order_by('title')
    directors = Director.objects.all()
    composers = Composer.objects.all()
    actors = Actor.objects.all()
    context = {
        "movie": movie,
        "genres": genres,
        "composers": composers,
        'directors': directors,
        'actors': actors
    }
    return render(request, 'netflix/movie_detail.html', context)


def genre_detail(request, slug):
    genre = Genre.objects.get(slug__exact=slug)
    movies = Movie.objects.all()
    genres = Genre.objects.order_by('title')
    return render(request, 'netflix/genre_detail.html', {"genre": genre, "genres": genres, "movies": movies})


def actor_detail(request, slug):
    actor = Actor.objects.get(slug__exact=slug)
    return render(request, 'netflix/actor_detail.html', {"actor": actor})


def director_detail(request, slug):
    director = Director.objects.get(slug__exact=slug)
    return render(request, 'netflix/director_detail.html', {"director": director})


def composer_detail(request, slug):
    composer = Composer.objects.get(slug__exact=slug)
    return render(request, 'netflix/composer_detail.html', {"composer": composer})


def search(request):
    query = request.GET.get("search")
    movies = (
        Movie.objects.filter(Q(title__icontains=query))
    )
    return render(request, "netflix/search.html", {"query": query, "movies": movies})


def register(request):
    if not request.user.is_authenticated:
        message = None
        if request.method == 'POST':
            username = User.objects.create(
                username=request.POST.get('username'),
                password=make_password(request.POST.get('password')),
                email=request.POST.get('email')
            )
            if not User.objects.filter(username=username).exists():
                user = User
                user.save()
                profile = Profile()
                profile.user = user
                profile.save()
                login(request, user)
            return redirect('signin')
        return render(request, 'netflix/register.html')
    return redirect("index")
    # if not request.user.is_authenticated:
    #     if request.method == 'POST':
    #         user = User.objects.create(username=request.POST.get('username'), password=make_password(
    #             request.POST.get('password')), email=request.POST.get('email'))
    #         if not User.objects.filter(username=username).exists():
    #             if user.is_valid():
    #                 user.save()
    #                 return redirect("signin")
    #     return render(request, "netflix/register.html")
    # return redirect('index')


def signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = "Invalid Username or Password, Please Fill out Forms Carefully!"
            return render(request, "netflix/signin.html", {"message": message})
    return render(request, "netflix/signin.html", {"message": message})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def sort(request):
    query = request.GET.get('sort')
    movie = Movie.objects.order_by(query)
    return render(request, 'netflix/sort.html', {"query": query, "movie": movie})
