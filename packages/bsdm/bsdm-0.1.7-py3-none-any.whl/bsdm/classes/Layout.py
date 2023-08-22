
import random
import math

from utils.logger import LOGGER

# mass
alpha = 1.0
beta = .0001
k = 1.0
d = 0.1

#damping
eta = .99
delta_t = .01

infinity = 1000000.0



class Point(object):

    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y
    
    def __add__(self, point):
        return(Point(self.getX() + point.getX(), self.getY() + point.getY()))   
    
    def __sub__(self, point):
        return(Point(self.getX() - point.getX(), self.getY() - point.getY()))       
    
    def __mul__(self, scalar):
        return(Point(self.getX() * scalar, self.getY() * scalar))     
        
    def __str__(self):
        return '('+str(self._x)+', '+str(self._y)+')'
        
    def set(self, x, y):
        self._x = x
        self._y = y   

    def getX(self):
        return self._x

    def getY(self):
        return self._y
    
    def translate(self, vector):
        self._x += vector.getX()
        self._y += vector.getY()

    def dot(self, scalar):
        self._x *= scalar
        self._y *= scalar
        
    def norm(self):
        return math.sqrt(self._x * self._x + self._y * self._y)
        
        
Vector = Point 
    
    
class Vertice(Point):
    
    def __init__(self, name, x=0.0, y=0.0):
        self.__name = name
        super().__init__(x, y)
    
    def __str__(self):
        return 'V [ '+self.__name+':'+ super().__str__() +']'
        
        
    def getName(self):
        return self.__name
    
    
class Edge(object):
    
    __SEPARATOR = '@'
    
    def __init__(self, vertice1, vertice2):    
        self.__vertice1 = vertice1
        self.__vertice2 = vertice2
    
    def getIdentifiers(self):
        return  self.__vertice1.getName() + Edge.__SEPARATOR + self.__vertice2.getName(), \
                self.__vertice2.getName() + Edge.__SEPARATOR + self.__vertice1.getName()
    
    @classmethod        
    def genIdentifiers(cls, vertice1, vertice2):
        return vertice1.getName()+Edge.__SEPARATOR+vertice2.getName(), vertice2.getName()+Edge.__SEPARATOR+vertice1.getName()


class Graph(object):
    
    __edges = {}     # arrêtes
    __vertices = {}  # noeuds
    
    @classmethod
    def getVerticesNumber(cls):
        return len(cls.__vertices)
    
    @classmethod
    def addEdge(cls, edge):
        identifier1, identifier2 = edge.getIdentifiers()
        cls.__edges[identifier1] = True
        cls.__edges[identifier2] = True

    @classmethod
    def addVertice(cls, vertice):
        if(vertice.getName() in cls.__vertices):
            LOGGER.warning('Trying to add a vertice with an already used name.')
        else:
            cls.__vertices[vertice.getName()] = vertice

    @classmethod
    def updateVertices(cls, vertices):
        cls.__vertices = vertices

    @classmethod
    def reset(cls):
        cls.__edges = {}  
        cls.__vertices = []        

    @classmethod  
    def print(cls):
        strResult =''
        for vertice in cls.__vertices:
            print(cls.__vertices[vertice])
    
    @classmethod        
    def getVertices(cls):
        return cls.__vertices
    
    @classmethod
    def edgeExists(cls, vertice1, vertice2):
        _id1, _id2 = Edge.genIdentifiers(vertice1, vertice2)
        return _id1 in cls.__edges or _id2 in cls.__edges



