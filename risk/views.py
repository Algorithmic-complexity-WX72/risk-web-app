from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def suma(request):
    sumtotal = 1 + 2
    template = loader.get_template('webapp.html') #loading template html
    context = {'risk' : sumtotal} #passing context to template          #risk is how you call it in html
    return HttpResponse(template.render(context, request)) #returning template with context

    # return HttpResponse(f"result is {sumtotal}")