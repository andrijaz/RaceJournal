from django.urls import path, include
from race import views, api_views
urlpatterns = [

    path('index/', views.index, name='index'),
    path('explorer/', views.explorer, name='explorer'),
    path('add/', views.add_race, name='add_race'),
    path('profile/', views.profile, name='profile'),
    path('detail/<int:pk>/', views.race_detail, name='detail'),
    path('timeline/', views.timeline, name='timeline'),
    path('search/', views.search_all, name='search'),

    path('login/', views.login_view, name='andr-login'),
    path('logout/', views.logout_view, name='andr-logout'),
    path('register/', views.register, name='register'),

    # API VIEWS

    path('api/', api_views.api_root),

    path('api/races/', api_views.RaceList.as_view(), name='race-list'),
    path('api/races/<int:pk>', api_views.RaceDetail.as_view(), name='race-detail'),

    path('api/profiles/', api_views.ProfileList.as_view(), name='profile-list'),
    path('api/profiles/<int:pk>', api_views.ProfileDetail.as_view(), name='profile-detail'),

    path('api/user/', api_views.UserList.as_view(), name='user-list'),
    path('api/user/<int:pk>', api_views.UserDetail.as_view(), name='user-detail'),

    path('api/trophy/', api_views.TrophyList.as_view(), name='trophy-list'),
    path('api/trophy/<int:pk>', api_views.TrophyDetail.as_view(), name='trophy-detail'),

    path('api/userraces/<int:pk>', api_views.UserRacesDetail.as_view(), name='userraces-detail'),
    path('api/userraces/', api_views.UserRacesList.as_view(), name='userraces-list'),

    path('api/usertrophy/<int:pk>', api_views.UserTrophyDetail.as_view(), name='usertrophy-detail'),
    path('api/usertrophy/', api_views.UserTrophyList.as_view(), name='usertrophy-list'),

]



