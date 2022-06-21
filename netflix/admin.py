from django.contrib import admin

from netflix.views import like
from .models import Like, Profile, Genre, Director, Actor, Composer, Movie, IMDb_Rating, Other_Rating, Rotten_Tomatoes_Rating, Comment


class TitleSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class NameSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CommentConfig(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('text',)}
    list_display = ['text', 'date']


class Profile_list(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name']


admin.site.register(Profile, Profile_list)
admin.site.register(Genre, TitleSlug)
admin.site.register(Actor, NameSlug)
admin.site.register(Director, NameSlug)
admin.site.register(Movie, TitleSlug)
admin.site.register(Composer, NameSlug)
admin.site.register(Other_Rating)
admin.site.register(Rotten_Tomatoes_Rating)
admin.site.register(IMDb_Rating)
admin.site.register(Comment, CommentConfig)
