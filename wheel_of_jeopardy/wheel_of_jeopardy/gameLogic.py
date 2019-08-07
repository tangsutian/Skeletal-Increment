from django.shortcuts import render, render_to_response, redirect

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.template import loader
from random import sample
from .forms import startGameForm
from .models import GameSession, User, GameWheel, Category

import os
import random

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MAXSECTORNUM = 11
WHEEL_OF_JEOPARDY = 'Wheel of Jeopardy'
ROUND_TITLE = 'Round Number: '

@require_http_methods(["GET"])
def home(request):
    template = loader.get_template('home.html')
    form = startGameForm()

    GameSession.delete()

    context = {
        'form': form,
        'button_1_text': 'Question Manager',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def wheel(request):
    template = loader.get_template('wheel.html')
    gs = GameSession.objects.all()[0]
    user_1 = gs.User1_profile
    user_2 = gs.User2_profile

    context = {
        'title': '%s | %s%d' % (WHEEL_OF_JEOPARDY, ROUND_TITLE, gs.current_round),
        'current_player': 'Current Player Name: ' + gs.getPlayerTurn().username,
        'number_turns': 'Number of turns: %d, Number of turns remaining: %d' % (gs.turnsTaken(), gs.turnsRemaining()),
        'sector_color': '#baa',
        'button_text': 'Spin Wheel',
        'button_link': 'wheel/spin/%d' % (random.randint(0,MAXSECTORNUM)),
        'classes': ['Round 1 Score', 'Round 2 Score', 'Total Score'],
        'data': gs.getPlayerScoreData(),

    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def spin(request, sector_id):
    template = loader.get_template('wheel2.html')
    wheel = GameWheel.objects.get(pk=request.session['gameWheel'])
    category = wheel.get_sector(sector_id)
    context = {
        'sector_color': '#bab',
        'sector_spun': sector_id,
        'category': category,
        'button_text': 'Go to Game Board',
        'button_link': 'board',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def board(request):
    template = loader.get_template('board.html')
    categories = GameWheel.objects.get(pk=request.session['gameWheel']).get_categories()
    values = []
    for i in range(0, 5):
        values.append(str(i * 200 + 200))
    context = {
        'category_1': categories[0],
        'category_2': categories[1],
        'category_3': categories[2],
        'category_4': categories[3],
        'category_5': categories[4],
        'category_6': categories[5],
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
        'button_link_1': 'right',
        'button_link_2': 'wrong',
        'point_total': '100',
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def questionManager(request):
    template = loader.get_template('questionManager.html')
    context = {
        'button_text': 'Go Back',
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def uploadCSV(request):
    response = redirect('home')
    context = {
        'button_text': 'Go Back',
    }
    return response


@require_http_methods(["GET"])
def right(request, sector_id):
    response = redirect('wheel')
    gs = GameSession.objects.all()[0]
    gs.updatePlayerScore(sector_id)

    return response

@require_http_methods(["GET"])
def wrong(request, sector_id):
    response = redirect('wheel')

    gs = GameSession.objects.all()[0]
    gs.updatePlayerScore(sector_id * -1)
    gs.updatePlayersTurn()
    
    
    return response

@require_http_methods(["POST"])
def start_game_session(request):
    '''
    Called when startGame form is submitted from home page. Stores data to session and redirects to wheel

    :param request: Should contain fields for user names and other pre game information
    :return: returns a redirect response to the game wheel
    '''
    user1 = User.create(request.POST.get('user_1'), True)
    user1.save()
    user2 = User.create(request.POST.get('user_2'), False)
    user2.save()
    '''
    categories = [request.POST.get('category_1'), request.POST.get('category_2'), request.POST.get('category_3'),
                  request.POST.get('category_4'), request.POST.get('category_5'), request.POST.get('category_6'), ]
    '''
    categories = sample(list(Category.objects.all().values()), 6)
    game_session = GameSession.create(user1, user2)
    game_session.save()
    game_wheel = GameWheel.create(categories)
    game_wheel.save()
    request.session['gameSession'] = game_session.id
    request.session['gameWheel'] = game_wheel.id
    response = redirect('wheel')
    return response
