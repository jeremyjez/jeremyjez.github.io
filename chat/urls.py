from django.contrib.auth.views import logout
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('logout/', logout, {'next_page': 'index'}, name='logout'),
    path('register/', views.register_view, name='register'),



    path("", views.index, name="index"),
    path("news-details/<str:news>", views.news_details, name="newsdetails"),
    path("news/", views.news, name="news"),
    path("news/next-page/<int:nmbr>", views.npage, name="npage"),
    path("news/previous-page/<int:nmbr>", views.ppage, name="ppage"),
    path("events/", views.events, name="events"),
    path("events/next-page/<int:nmbr>", views.enpage, name="enpage"),
    path("eventsS/previous-page/<int:nmbr>", views.eppage, name="eppage"),


    path("logout/", views.student_logout, name="logout"),
    path("login/", views.student_login, name="login"),
]
