from __future__ import annotations
from distutils.command.upload import upload
from email.policy import default
from os import link
from pyexpat import model
from tabnanny import verbose
from tkinter import CASCADE
from turtle import title
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
from django.conf import settings
import uuid
import datetime
import hashlib
import uuid
from typing import Any
import user_agents
from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _lazy
from movie.settings import REQUEST_CONTEXT_ENCODER, REQUEST_CONTEXT_EXTRACTOR


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Profile')
    picture = models.ImageField(
        'Profile Picture', blank=True, upload_to='user/pictures/')
    email = models.EmailField('Email', blank=True, unique=True)
    first_name = models.CharField('First Name', blank=True, max_length=255)
    last_name = models.CharField('Last Name', blank=True, max_length=255)
    last_visit = models.DateTimeField('Last Visit', default=timezone.now)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_absolute_url(self):
        return reverse('profile_detail_url', kwargs={'slug': self.slug})

    def get_current_path(self):
        return '/profile/' + request.path

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
        return "/genres/" + str(self.slug) + "/"

    def get_absolute_url(self):
        return reverse('genre_detial_url', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Director(models.Model):
    image = models.ImageField("Image", upload_to='directors/')
    name = models.CharField("Name", max_length=255)
    type = models.CharField('Type', max_length=255, default='Director')
    description = models.TextField('About', blank=True)
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
    type = models.CharField('Type', max_length=255, default='Actor')
    description = models.TextField('About')
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
    type = models.CharField('Type', max_length=255, default='Composer')
    description = models.TextField('About', blank=True)
    slug = models.SlugField('Link', unique=True)

    class Meta:
        verbose_name = 'Composer'
        verbose_name_plural = 'Composers'

    def get_absolute_url(self):
        return reverse('composer_detail_url', kwargs={"slug": self.slug})

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
    director = models.ManyToManyField(
        Director, blank=True, verbose_name='Director')
    cast = models.ManyToManyField(
        Actor, blank=True, verbose_name='Cast')
    imdb_rating = models.ForeignKey(
        IMDb_Rating, on_delete=models.CASCADE, null=True, verbose_name="IMDb Rating")
    rotten_tomatoes_rating = models.ForeignKey(
        Rotten_Tomatoes_Rating, on_delete=models.CASCADE, null=True, verbose_name="Rotten Tomatoes Rating")
    other_rating = models.ForeignKey(
        Other_Rating, on_delete=models.CASCADE, null=True, verbose_name="Other Rating")
    budget = models.CharField('Budget', max_length=255,
                              default="20 million", blank=True)
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


class Role(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField('Actor Role', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role


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
        return self.author.username + " | " + self.movie.title + " | " + self.text


class View(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Like(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Dislike(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CommentDislike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Poll(models.Model):
    question = models.CharField('Poll Question', max_length=255)
    actor = models.ManyToManyField(Actor, blank=True, verbose_name='Actors')
    director = models.ManyToManyField(
        Director, blank=True, verbose_name='Directors')
    composer = models.ManyToManyField(
        Composer, blank=True, verbose_name='Composers')
    firstchoice_title = models.CharField(
        'First Choice Title', max_length=255, default='Yes')
    secondchoice_title = models.CharField(
        'Second Choice Title', max_length=255, default='No')

    def __str__(self):
        return self.question


class FirstChoice(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)


class SecondChoice(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)


class View(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


def parse_remote_addr(request: HttpRequest) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR", "")


def parse_ua_string(request: HttpRequest) -> str:
    """Extract client user-agent from request."""
    return request.headers.get("User-Agent", "")


class UserVisitManager(models.Manager):
    """Custom model manager for UserVisit objects."""

    def build(self, request: HttpRequest, timestamp: datetime.datetime) -> UserVisit:
        """Build a new UserVisit object from a request, without saving it."""
        uv = UserVisit(
            user=request.user,
            timestamp=timestamp,
            session_key=request.session.session_key,
            remote_addr=parse_remote_addr(request),
            ua_string=parse_ua_string(request),
            context=REQUEST_CONTEXT_EXTRACTOR(request),
        )
        uv.hash = uv.md5().hexdigest()
        return uv


class UserVisit(models.Model):
    """
    Record of a user visiting the site on a given day.
    This is used for tracking and reporting - knowing the volume of visitors
    to the site, and being able to report on someone's interaction with the site.
    We record minimal info required to identify user sessions, plus changes in
    IP and device. This is useful in identifying suspicious activity (multiple
    logins from different locations).
    Also helpful in identifying support issues (as getting useful browser data
    out of users can be very difficult over live chat).
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Users")
    timestamp = models.DateTimeField(
        help_text=_lazy(
            "The time at which the first visit of the day was recorded"),
        default=timezone.now,
    )
    session_key = models.CharField(
        help_text="Django session identifier", max_length=40)
    remote_addr = models.CharField(
        help_text=_lazy(
            "Client IP address (from X-Forwarded-For HTTP header, "
            "or REMOTE_ADDR request property)"
        ),
        max_length=100,
        blank=True,
    )
    ua_string = models.TextField(
        "User agent (raw)",
        help_text=_lazy("Client User-Agent HTTP header"),
        blank=True,
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    hash = models.CharField(
        max_length=32,
        help_text=_lazy("MD5 hash generated from request properties"),
        unique=True,
    )
    created_at = models.DateTimeField(
        help_text=_lazy(
            "The time at which the database record was created (!=timestamp)"
        ),
        auto_now_add=True,
    )
    context = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        encoder=REQUEST_CONTEXT_ENCODER,
        help_text=_lazy(
            "Used for storing ad hoc / ephemeral data - e.g. GeoIP."),
    )

    objects = UserVisitManager()

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self) -> str:
        return f"{self.user} visited the site on {self.timestamp}"

    def __repr__(self) -> str:
        return f"<UserVisit id={self.id} user_id={self.user_id} date='{self.date}'>"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Set hash property and save object."""
        self.hash = self.md5().hexdigest()
        super().save(*args, **kwargs)

    @property
    def user_agent(self) -> user_agents.parsers.UserAgent:
        """Return UserAgent object from the raw user_agent string."""
        return user_agents.parsers.parse(self.ua_string)

    @property
    def date(self) -> datetime.date:
        """Extract the date of the visit from the timestamp."""
        return self.timestamp.date()

    # see https://github.com/python/typeshed/issues/2928 re. return type
    def md5(self) -> hashlib._Hash:
        """Generate MD5 hash used to identify duplicate visits."""
        h = hashlib.md5(str(self.user.id).encode())  # noqa: S303
        h.update(self.date.isoformat().encode())
        h.update(self.session_key.encode())
        h.update(self.remote_addr.encode())
        h.update(self.ua_string.encode())
        return h


class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            User.objects.filter(pk=request.user.pk).update(
                last_visit=timezone.now())
        return response