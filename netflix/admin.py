from django.contrib import admin
from .models import Choice_total, Poll, Profile, Genre, Director, Actor, Composer, Movie, IMDb_Rating, Other_Rating, Role, Rotten_Tomatoes_Rating, Comment, UserVisit


class UserVisitAdmin(admin.ModelAdmin):

    list_display = ("timestamp", "user", "session_key",
                    "remote_addr", "user_agent")
    list_filter = ("timestamp",)
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "ua_string",
    )
    raw_id_fields = ("user",)
    readonly_fields = (
        "user",
        "hash",
        "timestamp",
        "session_key",
        "remote_addr",
        "user_agent",
        "ua_string",
        "context",
        "created_at",
    )
    ordering = ("-timestamp",)


class TitleSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class NameSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class Profile_list(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name']


admin.site.register(UserVisit, UserVisitAdmin)
admin.site.register(Profile, Profile_list)
admin.site.register(Genre, TitleSlug)
admin.site.register(Actor, NameSlug)
admin.site.register(Director, NameSlug)
admin.site.register(Movie, TitleSlug)
admin.site.register(Composer, NameSlug)
admin.site.register(Other_Rating)
admin.site.register(Rotten_Tomatoes_Rating)
admin.site.register(IMDb_Rating)
admin.site.register(Comment)
admin.site.register(Poll)
admin.site.register(Choice_total)
admin.site.register(Role)
