
from Ponto import Ponto
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import copy

class Bezier:
    def __init__NEW(self, p0:Ponto, p1:Ponto, p2:Ponto):
        print ("Construtora da Bezier")
        self.ComprimentoTotalDaCurva = 0.0
        self.Coords = [p0, p1, p2]
        #P = self.Coords[0]
        #P.imprime()

    def __init__(self, *args:Ponto):
        #print ("Construtora da Bezier")
        self.ComprimentoTotalDaCurva = 0.0
        self.Coords = []
        #print (args)
        for i in args:
            self.Coords.append(i)
        #P = self.Coords[2]
        #P.imprime()

    def Calcula(self, t):
        UmMenosT = 1-t
        P = Ponto()
        P = self.Coords[0] * UmMenosT * UmMenosT + self.Coords[1] * 2 * UmMenosT * t + self.Coords[2] * t*t
        return P

    def Traca(self):     
        t=0.0
        DeltaT = 1.0/50
        P = Ponto
        glBegin(GL_LINE_STRIP)
        
        while(t<1.0):
            P = self.Calcula(t)
            glVertex2f(P.x, P.y)
            t += DeltaT
        P = self.Calcula(1.0) #faz o acabamento da curva
        glVertex2f(P.x, P.y)
        
        glEnd()

    def TracaPoligonoDeControle(self):
        glBegin(GL_LINE_LOOP)
        for i in range(3):
            glVertex3f(self.Coords[i].x, self.Coords[i].y, self.Coords[i].z)
        glEnd()

    def getPC(self, i):
        temp = copy.deepcopy(self.Coords[i])
        return temp
    
    def calcula_distancia(self, P1, P2):
        # Função que calcula a distância entre dois pontos P1 e P2
        return ((P2.x - P1.x)**2 + (P2.y - P1.y)**2)**0.5

    def calculaComprimentoDaCurva(self):
        # Função que calcula o comprimento total da curva Bezier
        DeltaT = 1.0 / 50
        t = DeltaT
        self.ComprimentoTotalDaCurva = 0

        P1 = self.Calcula(0.0)
        while t < 1.0:
            P2 = self.Calcula(t)
            self.ComprimentoTotalDaCurva += self.calcula_distancia(P1, P2)
            P1 = P2
            t += DeltaT

        P2 = self.Calcula(1.0)  # Faz o fechamento da curva
        self.ComprimentoTotalDaCurva += self.calcula_distancia(P1, P2)        