from distutils.command.upload import upload
from email.policy import default
from os import link
from tabnanny import verbose
from tkinter import CASCADE
from unicodedata import decimal
from django.db import models
from django.forms import SlugField
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from platformdirs import user_cache_dir
from requests import request


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Profile')
    picture = models.ImageField(
        'Profile Picture', blank=True, upload_to='user/pictures/')
    email = models.EmailField('Email', blank=True, unique=True)
    first_name = models.CharField('First Name', blank=True, max_length=255)
    last_name = models.CharField('Last Name', blank=True, max_length=255)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_absolute_url(self):
        return reverse('profile_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    image = models.ImageField("Image", upload_to='genres/')
    title = models.CharField("Title", max_length=255)
    slug = models.SlugField("Link", unique=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def current_path(self):
        return "/Genres/" + str(self.id) + "/"

    def get_absolute_url(self):
        return reverse('genre_detial_url', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Director(models.Model):
    image = models.ImageField("Image", upload_to='directors/')
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Link", unique=True)

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"

    def current_path(self):
        return "/Directors/" + str(self.name) + "/"

    def get_absolute_url(self):
        return reverse('director_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Actor(models.Model):
    image = models.ImageField("Image", upload_to='cast/')
    name = models.CharField("Name", max_length=255)
    description = models.TextField('About an Actor')
    slug = models.SlugField("Link", unique=True)

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Cast"

    def current_path(self):
        return "/Actor/" + str(self.name) + "/"

    def get_absolute_url(self):
        return reverse('actor_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class IMDb_Rating(models.Model):
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=5.0)

    class Meta:
        verbose_name = "IMDb Rating"
        verbose_name_plural = "IMDb Ratings"

    def __str__(self):
        return str(self.rate)


class Rotten_Tomatoes_Rating(models.Model):
    rate = models.DecimalField(max_digits=3, decimal_places=0,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = "Rotten Tomatoes Rating"
        verbose_name_plural = "Rotten Tomatoes Ratings"

    def __str__(self):
        return str(self.rate)


class Other_Rating(models.Model):
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=3.5)

    class Meta:
        verbose_name = "Other Rating"
        verbose_name_plural = "Other Ratings"

    def __str__(self):
        return str(self.rate)


class Composer(models.Model):
    image = models.ImageField('Image', upload_to='composers/')
    name = models.CharField("Composer Name", max_length=255)
    slug = models.SlugField('Link', unique=True)

    class Meta:
        verbose_name = 'Music Composer'
        verbose_name_plural = 'Music Composers'

    def get_absolute_url(self):
        return reverse('musiccomposer_detail_url', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Movie(models.Model):
    poster = models.ImageField(
        'Poster', blank=True, upload_to='posters/')
    movie = models.FileField("Movie Copy", upload_to="movies/")
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description')
    genre = models.ManyToManyField(
        Genre, blank=True, verbose_name='Genre')
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, null=True, verbose_name='Director')
    cast = models.ManyToManyField(
        Actor, blank=True, verbose_name='Cast')
    imdb_rating = models.ForeignKey(
        IMDb_Rating, on_delete=models.CASCADE, null=True, verbose_name="IMDb Rating")
    rotten_tomatoes_rating = models.ForeignKey(
        Rotten_Tomatoes_Rating, on_delete=models.CASCADE, null=True, verbose_name="Rotten Tomatoes Rating")
    other_rating = models.ForeignKey(
        Other_Rating, on_delete=models.CASCADE, null=True, verbose_name="Other Rating")
    budget = models.CharField('Budget', max_length=255, default="20 million", blank=True)
    box_office = models.CharField(
        'Box Office', max_length=255, default="1.50 billion", blank=True)
    composers = models.ManyToManyField(
        Composer, blank=True, verbose_name="Composers")
    date = models.DateField('Release Date', default=timezone.now)
    country = CountryField(blank_label='Select Country')
    Quality = models.CharField("Quality", max_length=255, default="720p")
    runtime = models.CharField("Runtime", max_length=255, default="1h 20m")
    publication = models.BooleanField("Publication", default=True)
    slug = models.SlugField('Link', unique=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def get_absolute_url(self):
        return reverse('movie_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Author")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name="Movie")
    text = models.TextField("Comment", default='What a Movie!')
    date = models.DateTimeField("Date", default=timezone.now)
    publication = models.BooleanField("Publication", default=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.author.username + "|" + self.movie.title


class Like(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Dislike(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
