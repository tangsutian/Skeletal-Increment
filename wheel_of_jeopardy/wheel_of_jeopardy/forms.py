from django import forms


class startGameForm(forms.Form):
    user_1 = forms.CharField(label='user1', max_length=100)
    user_2 = forms.CharField(label='user2', max_length=100)
