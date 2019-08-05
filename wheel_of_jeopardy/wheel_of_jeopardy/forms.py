from django import forms
from .models import Category


class startGameForm(forms.Form):
    user_1 = forms.CharField(label='user1', max_length=100)
    user_2 = forms.CharField(label='user2', max_length=100)
    category_1 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))
    category_2 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))
    category_3 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))
    category_4 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))
    category_5 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))
    category_6 = forms.ModelChoiceField(queryset=Category.objects.all().values('category_title'))

