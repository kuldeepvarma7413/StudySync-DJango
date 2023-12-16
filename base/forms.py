from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import cafiles

class userForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    
    
    
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']  # Set the username to the email value
        user.email = self.cleaned_data['email']
    
    

        if commit:
            user.save()
        return user
    
    
    
class PasswordUpdateForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password'}),
    )
    
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password'}),
    )


# class CaFilesForm(forms.ModelForm):
#     class Meta:
#         model = cafiles
#         fields = ['courseCode', 'teachername', 'canumber', 'cadate', 'files_ca']