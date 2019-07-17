from django.db import models


class Category(models.Model):
    '''
    Stores a category entry. One-to-many relationship with Question.
    '''
    category_title = models.CharField(max_length=200)


class Question(models.Model):
    '''
    Stores a single question and ties it to a category. Many-to-one relationship with Category.

    GameSession used as optional secondary foreign key, allows a list of already asked questions to be maintained
    during the game.
    '''
    question_text = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    game_session = models.ForeignKey('GameSession', null=True, blank=True, on_delete=models.SET_NULL)

class Answer(models.Model):
    '''
    Stores the answer to a question. One-to-one relationship with Question.
    '''
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)


class User(models.Model):
    '''
    Stores information for a user.
    '''
    username = models.CharField(max_length=20)
    total_points = models.IntegerField
    r1_points = models.IntegerField
    r2_points = models.IntegerField
    free_tokens = models.IntegerField
    current_turn = models.BooleanField


class GameSession(models.Model):
    '''
    Stores game session information: number of remaining turns, and IDs of both users.
    '''
    #TODO: discuss desire on delete behavior and proper form of related_names
    #current_user = models.CharField(max_length=30) Should this be handles in the db?
    turns_remaining = models.IntegerField
    User1_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one')
    User2_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="two")

