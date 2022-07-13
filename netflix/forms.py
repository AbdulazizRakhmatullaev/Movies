from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    picture = forms.ImageField(
        label='',
        required=False,
        widget=forms.FileInput(
            {'class': 'pp-input', 'style': 'padding: 8px 15px'})
    )
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            {'class': 'pp-input'})
    )
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.EmailInput(
            {'class': 'pp-input'})
    )
    first_name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            {'class': 'pp-input'})
    )
    last_name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            {'class': 'pp-input'})
    )

    class Meta:
        model = Profile
        fields = (
            'picture',
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def save(self, user, commit=True):
        profile = user.profile
        if self.cleaned_data['picture'] != None:
            profile.picture = self.cleaned_data["picture"]
        if self.cleaned_data['username'] != None:
            user.username = self.cleaned_data["username"]
        if self.cleaned_data['email'] != None:
            user.email = self.cleaned_data["email"]
        if self.cleaned_data['first_name'] != None:
            user.first_name = self.cleaned_data["first_name"]
        if self.cleaned_data['last_name'] != None:
            user.last_name = self.cleaned_data["last_name"]
        user.save()
        profile.save()
        return user, profile
