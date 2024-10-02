import random
import numpy as np


def CurvaAleatoria(pontos_curvas):
    return pontos_curvas[random.randint(0, len(pontos_curvas) - 1)]

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