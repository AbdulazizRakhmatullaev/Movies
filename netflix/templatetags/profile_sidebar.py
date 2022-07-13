from django import template
from django.shortcuts import redirect
from django.template import Library
from netflix.models import Profile

register = Library()


@register.inclusion_tag("netflix/profile_sidebar.html")
def profile_sidebar():
    profile = Profile.objects.all()
    return {'profile': profile}
