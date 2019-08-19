from django import forms
from .models import Category


class startGameForm(forms.Form):
    user_1 = forms.CharField(label='user1', max_length=100, required=False)
    user_2 = forms.CharField(label='user2', max_length=100, required=False)
    category_1 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    category_2 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    category_3 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    category_4 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    category_5 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    category_6 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)