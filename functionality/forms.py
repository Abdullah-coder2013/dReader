from django import forms


class SearchForm(forms.Form):
    searchfield = forms.CharField(label="Search", max_length=150)
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
    
class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
    
class EditUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=False)
    email = forms.EmailField(label="Email", max_length=100, required=False)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(), required=False)