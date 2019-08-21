from django.shortcuts import render, render_to_response, redirect

# Create your views here.    
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.template import loader
from random import sample
from .forms import startGameForm
from .models import GameSession, User, GameWheel, Category, Question, MAX_QUESTIONS_PER_CATEGORY, MAX_NUMBER_OF_QUESTIONS_PER_ROUND
from django.core.files import File

import os
import random

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MAXSECTORNUM = 11
WHEEL_OF_JEOPARDY = 'Wheel of Jeopardy'
ROUND_TITLE = 'Round: '

@require_http_methods(["GET"])
def home(request):
    template = loader.get_template('home.html')
    form = startGameForm()

    GameSession.delete()

    context = {
        'form': form,
        'page_title': 'Home Page',
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


        context = {
            'game_over_text': game_over_text,
            'winner_text': text,
            'classes': User.getPlayerTableHeaders(),
            'data': gs.getPlayerScoreData(),
            'button_text': 'Go Home',
            'page_title': 'Game Over',
        }

    else:
        template = loader.get_template('wheel.html')
        categories = GameWheel.objects.get(pk=request.session['gameWheel']).get_categories()
        values = Question.getQuestionPointsLeftInCategory(categories, gs.current_round)
        context = {
            'title': '%s | %s%d' % (WHEEL_OF_JEOPARDY, ROUND_TITLE, gs.current_round),
            'current_player': 'Current Player: ' + gs.getPlayerTurn().username,
            'number_turns': 'Number of turns: %d, Number of turns remaining: %d' % (gs.turnsTaken(), gs.turnsRemaining()),
            'button_text': 'Spin Wheel',
            'sector_val': '%d' % (random.randint(0,MAXSECTORNUM)),
            'classes': User.getPlayerTableHeaders(),
            'data': gs.getPlayerScoreData(),
            'categories': categories,
            'point_totals': values,
            'page_title': 'Wheel Board',
        }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def spin(request, sector_id):
    template = loader.get_template('wheel2.html')
    wheel = GameWheel.objects.get(pk=request.session['gameWheel'])

    sector_obj = wheel.get_sector(sector_id)
    print("GET spin() called with sector_id: " + str(sector_id) + " and sector_obj: " + sector_obj)

    if sector_obj == "bankrupt":
        return bankrupt(request)
    elif sector_obj == "double_score":
        return double_score(request)
    elif sector_obj == "free_turn":
        return free_turn(request)
    elif sector_obj == "lose_turn":
        return lose_turn(request)
    elif sector_obj == "opponents_choice":
        return HttpResponse(template.render(context, request)) # TODO Implement
    elif sector_obj == "players_choice":
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
            'use_token_button_text': 'Use Free Turn Token',
            'save_token_button_text': 'Save Free Turn Token',
            'player': player.username,
            'free_tokens': numTokens,
            'page_title': 'Token Management',
        }
    else:
        template = loader.get_template("lose_turn_no_token.html")
        gs.updatePlayersTurn()
        context = {
            'player': player.username,
            'button_text': 'Next Turn',
            'page_title': 'Token Management',
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
        'player': player.username,
        'new_score': score,
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def board(request):
    template = loader.get_template('board.html')
    categories = GameWheel.objects.get(pk=request.session['gameWheel']).get_categories()
    round = GameSession.objects.all()[0].current_round
    values = Question.getQuestionPointsLeftInCategory(categories, round)

    context = {
        'categories': categories,
        'point_totals': values,
        'button_text': 'Show Question!',
        'page_title': 'Category Selection',
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def question(request):
    category = request.GET.get('category', '')
   
    if not category:
        return redirect('wheel')

    round = GameSession.objects.all()[0].current_round
    Question.getQuestionPointsLeftInCategory(category, round)
    question = Question.getNextQuestionForCategory(category, round)

    if question == None:
        return redirect('wheel')
        
    question.setAsked(True)

    template = loader.get_template('question.html')
    context = {

        #'sector_id': GameWheel.objects.get(pk=request.session['gameWheel']).get_sector_num(category),
        'sector_id': 11,
        'category': question.category.category_title,
        'question_text': question.question_text,
        'button_text': 'Show Answer',
        'question_pk': question.pk,
        'point_total': question.points,
        'page_title': 'Question Time',
        'timeout_duration': 15,
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def answer(request, pk):
    template = loader.get_template('answer.html')
    question = Question.getQuestionWithPK(pk)
    txt = 'this is the answer'

    context = {
        'page_title': 'Answer',
        'answer_text': question.answer_text,
        'button_1_text': 'Right',
        'button_2_text': 'Wrong',
        'point_val': question.points,
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def questionManager(request):
    template = loader.get_template('questionManager.html')
    context = {
        'button_text': 'Go Back',
        'questions': Question.getAllQuestions(),
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def uploadCSV(request):

    if '_home' in request.POST:
        return redirect('home')
    elif '_delete' in request.POST:
        Category.deleteAll()
        Question.deleteAll()
        return redirect('questionManager')
    elif len(request.FILES) == 0:
        return redirect('questionManager')

    gss = GameSession.objects.all()
    gs = None
    if len(gss) == 1:
        gs = gss[0]
    handleQuestionCSV(request.FILES['csv_file'], gs)
    return redirect('home')

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
    if '_questionManager' in request.POST:
        response = redirect('questionManager')
        return response
    else:
        form = startGameForm(request.POST)
        form.fields['user_1'].required = True
        form.fields['user_2'].required = True
        form.fields['category_1'].required = True
        form.fields['category_2'].required = True
        form.fields['category_3'].required = True
        form.fields['category_4'].required = True
        form.fields['category_5'].required = True
        form.fields['category_6'].required = True

        txt = ''
        if not form.is_valid():
            txt = 'Please enter all fields before starting the game!'
        elif not checkUnique(form):
            txt = 'All categories must be unique before starting the game!'
        elif not checkCategoriesFull(form):
            txt = 'All catgories must have 5 questions in each round!'

        if txt is not '':
            template = loader.get_template('home.html')
            context = {
                'form': form,
                'page_title': 'Home Page',
                'error_text': txt,
            }
            return HttpResponse(template.render(context, request))

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

    for ca in categories:
        for q in Question.getQuestionsInCategory(ca):
            q.game_session = game_session
            q.setAsked(False)
            q.save()

    game_wheel = GameWheel.create(categories)
    game_wheel.save()
    request.session['gameSession'] = game_session.id
    request.session['gameWheel'] = game_wheel.id
    response = redirect('wheel')
    return response

def checkUnique(startform):
    lst = [startform.cleaned_data['category_1'], startform.cleaned_data['category_2'], startform.cleaned_data['category_3'], startform.cleaned_data['category_4'], startform.cleaned_data['category_5'], startform.cleaned_data['category_6']]
    
    return len(set(lst)) == len(lst)

def checkCategoriesFull(startform):
    categories = ['category_1', 'category_2', 'category_3', 'category_4', 'category_5', 'category_6']

    for cat in categories:
        cc = startform.cleaned_data[cat]
        roundqs = Question.getQuestionsInCategoryAndRound(cc, 1)
        allqs = Question.getQuestionsInCategory(cc)
        if len(roundqs) != MAX_NUMBER_OF_QUESTIONS_PER_ROUND:
            return False
        if len(allqs) != MAX_QUESTIONS_PER_CATEGORY:
            return False
    return True


def handleQuestionCSV(file, gs):
    lines = file.read().decode('UTF-8').split('\n')
    for l in lines:
        if l.strip() == '' or l[0] == '#':
            continue
        s = str(l).strip().split('`')
        if s[3] == 'Question_Text':
            continue

        cat = Category.create(s[2])
        if cat is None:
            print('Could not add the category name: %s' % (s[2]))
            continue
        cat.save()

        question = Question.create(s[3],s[4],cat,int(s[1]),gs,int(s[0]))
        if question is None:
            print('Could not add the question: %s,%s,%s,%s' % (s[3], cat.category_title, s[1], s[0]))
            continue
        question.save()


@require_http_methods(["GET"])        
def token1(request):
    template = loader.get_template('token.html')
    context = {
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

@require_http_methods(["GET"])
def download_example_csv(request):
    filename = './wheel_of_jeopardy/Demo/WheelOfJeopardy-ExampleQuestions.txt'

    f = open(filename, 'r')
    myfile = File(f)
    response = HttpResponse(myfile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + filename.split('/')[-1]
    return response
