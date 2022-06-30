from cgitb import text
import email
from unicodedata import category, name
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from pytz import timezone
from .models import Actor, Composer, Director, Poll, Like, Profile, Genre, Comment, Movie, Role
from django.db.models import Q, Max, Count
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone


def index(request):
    movies = Movie.objects.order_by('-date')
    genres = Genre.objects.order_by('title')
    context = {
        'genres': genres,
        'movies': movies,
    }
    return render(request, 'netflix/index.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    comments = request.user.comment_set.order_by('-date')
    likes = request.user.like_set.order_by('-date')
    views = request.user.view_set.order_by('-date')
    context = {
        'comments': comments,
        'likes': likes,
        'views': views
    }
    return render(request, "netflix/profile.html", context)


def user_detail(request, username):
    user = User.objects.get(username__exact=username)
    likes = user.like_set.order_by('-date')
    comments = user.comment_set.order_by('-date')
    views = user.view_set.order_by('-date')
    context = {
        'user': user,
        'likes': likes,
        'comments': comments,
        'views': views
    }
    return render(request, "netflix/user_detail.html", context)


def movie_detail(request, slug):
    movie = Movie.objects.get(slug__exact=slug)
    if request.user.is_authenticated:
        if not movie.view_set.filter(user=request.user).exists():
            movie.view_set.create(user=request.user)
        else:
            view = request.user.view_set.get(movie=movie)
            view.date = timezone.now()
            view.save()
    genres = Genre.objects.all()
    context = {
        "movie": movie,
        "genres": genres
    }
    return render(request, 'netflix/movie_detail.html', context)

def genre_detail(request, slug):
    genre = Genre.objects.get(slug__exact=slug)
    movies = Movie.objects.all()
    genres = Genre.objects.order_by('title')
    return render(request, 'netflix/genre_detail.html', {"genre": genre, "genres": genres, "movies": movies})


def actor_detail(request, slug):
    actor = Actor.objects.get(slug__exact=slug)
    cast = Actor.objects.order_by('-name').exclude(id=actor.id)
    movies = Movie.objects.order_by('-date')
    return render(request, 'netflix/actor_detail.html', {"actor": actor, 'cast': cast, 'movies': movies})


def director_detail(request, slug):
    director = Director.objects.get(slug__exact=slug)
    directors = Director.objects.order_by('-name').exclude(id=director.id)
    movies = Movie.objects.order_by('-date')
    return render(request, 'netflix/director_detail.html', {"director": director, 'movies': movies, 'directors': directors})


def composer_detail(request, slug):
    composer = Composer.objects.get(slug__exact=slug)
    composers = Composer.objects.order_by('-name').exclude(id=composer.id)
    movies = Movie.objects.order_by('-date')
    return render(request, 'netflix/composer_detail.html', {
        "composer": composer,
        'movies': movies,
        'composers': composers
    })


def search(request):
    query = request.GET.get("search")
    movies = (
        Movie.objects.filter(Q(title__icontains=query))
    )
    genres = Genre.objects.order_by('title')
    return render(request, "netflix/search.html", {"query": query, "movies": movies, 'genres': genres})


def comment(request, slug):
    movie = Movie.objects.get(slug__exact=slug)
    if request.method == 'POST':
        comment = movie.comment_set.create(
            author=request.user,
            text=request.POST.get('text')
        )
        if request.user.is_superuser:
            comment.publish = True
            comment.save()
    return redirect(reverse('movie_detail_url', kwargs={'slug': slug}))


def like(request, slug):
    movie = Movie.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not movie.like_set.filter(user=request.user).exists():
                movie.like_set.create(user=request.user)
                if movie.dislike_set.filter(user=request.user).exists():
                    dislike = request.user.dislike_set.get(movie=movie)
                    dislike.delete()
            else:
                like = request.user.like_set.get(movie=movie)
                like.delete()
        else:
            return redirect('signin')
    return redirect(reverse('movie_detail_url', kwargs={'slug': slug}))


def dislike(request, slug):
    movie = Movie.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not movie.dislike_set.filter(user=request.user).exists():
                movie.dislike_set.create(user=request.user)
                if movie.like_set.filter(user=request.user).exists():
                    like = request.user.like_set.get(movie=movie)
                    like.delete()
            else:
                dislike = request.user.dislike_set.get(movie=movie)
                dislike.delete()
        else:
            return redirect('signin')
    return redirect(reverse('movie_detail_url', kwargs={'slug': slug}))


# ------------------------------


def firstChoice(request, slug):
    actor = Actor.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not actor.firstchoice_set.filter(user=request.user).exists():
                actor.firstchoice_set.create(user=request.user)
                if actor.secondchoice_set.filter(user=request.user).exists():
                    secondchoice = request.user.secondchoice_set.get(
                        actor=actor)
                    secondchoice.delete()
            else:
                firstchoice = request.user.firstchoice_set.get(actor=actor)
                firstchoice.delete()
    return redirect(reverse('actor_detail_url', kwargs={'slug': slug}))


def secondChoice(request, slug):
    actor = Actor.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not actor.secondchoice_set.filter(user=request.user).exists():
                actor.secondchoice_set.create(user=request.user)
                if actor.firstchoice_set.filter(user=request.user).exists():
                    firstchoice = request.user.firstchoice_set.get(
                        actor=actor)
                    firstchoice.delete()
            else:
                secondchoice = request.user.secondchoice_set.get(actor=actor)
                secondchoice.delete()
    return redirect(reverse('actor_detail_url', kwargs={'slug': slug}))


# ------------------------------


def DirectorFirstChoice(request, slug):
    director = Director.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not director.firstchoice_set.filter(user=request.user).exists():
                director.firstchoice_set.create(user=request.user)
                if director.secondchoice_set.filter(user=request.user).exists():
                    secondchoice = request.user.secondchoice_set.get(
                        director=director)
                    secondchoice.delete()
            else:
                firstchoice = request.user.firstchoice_set.get(
                    director=director)
                firstchoice.delete()
    return redirect(reverse('director_detail_url', kwargs={'slug': slug}))


def DirectorSecondChoice(request, slug):
    director = Director.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not director.secondchoice_set.filter(user=request.user).exists():
                director.secondchoice_set.create(user=request.user)
                if director.firstchoice_set.filter(user=request.user).exists():
                    firstchoice = request.user.firstchoice_set.get(
                        director=director)
                    firstchoice.delete()
            else:
                secondchoice = request.user.secondchoice_set.get(
                    director=director)
                secondchoice.delete()
    return redirect(reverse('director_detail_url', kwargs={'slug': slug}))


# ------------------------------


def ComposerFirstChoice(request, slug):
    composer = Composer.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not composer.firstchoice_set.filter(user=request.user).exists():
                composer.firstchoice_set.create(user=request.user)
                if composer.secondchoice_set.filter(user=request.user).exists():
                    secondchoice = request.user.secondchoice_set.get(
                        composer=composer)
                    secondchoice.delete()
            else:
                firstchoice = request.user.firstchoice_set.get(
                    composer=composer)
                firstchoice.delete()
    return redirect(reverse('composer_detail_url', kwargs={'slug': slug}))


def ComposerSecondChoice(request, slug):
    composer = Composer.objects.get(slug__exact=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not composer.secondchoice_set.filter(user=request.user).exists():
                composer.secondchoice_set.create(user=request.user)
                if composer.firstchoice_set.filter(user=request.user).exists():
                    firstchoice = request.user.firstchoice_set.get(
                        composer=composer)
                    firstchoice.delete()
            else:
                secondchoice = request.user.secondchoice_set.get(
                    composer=composer)
                secondchoice.delete()
    return redirect(reverse('composer_detail_url', kwargs={'slug': slug}))


def signup(request):
    if not request.user.is_authenticated:
        message = None
        if request.method == 'POST':
            username = User.objects.create(
                username=request.POST.get('username'),
                password=make_password(request.POST.get('password')),
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            if User.objects.filter(username=username).exists():
                user = username
                user.save()
                profile = Profile()
                profile.user = user
                profile.email = user.email
                profile.first_name = user.first_name
                profile.last_name = user.last_name
                profile.save()
                return redirect('signin')
            else:
                message = 'WTF man'
                return render(request, 'netflix/signup.html', {'message': message})
        return render(request, 'netflix/signup.html')
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
