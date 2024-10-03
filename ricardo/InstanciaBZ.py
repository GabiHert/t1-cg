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
#from PontosCurva import *

""" Classe Instancia """
class InstanciaBZ:   
    def __init__(self, pontos_curvas):
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotacao:float = 0.0
        self.modelo = None 
        self.t = 0.0
        self.curva_atual = f.CurvaAleatoria(pontos_curvas)
        self.curva_proxima = f.CurvaAleatoria(pontos_curvas)
        self.velocidade = 1.4
        self.cor = YellowGreen
        self.tempo_inicial = 0.0
        self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
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
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        glRotatef(self.rotacao, 0, 0, 1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        SetColor(self.cor)
        self.modelo.desenhaPoligono()
        glPopMatrix()


    def AtualizaPosicao(self, pontos_curva, curvas_por_p0, curvas_por_p2):
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - self.tempo_inicial  # Calcula o tempo decorrido
        self.tempo_inicial = tempo_atual
        
        if self.curva_atual is None:
            self.curva_atual = pontos_curva  # Atribui uma curva aleatória no início
            
            #nao funciona, precisamos conseguir saber a curva atual corretamente pra conseguir pegar o P0 e P2 dela
            # a gente tem a lista de curvas pontos_curva, e a curva_atual, a gente precisa do indice da curva_atual no pontos curva
            #self.indice_curva = random.randint(0, len(pontos_curva) - 1)  # Armazena o índice da curva aleatória

            
            self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)  # Calcula o comprimento da curva

        # Calcular o deslocamento com base na velocidade e no tempo decorrido
        deslocamento = self.velocidade * tempo_decorrido

        # Calcular deltaT com base no deslocamento e no comprimento da curva
        deltaT = deslocamento / self.comprimento_curva

        # Atualize o parâmetro t para mover o personagem ao longo da curva
        self.t += deltaT

        # cuurvas adj
        curvas_adjacentes = []

        if self.t > 1:  # Se t for maior que 1, o personagem chegou ao fim da curva
            self.t = 0  # Reseta t

            indice_atual = f.retornaIndiceCurva()
            ponto_final = pontos_curva[indice_atual].P0
            ponto_inicial = pontos_curva[indice_atual].P2


            print(f"Posição Atual: ({self.posicao.x}, {self.posicao.y}, {self.posicao.z})")
            print(f"Ponto Inicial: {ponto_inicial}")
            print(f"Ponto Final: {ponto_final}")



            # Imprimir todos os pontos em curvas_por_p0 e curvas_por_p2
            print("Curvas por P0:")
            for p0, curvas in curvas_por_p0.items():
                print(f"P0: {p0}, Curvas: {curvas}")
        
            print("Curvas por P2:")
            for p2, curvas in curvas_por_p2.items():
                print(f"P2: {p2}, Curvas: {curvas}")

            # aqui tem q ser self.posicao.x = ponto_final.x ......
            if self.posicao == ponto_final:
                curvas_adjacentes = curvas_por_p2[ponto_final] # Curvas conectadas ao P2
            elif self.posicao == ponto_inicial:
                curvas_adjacentes = curvas_por_p0[ponto_final]  # Curvas conectadas ao P0

            print(f"Curvas Adjacentes: {curvas_adjacentes}")

            if curvas_adjacentes:  # Verifica se há curvas adjacentes antes de escolher aleatoriamente
                self.curva_atual = random.choice(curvas_adjacentes)
                self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
            else:
                print("Nenhuma curva adjacente disponível.")

        # Atualiza a posição do personagem com base na curva e no valor de t
        self.posicao = f.CalculaPontoXYDaCurva(self.t, self.curva_atual)
        self.rotacao = f.Rotacao(self.t, self.curva_atual)
