from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (  'topic','description',
                    'image_description','image',
                    'another_image_description','another_image',
                    'other_image_description','other_image')


class AnswerForm(forms.ModelForm):
   
    class Meta:
        model = Answer
        fields = ('email','answer','image')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', ]

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile

		fields=[
			"bio",
			"image",
		]