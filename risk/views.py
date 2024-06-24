import time

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import csv
import random
import graphviz
import os
from django.conf import settings
from collections import defaultdict
from django.templatetags.static import static

# views to handle AJAX request

#XDDD
global_mapa = None

    #Suma
@csrf_exempt
def update_suma(request):
    if request.method == 'POST':
        a = request.POST.get('planetName')
        if a is None:
            return JsonResponse({'error': 'Missing parameter: planetName'})
        result = suma(a)
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def dijkstra_union_view(request):
    global global_mapa
    if request.method == 'POST':
        startPlanet = request.POST.get('startPlanet')
        endPlanet = request.POST.get('endPlanet')
        mapa = global_mapa
        global_mapa = None
        # mapa = request.session.get('mapa')
        #debugging purpouses
        print(f"Mapa in dijkstra_union_view: {mapa}") #The problem is that this is null
        if startPlanet is None or endPlanet is None or mapa is None:
            return JsonResponse({'error': 'Missing parameters or session data'})
        result = dijkstra_union(mapa, startPlanet, endPlanet)
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})



    #Show graph
def ajax_show_graph(request):
    show_graph(request)
    return JsonResponse({'result': 'Graph has been shown'})





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



# Here I have to replace the function of djkstra
# I have to add the input from the first, because here there's only one
def suma(a):
    a = int(a)
    trying = a+2
    return trying

#UNION FUNCTION
def dijkstra_union(mapa, startPlanet, endPlanet):
    distancias, caminos = dijkstra(mapa, startPlanet, endPlanet)
    # You can now use the variables distancias and caminos for further processing
    # For now, let's just return them
    # return distancias, caminos
    print("Dijkstra Union function executed successfully!")
# Here I have to create a function to show the planets

#DJKSTRA

def dijkstra(G, inicio, destino):
    distancias = {nodo: float('inf') for nodo in G}
    distancias[inicio] = 0
    caminos = {nodo: [] for nodo in G}
    visitados = set()

    while len(visitados) < len(G):
        no_visitados = {nodo: distancias[nodo] for nodo in G if nodo not in visitados}
        if not no_visitados:
            break
        nodo_actual = min(no_visitados, key=no_visitados.get)
        visitados.add(nodo_actual)

        for vecino, peso in G[nodo_actual].items():
            nueva_distancia = distancias[nodo_actual] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                caminos[vecino] = caminos[nodo_actual] + [nodo_actual]

    return distancias, caminos

def generar_grafo(csv_file, total_nodes):

    G = {}
    # Leer el archivo CSV y seleccionar nodos aleatorios
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader if len(line) >= 2]
        lines = random.sample(lines, total_nodes)

        # Agregar nodos al grafo
        for line in lines:
            node_name, _ = line
            G[node_name] = {}

        # Asignar distancias aleatorias entre nodos
        for i in range(len(lines)):
            for j in range(i+1, len(lines)):
                distance = random.randint(1, 20)
                G[lines[i][0]][lines[j][0]] = distance
                #G[lines[j][0]][lines[i][0]] = distance

    return G

def dibujar_grafo(G):
    print('dibujar_grafo function called')
    dot = graphviz.Graph()

    # Agregar nodos al grafo
    for node in G:
        dot.node(node)

    # Agregar aristas al grafo
    for node in G:
        for neighbor, weight in G[node].items():
            dot.edge(node, neighbor, label=str(weight))

    # # Mostrar grafo
    # svg_filename = 'grafo.svg'
    # svg_path = os.path.join(settings.STATIC_ROOT, svg_filename)
    # dot.render(svg_path, format='svg', view=False)
    # print(f'SVG path in dibujar_grafo: {svg_path}')
    # return svg_path


    # Mostrar grafo
    svg_filename = 'grafo.svg'
    svg_path = os.path.join(settings.STATIC_ROOT, svg_filename)

    # Generate SVG data
    svg_data = dot.pipe(format='svg')

    # Write SVG data to file
    with open(svg_path, 'wb') as f:
        f.write(svg_data)

    print(f'SVG path in dibujar_grafo: {svg_path}')
    return svg_path



def show_graph(request):
    global global_mapa
    dataset = "C:\\Users\\Janiel Franz\\Desktop\\UPC\\Algorithmic Complexity\\web-app-definitive\\djangoProject1\\risk\\names.csv"
    nodos_totales = 6
    mapa = generar_grafo(dataset, nodos_totales)
    global_mapa = mapa

    # guardando variable de mapa
    # request.session['mapa'] = mapa #this is the problem
    #debugging purpouses
    print(f"Mapa in show_graph: {mapa}") #this is not null
    # draw the  planets
    svg_path = dibujar_grafo(mapa)
    #returns json response
    if svg_path is not None:
        timestamp = int(time.time())
        svg_url = request.build_absolute_uri(static('grafo.svg')) + f'?{timestamp}'
        print(f'SVG path: {svg_path}')
        print(f'SVG URL: {svg_url}')
        return JsonResponse({'result': 'Graph has been shown', 'svg_url': svg_url})
    else:
        return JsonResponse({'error': 'SVG path is undefined'})