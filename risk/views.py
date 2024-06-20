from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import csv
import random
import graphviz
from collections import defaultdict


# view to handle AJAX request

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
                distance = random.randint(10, 20)
                G[lines[i][0]][lines[j][0]] = distance
                G[lines[j][0]][lines[i][0]] = distance

    return G

def dibujar_grafo(G):
    dot = graphviz.Graph()

    # Agregar nodos al grafo
    for node in G:
        dot.node(node)

    # Agregar aristas al grafo
    for node in G:
        for neighbor, weight in G[node].items():
            dot.edge(node, neighbor, label=str(weight))

    # Mostrar grafo
    dot.render('grafo', format='svg', view=True)

def dijkstra(G, inicio, destino):
    distancias = {nodo: float('inf') for nodo in G}
    distancias[inicio] = 0
    caminos = defaultdict(list)
    nodos_vistos = []

    while nodos_vistos != list(G.keys()):
        nodos_no_vistos = {nodo: distancias[nodo] for nodo in set(G.keys()) - set(nodos_vistos)}
        if not nodos_no_vistos:
            break
        nodo_min = min(nodos_no_vistos, key=nodos_no_vistos.get)
        nodos_vistos.append(nodo_min)

        for vecino, peso in G[nodo_min].items():
            nueva_distancia = distancias[nodo_min] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                caminos[vecino] = caminos[nodo_min] + [nodo_min]

    return distancias, caminos

dataset = "C:\Users\Janiel Franz\Desktop\UPC\Algorithmic Complexity\web-app-definitive\djangoProject1\risk\names.csv"
nodos_totales = 5
mapa = generar_grafo(dataset, nodos_totales)

dibujar_grafo(mapa)

nodo_origen = input("Introduce el planeta de origen: ")
nodo_destino = input("I ntroduce el planeta de destino: ")
distancias, caminos = dijkstra(mapa, nodo_origen, nodo_destino)

if nodo_destino in caminos:
    ruta = ' -> '.join(caminos[nodo_destino] + [nodo_destino])
    distancia = distancias[nodo_destino]
    print(f"El camino más corto desde {nodo_origen} a {nodo_destino} es: {ruta} (Distancia: {distancia})")
else:
    print(f"No hay un camino válido desde {nodo_origen} a {nodo_destino}")

print("Todas las rutas posibles:")
for nodo in mapa:
    if nodo != nodo_origen:
        ruta = ' -> '.join(caminos[nodo] + [nodo])
        distancia = distancias[nodo]
        print(f"{nodo_origen} -> {ruta} (Distancia: {distancia})")