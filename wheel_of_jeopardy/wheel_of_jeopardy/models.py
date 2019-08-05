from django.db import models
from random import randint
import simplejson as json


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
    answer_text = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    game_session = models.ForeignKey('GameSession', null=True, blank=True, on_delete=models.SET_NULL)


class User(models.Model):
    '''
    Stores information for a user.
    '''
    username = models.CharField(max_length=20)
    r1_points = models.IntegerField(verbose_name="round1 points")
    r2_points = models.IntegerField()
    free_tokens = models.IntegerField()

    @classmethod
    def create(cls, username):
        user = cls(username=username, r1_points=int(0), r2_points=int(0), free_tokens=int(0))
        return user


class GameWheel(models.Model):

    wheel_sectors = models.TextField(null=True);
    # sector1 = models.CharField(max_length=30)#, default='lose_turn')
    # sector2 = models.CharField(max_length=30)#, default='free_turn')
    # sector3 = models.CharField(max_length=30)#, default='bankrupt')
    # sector4 = models.CharField(max_length=30)#, default='player_choice')
    # sector5 = models.CharField(max_length=30)#, default='opponent_choice')
    # sector6 = models.CharField(max_length=30)#, default='double_score')
    # sector7 = models.CharField(max_length=30)
    # sector8 = models.CharField(max_length=30)
    # sector9 = models.CharField(max_length=30)
    # sector10 = models.CharField(max_length=30)
    # sector11 = models.CharField(max_length=30)
    # sector12 = models.CharField(max_length=30)


    @classmethod
    def create(cls):
        event_list = ['lose_turn', 'free_turn', 'bankrupt', 'player_choice', 'opponent_choice', 'double_score']
        sample_categories = ['soccer', 'football', 'tennis', 'baseball', 'basketball', 'lacrosse']
        wheel = cls(wheel_sectors=json.dumps(event_list+sample_categories))
        return wheel

    # @classmethod
    # def create(cls):
    #     wheel = cls(sector1="lose_turn", sector2="free_turn", sector3="bankrupt", sector4="player_choice",
    #                 sector5="opponent_choice", sector6="double_score", sector7="soccer", sector8="football",
    #                 sector9="tennis", sector10="baseball", sector11="basketball", sector12="lacrosse")
    #     return wheel

    # @classmethod
    # def create(cls, categories):
    #     '''
    #
    #
    #     :param categories: - should be list of length=6 with categories.
    #     :return:
    #     '''

    def get_spin_result(self):
        jsonDec = json.decoder.JSONDecoder()
        sector_list = jsonDec.decode(self.wheel_sectors)
        x = randint(0,11)
        return {x, sector_list[randint(0, 11)]}

    def get_sector(self, x):
        jsonDec = json.decoder.JSONDecoder()
        sector_list = jsonDec.decode(self.wheel_sectors)
        return sector_list[x]



class GameSession(models.Model):
    '''
    Stores game session information: number of remaining turns, and IDs of both users.
    '''
    #TODO: discuss desire on delete behavior and proper form of related_names
    #current_user = models.CharField(max_length=30) Should this be handles in the db?
    turn_number = 60
    User1_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="one")
    User2_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="two")


    @classmethod
    def create(cls, user1, user2):
        session = cls(User1_profile=user1, User2_profile=user2)
        return session


    # def __init__(self, user1, user2):
    #     self.user1 = user1
    #     self.user2 = user2
    #     self.cur_rount = 0
    #     self.gameWheel = gameWheel()




