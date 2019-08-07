from django.db import models
from random import randint
import simplejson as json


class Category(models.Model):
    '''
    Stores a category entry. One-to-many relationship with Question.
    '''
    category_title = models.CharField(max_length=200)

    @classmethod
    def create(cls, category):
        for cat in Category.objects.all():
            if cat.category_title == category:
                return cat
        return cls(category_title=category)

    @classmethod
    def deleteAll(cls):
        Category.objects.all().delete()

    def __str__(self):
        return '%s' % (self.category_title)

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
    points = models.IntegerField()

    @classmethod
    def create(cls, q_text, a_text, category, point, session):
        question = cls(question_text=q_text, answer_text=a_text, category=category, points=point, game_session=session)
        return question

    @classmethod
    def deleteAll(cls):
        Question.objects.all().delete()

    def __str__(self):
        return 'Question Object:\n\tQuestion: %s\n\tAnswer: %s\n\tCategory: %s\n\tPoint Total: %d\n\tGame Session: %s' % (self.question_text, self.answer_text, self.category.category_title, self.points, self.game_session)


class User(models.Model):
    '''
    Stores information for a user.
    '''
    username = models.CharField(max_length=20)
    r1_points = models.IntegerField(verbose_name="round1 points")
    r2_points = models.IntegerField()
    free_tokens = models.IntegerField()
    current_turn = models.BooleanField()

    @classmethod
    def create(cls, username, turn):
        user = cls(username=username, r1_points=int(0), r2_points=int(0), free_tokens=int(0), current_turn=turn)
        return user

    @classmethod
    def deleteAll(cls):
        User.objects.all().delete()

    def getTotalScore(self):
        return self.r1_points + self.r2_points

    def getRoundScore(self, round):
        if round == 1:
            return self.r1_points
        elif round == 2:
            return self.r2_points
        else:
            return 0

    def updateRoundScore(self, round, addn):
        if round is 1:
            self.r1_points = self.r1_points + addn
        elif round is 2:
            self.r2_points = self.r2_points + addn


    def getFreeTokenNumber(self):
        return self.free_tokens

    def setTurnState(self, state):
        self.current_turn = state

    def equals(self, user):
        if self.username is user.username:
            return True
        return False

    def getPlayerScoreRow(self):
        return [self.username, self.r1_points, self.r2_points, self.getTotalScore()]

    def __str__(self):
        return 'User-\n\tname: %s\n\tround 1 score: %d\n\tround 2 score: %d\n\tNum Free Tokens: %d\n\tCurrent Turn: %s' % (self.username, self.r1_points, self.r2_points, self.free_tokens, self.current_turn)


class GameWheel(models.Model):
    event_list = ['lose_turn', 'free_turn', 'bankrupt', 'player_choice', 'opponent_choice', 'double_score']
    wheel_sectors = models.TextField(null=True);

    @classmethod
    def create(cls):
        '''
        Default create method with hardcoded categories
        :return: - populated wheel object
        '''

        sample_categories = ['soccer', 'football', 'tennis', 'baseball', 'basketball', 'lacrosse']
        wheel = cls(wheel_sectors=json.dumps(cls.event_list+sample_categories))
        return wheel

    @classmethod
    def create(cls, categories):
        '''
        Alternate constructor accepts a list of categories. To be used with startGame form
        :param categories: - list of categorie names of length=6
        :return: - populated wheel object
        '''
        if not isinstance(categories, list):
            return -1
        wheel = cls(wheel_sectors=json.dumps(cls.event_list+categories))
        return wheel


    def get_spin_result(self):
        jsonDec = json.decoder.JSONDecoder()
        sector_list = jsonDec.decode(self.wheel_sectors)
        x = randint(0,11)
        return {x, sector_list[randint(0, 11)]}

    def get_sector(self, x):
        jsonDec = json.decoder.JSONDecoder()
        sector_list = jsonDec.decode(self.wheel_sectors)
        return sector_list[x]

    def get_categories(self):
        '''
        Retrieves category names
        :return: - list of category titles (list length=6)
        '''
        jsonDec = json.decoder.JSONDecoder()
        sector_list = jsonDec.decode(self.wheel_sectors)
        return sector_list[6:]


class GameSession(models.Model):
    '''
    Stores game session information: number of remaining turns, and IDs of both users.
    '''
    #TODO: discuss desire on delete behavior and proper form of related_names
    #current_user = models.CharField(max_length=30) Should this be handles in the db?
    MAX_NUMBER_OF_TURNS = 50
    number_turns_left = models.IntegerField()
    current_round = models.IntegerField()
    User1_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="one")
    User2_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="two")

    @classmethod
    def create(cls, user1, user2):
        session = cls(User1_profile=user1, User2_profile=user2, current_round=1, number_turns_left=cls.MAX_NUMBER_OF_TURNS)
        return session

    @classmethod
    def delete(cls):
        GameSession.objects.all().delete()

    def nextTurn(self):
        self.number_turns_left = self.number_turns_left - 1
        self.save()

    def turnsRemaining(self):
        return self.number_turns_left

    def turnsTaken(self):
        return self.MAX_NUMBER_OF_TURNS - self.number_turns_left

    def getPlayerTurn(self):
        if self.User1_profile.current_turn is True:
            return self.User1_profile
        return self.User2_profile

    def updatePlayersTurn(self):
        val = self.User1_profile.current_turn
        self.User1_profile.current_turn = self.User2_profile.current_turn
        self.User2_profile.current_turn = val

        self.User1_profile.save()
        self.User2_profile.save()

    def updatePlayerScore(self, points):
        player_to_update = self.getPlayerTurn()
        self.nextTurn()

        player_to_update.updateRoundScore(self.current_round, points)
        player_to_update.save()
        self.save()

    def getPlayerScoreData(self):
        return [self.User1_profile.getPlayerScoreRow(), self.User2_profile.getPlayerScoreRow()]


    # def __init__(self, user1, user2):
    #     self.user1 = user1
    #     self.user2 = user2
    #     self.cur_rount = 0
    #     self.gameWheel = gameWheel()



