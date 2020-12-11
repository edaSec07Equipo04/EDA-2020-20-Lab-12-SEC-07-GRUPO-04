"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
import datetime
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as e
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer():
    try:
        taxis = {
                    'graph': None                 
                    }

        taxis['graph']=gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)  
         
        return taxis
    except Exception as exp:
        error.reraise(exp,'model:newAnalyzer')

def addTrip(taxis, trip):
    """
    """
    origin = trip['pickup_community_area']
    destination = trip['dropoff_community_area']
    if trip['trip_seconds'] != "":
        d = float(trip['trip_seconds'])
        
        duration = int(d)
        
        addStation(taxis,origin)
        addStation(taxis,destination)
        addConnection(taxis,origin,destination,duration)
    else: 
        None

def addStation(taxis,stationId):
    """
    Adiciona una estación como un vértice del grafo
    """
    if not gr.containsVertex(taxis['graph'],stationId):
        gr.insertVertex(taxis['graph'],stationId)
    return taxis

def addConnection(taxis,origin,destination,duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(taxis['graph'],origin,destination)
    if edge is None:
        gr.addEdge(taxis['graph'],origin,destination,duration)
    else:
        e.updateAverageWeight(edge,duration)
    return taxis

def getDateTimeTaxiTrip(taxitrip):
    """
    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).
    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'
    Los datos date se pueden comparar con <, >, <=, >=, ==, !=
    Los datos time se pueden comparar con <, >, <=, >=, ==, !=
    """
    tripstartdate = taxitrip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()

# ==============================
# Funciones de consulta
# ==============================

def totalStops(taxis):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(taxis['graph'])


def totalConnections(taxis):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(taxis['graph'])   

def numSCC(graph):
    """
    Informa cuántos componentes fuertemente conectados se encontraron
    """
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(graph,station1,station2):
    """
    Informa si dos estaciones están en el mismo componente conectado.
    """
    sc = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(sc,station1,station2)

def stationsSize(graph):
    return lt.size(graph['stations'])
# ==============================
# Funciones Helper
# ==============================
def getDateTimeTaxiTrip(taxitrip):
    """
    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).
    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'
    Los datos date se pueden comparar con <, >, <=, >=, ==, !=
    Los datos time se pueden comparar con <, >, <=, >=, ==, !=
    """
    tripstartdate = taxitrip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(station, keyvaluestation):
    """
    Compara dos estaciones
    """
    stationId = keyvaluestation['key']
    if (station == stationId):
        return 0
    elif (station > stationId):
        return 1
    else:
        return -1





