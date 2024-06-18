from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def home(request):
    sumtotal = 1 + 2
    templateHome = loader.get_template('home.html') #loading template html
    context = {'riskHome' : sumtotal} #passing context to template          #risk is how you call it in html
    return HttpResponse(templateHome.render(context, request)) #returning template with context

    # return HttpResponse(f"result is {sumtotal}")
def app(request):
    app_value = suma()
    templateApp = loader.get_template('webapp.html')
    context = {'suma' : app_value }
    return HttpResponse(templateApp.render(context, request))

def suma():
    trying = 1+2
    return trying