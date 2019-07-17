# Skeletal-Increment


Required Packages:
* Python=3.X
* Django=2.X


START GAME
1) Clone repo to local machine
2) Checkout new local branch
3) Navigate to wheel_of_jeopardy folder
4) run: 'python3 manage.py runserver'
5) Open browser of choice
6) Navigate to '127.0.0.1:8000/'
7) Play Wheel Of Jeopardy!

MODEL CHANGES [Django Documentation](https://docs.djangoproject.com/en/2.2/topics/migrations/#workflow)
1) Make changes to wheel_of_jeopardy/wheel_of_jeopardy/models.py
2) Go to '127.0.0.1:8000/'
3) Click 'Reset Game'
4) Navigate to wheel_of_jeopardy folder
5) run: 'python3 manage.py makemigrations wheel_of_jeopardy'
6) run: 'python3 manage.py migrate'
