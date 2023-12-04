from django import forms


class GameSearchForm(forms.Form):
    search_query = forms.CharField(label='Zawartość tytułu wyszukania',
                                   required=False)
