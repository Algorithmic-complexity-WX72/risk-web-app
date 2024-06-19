from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# view to handle AJAX request

@csrf_exempt
def update_suma(request):
    if request.method == 'POST':
        a = request.POST.get('planetName')
        result = suma(a)
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})


# Create your views here.
def home(request):
    sumtotal = 1 + 2
    templateHome = loader.get_template('home.html') #loading template html
    context = {'riskHome' : sumtotal} #passing context to template          #risk is how you call it in html
    return HttpResponse(templateHome.render(context, request)) #returning template with context

    # return HttpResponse(f"result is {sumtotal}")
def app(request):
    a = request.GET.get('planetName', "1")
    app_value = suma(a)
    templateApp = loader.get_template('webapp.html')
    context = {'suma' : app_value }
    return HttpResponse(templateApp.render(context, request))

def suma(a):
    a = int(a)
    trying = a+2
    return trying

# images on the fly, se genera en memoria
#
# plotly
#
# incrustar el svg, funcion de graphviz
#
# networkx a graphviz y luego a svg