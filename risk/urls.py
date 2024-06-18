from django.urls import path

from risk import views

urlpatterns =[
    path("risk/home", views.home, name="risk"), #join views
    path("risk/app",views.app, name ="risk app")

]