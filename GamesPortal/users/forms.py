from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages


class RegisterForm(UserCreationForm):
    """ Formularz rejestracji """
    username = forms.CharField(label='Nazwa użytkownika',
                               min_length=2,
                               max_length=20,
                               widget=forms.TextInput(
                                   attrs={'title': 'Wprowadź nazwę użytkownika o długości między 2 a 20 znaków.'}))
    email = forms.EmailField(label='Adres e-mail')
    password1 = forms.CharField(label='Wprowadź hasło',
                                widget=forms.PasswordInput(
                                    attrs={'title': 'Wprowadź hasło o długości pomiędzy 5 a 15 znaków.'}),
                                min_length=5,
                                max_length=15)
    password2 = forms.CharField(label='Potwierdź hasło',
                                widget=forms.PasswordInput(
                                    attrs={'title': 'Powtórz wcześniej wprowadzone hasło.'}),
                                min_length=5,
                                max_length=15)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2']
        labels = {
            'username': 'Nazwa Użytkownika',
            'email': 'Adres e-mail',
            'password1': 'Wprowadź hasło',
            'password2': 'Potwierdź hasło',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f"Pole '{field.label}' jest wymagane do utworzenia konta użytkownika!"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nazwa użytkownika już istnieje.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Istnieje już użytkownik z podanym adresem e-mail.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są takie same.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są takie same.')
        return password2


class LoginForm(AuthenticationForm):
    """ Formularz logowania """
    username = forms.CharField(
        label='Nazwa użytkownika',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'title': 'Wprowadź nazwę użytkownika o długości między 2 a 20 znaków.'}),
        min_length=2,
        max_length=20,
        required=True,
        error_messages={
            'min_length': 'Nazwa użytkownika musi mieć co najmniej 2 znaki',
            'max_length': 'Nazwa użytkownika może mieć co najwyższej 20 znaków'})
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'title': 'Wprowadź hasło o długości pomiędzy 5 a 15 znaków.'}),
        min_length=5,
        max_length=15,
        required=True,
        error_messages={
            'min_length': 'Hasło musi mieć co najmniej 5 znaków',
            'max_length': 'Hasło może mieć co najwyżej 15 znaków'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Wprowadzono błędną nazwę użytkownika albo nie jesteś zarejestrowany.")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError("Wprowadzono błędną nazwę użytkownika albo nie jesteś zarejestrowany.")

        if user and not user.check_password(password):
            raise forms.ValidationError("Nieprawidłowe hasło.")

        return password
