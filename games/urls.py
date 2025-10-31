from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Games home
    path('', views.games_home, name='games_home'),

    # Mad Libs
    path('madlibs/', views.madlibs_list, name='madlibs_list'),
    path('madlibs/<int:template_id>/', views.madlibs_play, name='madlibs_play'),
    path('madlibs/<int:template_id>/submit/', views.madlibs_submit, name='madlibs_submit'),
    path('madlibs/result/<str:share_code>/', views.madlibs_result, name='madlibs_result'),

    # API
    path('api/random-word/<str:part_of_speech>/', views.api_random_word, name='api_random_word'),
]
