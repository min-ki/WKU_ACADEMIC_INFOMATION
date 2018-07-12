from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class SignupForm(UserCreationForm):
     
    class Meta(UserCreationForm.Meta):
        # fields = ('username', 'email')
        fields = UserCreationForm.Meta.fields

    def save(self):
        user = super().save()
        return user