class Layout(object):

    ## Spring constants and variables
    # mass
    __springAlpha  = 1.0
    __springBeta   = 0.0001
    __springK      = 1.0
    __springD      = 0.1

    #damping
    __springEta    = 0.99
    __springDeltaT = 0.01
    
    __springStep   = 0

    
    @classmethod        
    def initSpringAlgorithm(cls, step=500, limit=0):
        cls.__vertices = Graph.getVertices()
    
        cls.__springSpeeds = {}
        cls.__springStep   = step
        cls.__springLimit  = limit
    
        for vertice in cls.__vertices:
            vertice = cls.__vertices[vertice]
            vertice.set(random.random(), random.random())               # set random position
            cls.__springSpeeds[vertice.getName()] = Vector(0.0, 0.0)    # set initial speed
            
        
    @classmethod 
    def runSpringAlgorithm(cls):
        while (cls.__springStep > 0):
            cls.__springStep -= 1
            kineticEnergy = cls.__springLoop() 
            Graph.updateVertices(cls.__vertices)  
            if(kineticEnergy < cls.__springLimit):
                return         
    
    @classmethod
    def __springRepulsiveForce(cls, vertice1, vertice2):  # Coulomb law 
    
        if(vertice1 == vertice2):
            return Vector(0.0, 0.0)
        delta = vertice2 - vertice1

        distance = delta.norm()  

        if(distance != 0.0):
            const = cls.__springBeta / (distance**3)
        else:
            const = cls.__springBeta * infinity

        return delta * (- const)


    @classmethod
    def __springAttractiveForce(cls, vertice1, vertice2): #Hooke law

        if(vertice1 == vertice2):
            return Vector(0.0, 0.0)

        delta = vertice2 - vertice1
        
        distance = delta.norm()

        const = cls.__springK * (distance - cls.__springD) / distance

        return delta * const
    
    
    @classmethod     
    def __springLoop(cls):
        
        kineticEnergy = Vector(0.0, 0.0) # initialize force
        
        for vertice1 in cls.__vertices:
            vertice1 = cls.__vertices[vertice1]
            
            force = Vector(0.0, 0.0) # initialize force
        
            for vertice2 in cls.__vertices:
                vertice2 = cls.__vertices[vertice2]

                # compute force
                if(Graph.edgeExists(vertice1, vertice2)) :
                    force += cls.__springAttractiveForce(vertice1, vertice2)
                force += cls.__springRepulsiveForce(vertice1, vertice2)           

            # update speed
            _speedX = cls.__springSpeeds[vertice1.getName()].getX() + cls.__springAlpha * force.getX() * cls.__springDeltaT 
            _speedY = cls.__springSpeeds[vertice1.getName()].getY() + cls.__springAlpha * force.getY() * cls.__springDeltaT 

            cls.__springSpeeds[vertice1.getName()] = Vector(_speedX, _speedY) * cls.__springEta

            tmpVertice = cls.__vertices[vertice1.getName()] + (cls.__springSpeeds[vertice1.getName()] * cls.__springDeltaT) # to delete

        # update position
        for vertice in cls.__vertices:
            tmpVertice = cls.__vertices[vertice] + (cls.__springSpeeds[vertice] * cls.__springDeltaT)
            cls.__vertices[vertice].set(tmpVertice.getX(), tmpVertice.getY())
            
        #compute kinetic energy
            _kinEX = kineticEnergy.getX() + cls.__springAlpha * (cls.__springSpeeds[vertice].getX() ** 2) 
            _kinEY = kineticEnergy.getY() + cls.__springAlpha * (cls.__springSpeeds[vertice].getY() ** 2)
            kineticEnergy = Vector(_kinEX, _kinEY)
            
        kineticEnergy = kineticEnergy.norm()
        
        return kineticEnergy


def layout():
    
    # Build graph
    
    vA = Vertice('A')
    vB = Vertice('B')  
    vC = Vertice('C')
    vD = Vertice('D')  
    
    eAB = Edge(vA, vB)
    eBC = Edge(vB, vC)
    eCA = Edge(vC, vA)
    eCD = Edge(vC, vD)
    
    Graph.addVertice(vA)
    Graph.addVertice(vB)
    Graph.addVertice(vC)
    Graph.addVertice(vD)
    #Graph.addVertice(vD)
    
    Graph.addEdge(eAB)
    Graph.addEdge(eBC)
    Graph.addEdge(eCA)
    Graph.addEdge(eCD)
    

    Layout.initSpringAlgorithm(step=1000000, limit=0.00000000000000000001)
    Graph.print() 
    input()
    Layout.runSpringAlgorithm()
    Graph.print()    
    
    