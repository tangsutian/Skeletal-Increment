from django.shortcuts import render, render_to_response

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.template import loader

import os
import random

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MAXSECTORNUM = 12

from wheel_of_jeopardy.models import Category, Question


@require_http_methods(["GET"])
def home(request):
    template = loader.get_template('home.html')
    context = {
        'button_text': 'Start Game',
        'button_1_text': 'Question Manager',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def wheel(request):
    template = loader.get_template('wheel.html')
    context = {
        'sector_color': '#baa',
        'button_text': 'Spin Wheel',
        'button_link': 'wheel/spin/%d' % (random.randint(1,MAXSECTORNUM))
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def spin(request, sector_id):
    template = loader.get_template('wheel2.html')
    context = {
        'sector_color': '#bab',
        'sector_spun': sector_id,
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
    all_entries = Question.objects.all()
    lastquestion = all_entries[len(all_entries)-1]
    question = lastquestion.question_text
    answer = lastquestion.answer_text
    template = loader.get_template('question.html')
    context = {
        'question_text': question,
        'answer_text': answer,
        'button_1_text': 'Right',
        'button_1_color': 'green',
        'button_2_text': 'Wrong',
        'button_2_color': 'red',
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(['POST'])
def addNewQuestion(request):
    category1 = Category(
            category_title='Example Question'
        )
    category1.save()

    question1 = Question(
            question_text=request.POST['question'], 
            answer_text=request.POST['answer'], 
            category=category1, 
            point_value=200, 
            asked=False,
            round_number=Question.ROUND_ONE,
            game_session=None,
        )
    question1.save()

    return HttpResponseRedirect('/questionManager/')


@require_http_methods(["GET"])
def questionManager(request):
    template = loader.get_template('questionManager.html')
    context = {
        'button_text': 'Go Back',
        'url': '/new_question/',
    }
    return HttpResponse(template.render(context, request))
