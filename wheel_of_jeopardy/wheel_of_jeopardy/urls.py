"""wheel_of_jeopardy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
admin.autodiscover()
from wheel_of_jeopardy import gameLogic


extra_patterns = [
    path('', gameLogic.wheel, name='wheel'),
    path('spin/<int:sector_id>/', gameLogic.spin, name='spin'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', gameLogic.home, name='home'),
    path('wheel/', include(extra_patterns)),
    path('board/', gameLogic.board, name='board'),
    path('question/', gameLogic.question, name='question'),
    path('questionManager/', gameLogic.questionManager, name='questionManager'),
    path('', gameLogic.home, name='home'),
    path('startGameSession/', gameLogic.start_game_session, name='startGame'),
]
