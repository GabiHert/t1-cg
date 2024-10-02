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
        self.velocidade = 0.01
        self.cor = YellowGreen
    
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


    def AtualizaPosicao(self, pontos_curva):
        if self.curva_atual is None:
            self.curva_atual = pontos_curva  # Atribui uma curva aleatória no início
            
            # self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)  # Calcula o comprimento da curva

        # # Calcular o deslocamento com base na velocidade e no tempo decorrido
        # deslocamento = self.velocidade * tempo_decorrido

        # # Calcular deltaT com base no deslocamento e no comprimento da curva
        # deltaT = deslocamento / self.comprimento_curva

        # # Atualize o parâmetro t para mover o personagem ao longo da curva
        # self.t += deltaT
        
        self.t += 0.001

        # Atualize o parâmetro t para mover o personagem ao longo da curva

        if self.t > 1:  # Se t for maior que 1, o personagem chegou ao fim da curva
            self.t = 0  # Reseta t
            self.curva_atual = f.CurvaAleatoria(pontos_curva)
            # self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)

        # Atualiza a posição do personagem com base na curva e no valor de t
        self.posicao = f.CalculaPontoXYDaCurva(self.t, self.curva_atual)
        self.rotacao = f.Rotacao(self.t, self.curva_atual)
        
    # def AtualizaPosicao(self, pontos_curvas):
    # # Placeholder for actual implementation
    #     pass
        
        
    #def AtualizaPosicao(self,pontos_curvas):
        ##
        # preciso saber qual a curva que estou
        # 
        # descobir se a curva ja terminou
        #   se ja terminou escolher outra curva que tenha inicio/fim no mesmo ponto 
        #   se nao terminou 
       # pass

