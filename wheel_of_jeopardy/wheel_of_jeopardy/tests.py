from django.test import TestCase
from .models import Question, GameSession, GameWheel, Category, User


class QuestionModelTests(TestCase):

    def setUp(self):
        category = Category(category_title='Math')
        category.save()
        question_text = 'what is 2+2?'
        question_answer = '4'
        question = Question.create(question_text, question_answer, category, 100, None)
        question.save()

    def test_create_question(self):
        """
        tests question constructor
        :return: Question
        """
        question = Question.objects.get(id=1)
        self.assertTrue(isinstance(question, Question))

    def test_get_queestion_text(self):
        question = Question.objects.get(id=1)
        self.assertEqual('what is 2+2?', question.question_text)


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
