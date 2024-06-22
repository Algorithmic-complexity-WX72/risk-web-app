from django.urls import path
from risk import views

urlpatterns =[
    path("risk/home", views.home, name="risk"), #join views
    path("risk/app",views.app, name ="risk app"),

    #API
    path("risk/update_suma", views.update_suma, name="update_suma"),
    path("risk/show_graph", views.ajax_show_graph, name="show_graph")

]