#  Using Django built-in user registration form
from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
  # add email field to the built-in ones
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")

  def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.email = self.cleaned_data['email'] # assign and check at the same time
    # other field are already checked in the built-in functions
    if commit:
      user.save()
    return user