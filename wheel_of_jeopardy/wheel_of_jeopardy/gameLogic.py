from django.shortcuts import render, render_to_response

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.template import loader

import os
import random

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MAXSECTORNUM = 12

from wheel_of_jeopardy.models import Category, Question, User, GameSession

@require_http_methods(['GET'])
def reset(request):
    User.objects.all().delete()
    GameSession.objects.all().delete()
    Question.objects.all().delete()
    Category.objects.all().delete()

    return HttpResponseRedirect('/')

@require_http_methods(["GET", "POST"])
def home(request):
    template = loader.get_template('home.html')
    n1 = ''
    if 'player_1_name' in request.POST:
        n1 = request.POST['player_1_name']
        player1 = User(username=n1, total_points=0, r1_points=0, r2_points=0, free_tokens=0, current_turn=True)
        player1.save()

    n2 = ''
    if 'player_2_name' in request.POST:
        n2 = request.POST['player_2_name']
        player2 = User(username=n2, total_points=0, r1_points=0, r2_points=0, free_tokens=0, current_turn=False)
        player2.save()

    context = {
        'button_text': 'Start Game',
        'button_1_text': 'Question Manager',
        'button_2_text': 'Reset Game',
        'player_1_name': n1,
        'player_2_name': n2,
        'url': '/home/',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def wheel(request):
    all_entries = User.objects.all()
    points = [all_entries[len(all_entries)-2].pointTable(), all_entries[len(all_entries)-1].pointTable()]

    template = loader.get_template('wheel.html')
    context = {
        'sector_color': '#baa',
        'button_text': 'Spin Wheel',
        'button_link': 'wheel/spin/%d' % (random.randint(1,MAXSECTORNUM)),
        'player_points': points,
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
        'right_url': '/updateScore/right/',
        'wrong_url': '/updateScore/wrong/',
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

@require_http_methods(['POST'])
def right(request):
    players = User.objects.all()
    currentPlayer = players[len(players)-2]

    updateScore(currentPlayer, 100)
    return HttpResponseRedirect('/wheel/')

@require_http_methods(['POST'])
def wrong(request):
    players = User.objects.all()
    currentPlayer = players[len(players)-2]

    updateScore(currentPlayer, -100)
    return HttpResponseRedirect('/wheel/')

def updateScore(user, points):
    user.r1_points = user.r1_points + points
    user.total_points = user.total_points + points
    user.save()


@require_http_methods(["GET"])
def questionManager(request):
    template = loader.get_template('questionManager.html')
    context = {
        'button_text': 'Go Back',
        'url': '/newQuestion/',
    }
    return HttpResponse(template.render(context, request))
