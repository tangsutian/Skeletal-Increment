from django.db import models


class Category(models.Model):
    '''
    Stores a category entry. One-to-many relationship with Question.
    '''
    category_title = models.CharField(max_length=200)


class Answer(models.Model):
    '''
    Stores the answer to a question. One-to-one relationship with Question.
    '''
    answer_text = models.CharField(max_length=200)


class Question(models.Model):
    '''
    Stores a single question and ties it to:
      category -> Many-to-one relationship with Category.
      answer -> One-to-One relationship with Answer

    GameSession used as optional secondary foreign key, allows a list of already asked questions to be maintained
    during the game.
    '''
    question_text = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    point_value = models.IntegerField
    asked = models.BooleanField(default=False)

    ROUND_NUMBER = (
            ('1', 'One'),
            ('2', 'Two'),
        )
    round_number = models.CharField(max_length=1, choices=ROUND_NUMBER)
    game_session = models.ForeignKey('GameSession', null=True, blank=True, on_delete=models.SET_NULL)


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
    User1_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    User2_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")

