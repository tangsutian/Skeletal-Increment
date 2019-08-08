from django.shortcuts import render, render_to_response, redirect

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.template import loader
from random import sample
from .forms import startGameForm
from .models import GameSession, User, GameWheel, Category, Question

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
    gs = GameSession.objects.all()[0]
    user_1 = gs.User1_profile
    user_2 = gs.User2_profile
    gs.updateCurrentRound()

    if gs.current_round == GameSession.GAME_OVER:
        winner_text = 'Player %s is the winner! Good Job!'
        tie_text = 'Player %s and Player %s tie!'
        game_over_text = 'GAME OVER!'

        template = loader.get_template('game_over.html')
        winner = gs.getWinner()
        text = ''
        if winner == None:
            text = tie_text % (gs.User1_profile.username, gs.User2_profile.username)
        else:
            text = winner_text % (winner.username)

        d = []
        for e in gs.getPlayerScoreData():
            d.append(e[0:-1])

        context = {
            'game_over_text': game_over_text,
            'winner_text': text,
            'classes': User.getPlayerTableHeaders()[0:-1],
            'data': d,
            'button_link': 'home',
            'button_text': 'Go Home',
        }

    else:
        template = loader.get_template('wheel.html')
        context = {
            'title': '%s | %s%d' % (WHEEL_OF_JEOPARDY, ROUND_TITLE, gs.current_round),
            'current_player': 'Current Player Name: ' + gs.getPlayerTurn().username,
            'number_turns': 'Number of turns: %d, Number of turns remaining: %d' % (gs.turnsTaken(), gs.turnsRemaining()),
            'sector_color': '#baa',
            'button_text': 'Spin Wheel',
            'button_link': 'wheel/spin/%d' % (random.randint(0,MAXSECTORNUM)),
            'classes': User.getPlayerTableHeaders(),
            'data': gs.getPlayerScoreData(),

        }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def spin(request, sector_id):
    template = loader.get_template('wheel2.html')
    wheel = GameWheel.objects.get(pk=request.session['gameWheel'])


    print("wheel.get_categories(): " + str(wheel.get_categories()))
    sector_obj = wheel.get_sector(sector_id)
    print("GET spin() called with sector_id: " + str(sector_id) + " and sector_obj: " + sector_obj)

    context = {
        'sector_color': '#bab',
        'sector_spun': sector_obj,
        'categories': wheel.get_categories()
    }

    if sector_obj == "bankrupt":
        return bankrupt(request)
    elif sector_obj == "double_score":
        return double_score(request)
    elif sector_obj == "free_turn":
        return free_turn(request)
    elif sector_obj == "lose_turn":
        return lose_turn(request)
    elif sector_obj == "opponent_choice":
        return HttpResponse(template.render(context, request)) # TODO Implement
    elif sector_obj == "player_choice":
        return HttpResponse(template.render(context, request)) # TODO Implement
    else: # If the wheel spin was a category, forward right to the question page
        get_info = request.GET.copy()
        get_info["category"] = sector_obj
        request.GET = get_info
        return question(request)



def use_token(request):
    gss = GameSession.objects.all()
    gs = gss[0]
    gs.decrementPlayerTokenNumber()
    return wheel(request)


def save_token(request):
    gss = GameSession.objects.all()
    gs = gss[0]
    gs.updatePlayersTurn()
    return wheel(request)

def lose_turn(request):
    gss = GameSession.objects.all()
    gs = gss[0]
    hasToken = gs.playerHasTokenLeft()
    player = gs.getPlayerTurn()
    gs.nextTurn()
    if(hasToken):
        template = loader.get_template("lose_turn_has_token.html")
        numTokens = gs.getNumPlayerFreeTokens()
        context = {
            'sector_color': '#bab',
            'use_token_button_text': 'Use Free Turn Token',
            'save_token_button_text': 'Save Free Turn Token',
            'player': player.username,
            'free_tokens': numTokens,
        }
    else:
        template = loader.get_template("lose_turn_no_token.html")
        gs.updatePlayersTurn()
        context = {
            'sector_color': '#bab',
            'player': player.username,
            'button_text': 'Next Turn',
            'button_link': 'wheel',
        }
    return HttpResponse(template.render(context, request))

def free_turn(request):
    template = loader.get_template("free_turn.html")
    gss = GameSession.objects.all()
    gs = gss[0]
    gs.incrementPlayerTokenNumber()
    player = gs.getPlayerTurn()
    tokens = gs.getNumPlayerFreeTokens()
    context = {
        'sector_color': '#bab',
        'button_text': 'Next Turn',
        'button_link': 'wheel',
        'player': player.username,
        'free_tokens': tokens,
    }
    return HttpResponse(template.render(context, request))

