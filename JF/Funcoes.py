import random
import numpy as np
from Ponto import *
import math

indice_curva_atual = None

def CurvaAleatoria(pontos_curvas):
    global indice_curva_atual
    indice_curva_atual = random.randint(0, len(pontos_curvas) - 1)
    return pontos_curvas[indice_curva_atual]

def retornaIndiceCurva():
    return indice_curva_atual

def CalculaPontoXYDaCurva(t, pontos_curva):
    return pontos_curva.P0 * ((1 - t)**2) + pontos_curva.P1 * (2 * (1 - t) * t ) + pontos_curva.P2 * t**2

def DerivadaBezier(t, pontos_curva):
    return (pontos_curva.P1 - pontos_curva.P0) * (2 * (1 - t)) + (pontos_curva.P2 - pontos_curva.P1) * (2 * t )

def Rotacao(t, pontos_curva, direcao):
    # Get the derivative (direction vector) at point t
    direction_vector = DerivadaBezier(t, pontos_curva)
    
    # Calculate the angle using atan2 to get the angle between the x-axis and the direction
    angle_radians = np.arctan2(direction_vector.y, direction_vector.x)  # Between -π and π
    angle_degrees = np.degrees(angle_radians)  # Convert to degrees

# Ensure the angle is in the range [0, 360)
    if not direcao:
        angle_degrees += 180
    return angle_degrees


def calculaComprimentoDaCurva(curva):
    DeltaT = 1.0 / 50
    t = DeltaT
    ComprimentoTotalDaCurva = 0.0

    P1 = Calcula(curva, 0.0)
    while t < 1.0:
        P2 = Calcula(curva, t)
        ComprimentoTotalDaCurva += CalculaDistancia(P1,P2)
        P1 = P2
        t += DeltaT

    P2 = Calcula(curva, 1.0)  # faz o fechamento da curva
    ComprimentoTotalDaCurva += CalculaDistancia(P1,P2)

    return ComprimentoTotalDaCurva

def Calcula(curva, t):
    UmMenosT = 1 - t
    P = curva.P0 * UmMenosT * UmMenosT + curva.P1 * 2 * UmMenosT * t + curva.P2 * t * t
    return P

def CalculaDistancia(P1, P2):
    return math.sqrt((P1.x - P2.x) ** 2 + (P1.y - P2.y) ** 2)
