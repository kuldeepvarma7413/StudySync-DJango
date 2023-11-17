from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class userForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    
    
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set the username to the email value
        user.email = self.cleaned_data['email']
    
    

        if commit:
            user.save()
        return user