def bankrupt(request):
    template = loader.get_template("bankrupt.html")
    gss = GameSession.objects.all()
    gs = gss[0]
    gs.clearPlayerRoundScore()
    gs.updatePlayersTurn()
    context = {
        'sector_color': '#bab',
        'button_text': 'Next Turn',
        'button_link': 'wheel',
    }
    return HttpResponse(template.render(context, request))

def double_score(request):
    template = loader.get_template("double_score.html")
    gss = GameSession.objects.all()
    gs = gss[0]
    gs.doublePlayerRoundScore()
    player = gs.getPlayerTurn()
    score = gs.getCurrentPlayerScore()
    #gs.updatePlayersTurn()
    context = {
        'sector_color': '#bab',
        'button_text': 'Next Turn',
        'button_link': 'wheel',
        'player': player.username,
        'new_score': score,
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def board(request):
    template = loader.get_template('board.html')
    categories = GameWheel.objects.get(pk=request.session['gameWheel']).get_categories()
    print(categories)

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

def question(request, category):
    get_info = request.GET.copy()
    get_info["category"] = category
    request.GET = get_info
    return question(request)


@require_http_methods(["GET"])
def question(request, **kwargs):
    print("GET QUESTION")
    category = kwargs.get('category', None)
    if not category:
        category = request.GET.get('category', '')


    if(category):
        print("GET question() called with category: " + category)
    else:
        print("ERROR! Question page called without a category")
        category = GameWheel.objects.all()[0].get_categories()[0]

    print(category)

    round = GameSession.objects.all()[0].current_round
    question = Question.getNextQuestionForCategory(category, round)
    print(question)
    if question == None:
        return redirect('wheel')
        
    question.setAsked()

    template = loader.get_template('question.html')
    context = {
        'category': question.category,
        'question_text': question.question_text,
        'button_1_text': 'Right',
        'button_1_color': 'green',
        'button_2_text': 'Wrong',
        'button_2_color': 'red',
        'button_link_1': 'right',
        'button_link_2': 'wrong',
        'point_total': '100',
    }
    print("GET QUESTION END")

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
    gss = GameSession.objects.all()
    gs = None
    if len(gss) == 1:
        gs = gss[0]
    handleQuestionCSV(request.FILES['csv_file'], gs)
    response = redirect('home')
    return response

@require_http_methods(["GET"])
def right(request, sector_id):
    response = redirect('wheel')
    gs = GameSession.objects.all()[0]
    gs.updatePlayerScore(sector_id)

    return response

@require_http_methods(["GET"])
def wrong(request, sector_id):
    gs = GameSession.objects.all()[0]
    gs.updatePlayerScore(sector_id * -1)

    if gs.playerHasTokenLeft():
        response = redirect('token')
    else:
        response = redirect('wheel')

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

    categories = [Category.objects.get(pk=request.POST.get('category_1')).category_title,
                    Category.objects.get(pk=request.POST.get('category_2')).category_title,
                    Category.objects.get(pk=request.POST.get('category_3')).category_title,
                    Category.objects.get(pk=request.POST.get('category_4')).category_title,
                    Category.objects.get(pk=request.POST.get('category_5')).category_title,
                    Category.objects.get(pk=request.POST.get('category_6')).category_title,]

    game_session = GameSession.create(user1, user2)
    game_session.save()

    for q in Question.objects.all():
        q.game_session = game_session
        q.save()
        print(q)

    game_session.incrementPlayerTokenNumber()
    game_wheel = GameWheel.create(categories)
    game_wheel.save()
    request.session['gameSession'] = game_session.id
    request.session['gameWheel'] = game_wheel.id
    response = redirect('wheel')
    return response


def handleQuestionCSV(file, gs):
    lines = file.read().decode('UTF-8').split('\n')
    for l in lines:
        s = str(l).strip().split('`')
        if s[3] == 'Question_Text':
            continue
        cat = Category.create(s[2])
        cat.save()
        question = Question.create(s[3],s[4],cat,int(s[1]),gs,int(s[0]))
        question.save()


@require_http_methods(["GET"])        
def token1(request):
    template = loader.get_template('token.html')
    context = {
        'button_link_1': 'decrementToken',
        'button_link_2': 'wheel',
        'button_1_text': 'Yes',
        'button_2_text': 'No',
        'question_text': 'Would you like to use a free turn token? You have %d left' % GameSession.objects.all()[0].getOtherPlayerTokensLeft()
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])        
def token2(request):
    gs = GameSession.objects.all()[0]
    gs.updatePlayersTurn()
    gs.decrementPlayerTokenNumber()
    return redirect('wheel')

@require_http_methods(["GET"])
def gameOver(request):
    return redirect('home')
