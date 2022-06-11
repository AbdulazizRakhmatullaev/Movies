from tabnanny import verbose
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    username = forms.CharField(label="Username", required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        if commit:
            user.save()
            return user
