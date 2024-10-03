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

def Rotacao(t, pontos_curva):
    # Calcule o ponto futuro na curva
    future_point = CalculaPontoXYDaCurva(t, pontos_curva)
    
    # Calcule o vetor direção
    direction_vector = DerivadaBezier(t, pontos_curva)

    # Calcule o vetor do objeto ao ponto futuro
    object_to_future = future_point - pontos_curva.P0

    # Normalize os vetores
    direction_vector_normalized = direction_vector / np.linalg.norm(np.array([direction_vector.x, direction_vector.y, direction_vector.z]))
    object_to_future_normalized = object_to_future / np.linalg.norm(np.array([object_to_future.x, object_to_future.y, object_to_future.z]))

    # Calcule o ângulo em radianos
    angle = np.arctan2(direction_vector_normalized.y, direction_vector_normalized.x) - np.arctan2(object_to_future_normalized.y, object_to_future_normalized.x)
    angle = np.degrees(angle)  # Converta para graus

    # Ajuste o ângulo para estar entre 0 e 360 graus
    if angle < 0:
        angle += 360

    return angle


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
