from django.contrib import admin
from .models import Question, Category

admin.site.register(Category)
admin.site.register(Question)