from django.test import TestCase
from .models import Question, GameSession, GameWheel, Category, User


class QuestionModelTests(TestCase):

    def setUp(self):
        category = Category(category_title='Math')
        category.save()
        question_text = 'what is 2+2?'
        question_answer = '4'
        question = Question.create(question_text, question_answer, category, 100, None, 1)
        question.save()

        question_text = 'what is 5-3?'
        question_answer = '2'
        question2 = question.create(question_text, question_answer, category, 200, None, 1)
        question2.save()


    def test_create_question(self):
        """
        tests question constructor
        :return: Question
        """
        question = Question.objects.get(id=1)
        self.assertTrue(isinstance(question, Question))

    def test_get_question_text(self):
        question = Question.objects.get(id=1)
        self.assertEqual('what is 2+2?', question.question_text)

    def test_get_questions_in_category(self):
        cat = Category.objects.get(id=1)
        questions = Question.getQuestionsInCategory(cat.category_title)
        self.assertEqual(questions.__len__(), 2)


class GameWheelTests(TestCase):

    def setUp(self):
        #GameWheel.objects.create(GameWheel.create(['test1', 'test2', 'test3', 'test4', 'test5', 'test6']))
        wheel = GameWheel.create(['test1', 'test2', 'test3', 'test4', 'test5', 'test6'])
        wheel.save()

    def test_create_wheel(self):
        """
        Test that a wheel was able to be created and accessed
        :return:
        """
        wheel = GameWheel.objects.get(id=1)
        self.assertTrue(isinstance(wheel, GameWheel))

    def test_get_sector(self):
        wheel = GameWheel.objects.get(id=1)
        self.assertEqual(wheel.get_sector(6), 'test1')



class UserTests(TestCase):

    def setUp(self):
        user = User.create("testuser", False)
        user.save()

    def test_create_user(self):
        """
        Tests that we were able to successfully create a user
        :return:
        """
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'testuser')

    def test_total_score(self):
        user = User.objects.get(id=1)
        user.updateRoundScore(1, 500)
        user.updateRoundScore(2, 500)
        self.assertEqual(user.getTotalScore(), 1000)



class GameSessionTests(TestCase):

    def setUp(self):
        user1 = User.create("testuser1", True)
        user2 = User.create("testuser2", False)
        user1.save()
        user2.save()
        session = GameSession.create(user1, user2)
        session.save()

    def test_create_session(self):
        """
        Tests that we were able to successfully create a GameSession
        :return:
        """
        session = GameSession.objects.get(id=1)
        self.assertIsNotNone(session)

    def test_increment_turn(self):
        session = GameSession.objects.get(id=1)
        x = session.number_turns_left
        session.nextTurn()
        y = session.number_turns_left
        self.assertLess(y, x)

    def test_increment_player_tokens(self):
        """
        Tests that free tokens can be added and used
        :return:
        """
        session = GameSession.objects.get(id=1)
        a = session.getNumPlayerFreeTokens()
        session.incrementPlayerTokenNumber()
        b = session.getNumPlayerFreeTokens()
        self.assertGreater(b, a)

    def test_decrement_player_tokens(self):
        session = GameSession.objects.get(id=1)
        session.incrementPlayerTokenNumber()
        a = session.getNumPlayerFreeTokens()
        session.decrementPlayerTokenNumber()
        b = session.getNumPlayerFreeTokens()
        self.assertLess(b, a)

    def test_double_player_round_score(self):
        session = GameSession.objects.get(id=1)
        session.updatePlayerScore(500)
        a = session.getCurrentPlayerScore()
        session.doublePlayerRoundScore()
        b = session.getCurrentPlayerScore()
        self.assertEqual(2*a, b)

    def test_clear_player_round_score(self):
        session = GameSession.objects.get(id=1)
        session.updatePlayerScore(500)
        session.clearPlayerRoundScore()
        a = session.getCurrentPlayerScore()
        self.assertEqual(a, 0)