from django.urls import path

from risk import views

urlpatterns =[
    path("risk/", views.suma, name="risk") #join views

]