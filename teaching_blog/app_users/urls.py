from django.urls import path
from app_users import views
from django.urls import path
from .views import chat_View
 
# app_name = 'app_users'
urlpatterns = [

    path('',views.HomeView.as_view(),name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('contact/', views.ContactView.as_view(), name="contact"),
     path('simple-form/', views.simple_form_view, name='simple_form'),
    #  path('chat/', chat_View.as_view(), name='chat'),
     path('chat/', views.chat_View, name='chat'),
    path('chat_page/', views.chat_page, name='chat_page'),
]
