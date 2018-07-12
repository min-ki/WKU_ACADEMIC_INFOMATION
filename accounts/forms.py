from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class SignupForm(UserCreationForm):
    
    intra_id = forms.CharField()
    intra_pw = forms.CharField()
    
    class Meta(UserCreationForm.Meta):
        # fields = ('username', 'email')
        fields = UserCreationForm.Meta.fields

    def save(self):
        user = super().save()
        return user


class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(label='3+3?')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', None)
        if answer != 6:
            raise forms.ValidationError('mismatched!')
        return answer
