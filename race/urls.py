from django.urls import path, include
from race import views
urlpatterns = [

    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('explorer/', views.explorer, name='explorer'),
    path('add/', views.add_race, name='add_race'),
    path('profile/', views.profile, name='profile'),
    path('detail/<int:pk>/', views.race_detail, name='detail'),
    path('timeline/', views.timeline, name='timeline'),
    path('search/', views.search_all, name='search'),
    # path('logout/', views.logout, name='andr-logout'),


    # API VIEWS

    path('api/', views.api_root),
    path('api/races/', views.RaceList.as_view(), name='race-list'),
    path('api/races/<int:pk>', views.RaceDetail.as_view(), name='race-detail')
]



