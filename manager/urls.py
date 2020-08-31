from django.urls import path, include
from manager import views

urlpatterns = [
    path('', views.index,  name='manager-index'),

    path('group/new/', views.GroupCreate.as_view(), name='group-new'),
    path('group/<int:pk>/', views.GroupDetail.as_view(), name='group-detail'),
    path('group/<int:pk>/edit', views.GroupUpdate.as_view(), name='group-update'),
    path('group/<int:pk>/edit_members', views.group_edit_members, name='group-edit-members'),
    path('group/<int:pk>/edit_month_plan_training', views.group_edit_plan_training, name='group-edit-plan-training'),

    path('member/new/', views.MemberCreate.as_view(), name='member-new'),
    path('member/<int:pk>/', views.MemberDetail.as_view(), name='member-detail'),
    path('member/<int:pk>/edit', views.MemberUpdate.as_view(), name='member-update'),

    path('staff/new/', views.StaffCreate.as_view(), name='staff-new'),
    path('staff/<int:pk>/', views.StaffDetail.as_view(), name='staff-detail'),
    path('staff/<int:pk>/edit', views.StaffUpdate.as_view(), name='staff-update'),

    path('training/new/', views.TrainingCreate.as_view(), name='training-new'),
    path('training/<int:pk>/edit', views.TrainingUpdate.as_view(), name='training-update'),
    path('training/<int:pk>/', views.TrainingDetail.as_view(), name='training-detail'),

    path('onetrainingplan/new/', views.OneTrainingPlanCreate.as_view(), name='one-training-plan-new'),
    path('onetrainingplan/<int:pk>/edit', views.OneTrainingPlanUpdate.as_view(), name='one-training-plan-update'),
    path('onetrainingplan/<int:pk>/', views.OneTrainingPlanDetail.as_view(), name='one-training-plan-detail'),

    path('monthplan/new/', views.MonthPlanCreate.as_view(), name='month-plan-new'),
    path('monthplan/<int:pk>/edit', views.MonthPlanUpdate.as_view(), name='month-plan-update'),
    path('monthplan/<int:pk>/', views.MonthPlanDetail.as_view(), name='month-plan-detail'),

    path('monthtraingingplan/<int:pk>/', views.MonthTrainingPlanDetail.as_view(), name='month-training-plan-detail'),
    path('monthtraingingplan/<int:pk>/edit', views.MonthTrainingPlanUpdate.as_view(), name='month-training-plan-update'),
    path('monthtraingingplan/new/', views.MonthTrainingPlanCreate.as_view(), name='month-training-plan-new'),


    path('profile/', views.profile, name='profile')
]
