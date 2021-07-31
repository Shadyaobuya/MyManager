from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]



class UserForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150,widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px'}))
    firstname=forms.CharField(label='First Name',widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px'}))
    lastname=forms.CharField(label='Last Name',widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px'}))
    email = forms.EmailField(label='Enter email',widget=forms.EmailInput(attrs={'class':'form-control','style':'width:300px'}))
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))

    def check_username(self):
        username = self.cleaned_data['username']
        entry = User.objects.filter(username=username)
        if entry.exists():
            raise  ValidationError("Username already exists")
        return username

    def check_email(self):
        email = self.cleaned_data['email']
        entry = User.objects.filter(email=email)
        if entry.exists():
            raise  ValidationError("Email already exists")
        return email
    
    def fname(self):
        firstname=self.cleaned_data['firstname']
        return firstname
    
    def lname(self):
        lastname=self.cleaned_data['lastname']
        return lastname


    def check_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1  != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            last_name=self.cleaned_data['lastname'],
            first_name=self.cleaned_data['firstname']   
        )
        
        return user