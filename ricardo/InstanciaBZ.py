# ************************************************
#   InstanciaBZ.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
import Funcoes as f
from ListaDeCoresRGB import *
import time
import random
from Poligonos import *

""" Classe Instancia """
class InstanciaBZ:   
    def __init__(self, pontos_curvas):
        self.flag = False
        self.flag2 = False
        self.direcao = True
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (0.3,0.3,0.3)
        self.rotacao:float = 0.0
        self.modelo = None 
        self.t = 0.0
        self.curva_atual = f.CurvaAleatoria(pontos_curvas)
        self.curva_proxima = f.CurvaAleatoria(pontos_curvas)
        self.velocidade = 2.5
        self.cor = YellowGreen
        self.tempo_inicial = 0.0
        self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
        self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
        self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
        self.indice_curva = f.retornaIndiceCurva
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            pass 
        else:
            print ("Rotacao:", self.rotacao)

    """ Define o modelo a ser usada para a desenhar """
    def setModelo(self, func):
        self.modelo = func

    def Desenha(self):
        #print ("Desenha")
        #self.escala.imprime("\tEscala: ")
        #print ("\tRotacao: ", self.rotacao)
        #centroid = calculaCentroid(self.modelo)
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        #glTranslatef(-centroid.x, -centroid.y, 0)
        glRotatef(self.rotacao, 0,0,1)
        #glTranslatef(centroid.x, centroid.y, 0)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        SetColor(self.cor)
        glLineWidth(3)
        self.modelo.desenhaPoligono()
        glPopMatrix()
    
    def calcula_centroid(self):
    # Supondo que self.modelo tem os vértices do triângulo
        x1, y1 = self.modelo.vertices[0].x, self.modelo.vertices[0].y
        x2, y2 = self.modelo.vertices[1].x, self.modelo.vertices[1].y
        x3, y3 = self.modelo.vertices[2].x, self.modelo.vertices[2].y
        return Ponto((x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3)


    def AtualizaPosicao(self, grupos_de_pontos):
        tempo_atual = time.time()
    
        if self.flag2:
            tempo_decorrido = tempo_atual - self.tempo_inicial  # Calcula o tempo decorrido
        else:
            tempo_decorrido = 0.0        
            self.flag2 = True

        self.tempo_inicial = tempo_atual

        # Calcular o deslocamento com base na velocidade e no tempo decorrido
        deslocamento = self.velocidade * tempo_decorrido

        # Calcular deltaT com base no deslocamento e no comprimento da curva
        deltaT = deslocamento / self.comprimento_curva

        # Atualize o parâmetro t para mover o personagem ao longo da curva
        chegou_ao_fim = False
        if self.direcao:
            self.t += deltaT
            chegou_ao_fim = self.t >= 1
        else: 
            self.t -= deltaT
            chegou_ao_fim = self.t <= 0

        # cuurvas adj
        curvas_adjacentes = []

        if  chegou_ao_fim:  # Se t for maior que 1, o personagem chegou ao fim da curva
            if self.flag:
                if posicaoAproximada(self.ponto_final, self.posicao):
                    chave = geraChave(self.ponto_final)
                elif posicaoAproximada(self.ponto_inicial, self.posicao):
                    chave = geraChave(self.ponto_inicial)
                curvas_adjacentes = grupos_de_pontos[chave]

                print(f"Curvas Adjacentes: {curvas_adjacentes}")
            else: 
                self.flag = True

            if curvas_adjacentes:  # Verifica se há curvas adjacentes antes de escolher aleatoriamente
                proxima_curva = self.curva_atual

                while proxima_curva == self.curva_atual:  # Evita que a próxima curva seja a mesma que a atual
                    proxima_curva = random.choice(curvas_adjacentes)

                self.curva_atual = proxima_curva
                if posicaoAproximada(self.curva_atual.P0, self.posicao):
                    self.direcao = True
                    self.t = 0 
                else:
                    self.direcao = False
                    self.t = 1 
                self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
                self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
                self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
                self.flag = False
                self.flag2 = False
            else:
                print("Nenhuma curva adjacente disponível.")

        # Atualiza a posição do personagem com base na curva e no valor de t
        self.posicao = f.CalculaPontoXYDaCurva(self.t, self.curva_atual)
        self.rotacao = f.Rotacao(self.t, self.curva_atual, self.direcao)
        
    def calcularCurvasAdjacentes(self, grupos_de_pontos):
        if self.flag:
            if posicaoAproximada(self.ponto_final, self.posicao):
                chave = geraChave(self.ponto_final)
            elif posicaoAproximada(self.ponto_inicial, self.posicao):
                chave = geraChave(self.ponto_inicial)
            curvas_adjacentes = grupos_de_pontos[chave]

            print(f"Curvas Adjacentes: {curvas_adjacentes}")
        else: 
            self.flag = True

    def calculaProximaCurva(self, curvas_adjacentes):
        if curvas_adjacentes:  # Verifica se há curvas adjacentes antes de escolher aleatoriamente
            proxima_curva = self.curva_atual

            while proxima_curva == self.curva_atual:  # Evita que a próxima curva seja a mesma que a atual
                proxima_curva = random.choice(curvas_adjacentes)

            self.curva_atual = proxima_curva
            if posicaoAproximada(self.curva_atual.P0, self.posicao):
                self.direcao = True
                self.t = 0 
            else:
                self.direcao = False
                self.t = 1 
            self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
            self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
            self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
            self.flag = False
            self.flag2 = False
        else:
            print("Nenhuma curva adjacente disponível.")

def posicaoAproximada(ponto, posicao):
    aproximacao = 0.2
    return (posicao.x < ponto.x+aproximacao and posicao.x > ponto.x-aproximacao) and (posicao.y < ponto.y+aproximacao and posicao.y > ponto.y-aproximacao)

class ChavePonto:
    def __init__(self, ponto, chave):
        self.ponto = ponto
        self.chave = chave
chaves_pontos= []

def geraChave(ponto):
    global chaves_pontos
    
    for chave_ponto in chaves_pontos:
        if posicaoAproximada(chave_ponto.ponto, ponto):
            return chave_ponto.chave
    
    chave = f"{ponto.x}-{ponto.y}"
    chaves_pontos.append(ChavePonto(ponto, chave))

    return chave