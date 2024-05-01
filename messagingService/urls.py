from django.urls import path
from messagingService import views

urlpatterns = [
    path('users/<str:name>/messages/', views.messages),
    path('users/<str:name>/messages/<int:id>', views.delete_message),
    path('users/', views.users)
]