from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, COUNTRIES

class UserForm(UserCreationForm):
	'''
	Form that uses built-in UserCreationForm to handel user creation
	'''
	username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	password1 = forms.CharField(required=True, widget=forms.PasswordInput())
	password2 = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')



class AuthForm(AuthenticationForm):
	'''
	Form that uses built-in AuthenticationForm to handel user auth
	'''
	username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	password = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','password')



class UserProfileForm(forms.ModelForm):
	'''
	Basic model-form for our user profile
	'''
	telephone = forms.CharField(max_length=255, required=False, widget=forms.TextInput())
	address = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	town = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	county = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	post_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput())
	country = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
	country = forms.CharField(max_length=100, required=False, widget=forms.Select(choices=COUNTRIES))
	
	class Meta:
		model = UserProfile
		fields = ('telephone', 'address', 'town', 'county', 'post_code', 'country')


class UserAlterationForm(forms.ModelForm):
	'''
	Basic model-form for our user
	'''
	first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
	email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')