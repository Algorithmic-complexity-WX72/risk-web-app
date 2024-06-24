from django.urls import path
from risk import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("risk/home", views.home, name="risk"), #join views
    path("risk/app",views.app, name ="risk app"),

    #API
    path("risk/update_suma", views.update_suma, name="update_suma"),
    path("risk/show_graph", views.ajax_show_graph, name="show_graph"),
    path('risk/dijkstra_union_view', views.dijkstra_union_view, name='dijkstra_union_view'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)