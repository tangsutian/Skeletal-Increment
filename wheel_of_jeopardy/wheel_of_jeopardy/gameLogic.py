from django.shortcuts import render, render_to_response

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.template import loader

import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


@require_http_methods(["GET"])
def home(request):
    template = loader.get_template('home.html')
    context = {
        'button_text': 'Start Game',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def wheel(request):
    template = loader.get_template('wheel.html')
    context = {
        'sector_color': '#baa',
        'button_text': 'Spin Wheel',
        'button_link': 'wheel/selection',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def spin(request):
    template = loader.get_template('wheel2.html')
    context = {
        'sector_color': '#bab',
        'button_text': 'Go to Game Board',
        'button_link': 'board',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def board(request):
    template = loader.get_template('board.html')
    values = []
    for i in range(0, 5):
        values.append(str(i * 200 + 200))
    context = {
        'category_1': 'Animals',
        'category_2': 'Sports',
        'category_3': 'Cars',
        'category_4': 'Books',
        'category_5': 'Programming Languages',
        'category_6': 'TV/ Movies',
        'point_totals': values,
        'num_columns': [1, 1, 1, 1, 1, 1],
        'button_text': 'Show Question!',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def question(request):
    question = 'How much wood could a wood chuck chuck if a wood chuck could chuck wood?'
    template = loader.get_template('question.html')
    context = {
        'question_text': question,
        'button_1_text': 'Right',
        'button_1_color': 'green',
        'button_2_text': 'Wrong',
        'button_2_color': 'red',
    }
    return HttpResponse(template.render(context, request))
