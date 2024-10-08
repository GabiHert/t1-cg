# ************************************************
#   InstanciaBZ.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# calcularCurvasAdjacentes esta pegando o ponto 
# precisa instanciar o atributo proxima_curva antes no costrutor
# calcularCurvasAdjacentes dependencia ciclica entre calculaProximaCurva
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
import Funcoes as f
from ListaDeCoresRGB import *
import random
from Poligonos import *
import math

class InfoProximaCurva:
    def __init__(self, curva, direcao, indice):
        self.direcao = direcao
        self.indice = indice
        if direcao:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(0, curva)
            self.ponto_final = f.CalculaPontoXYDaCurva(1, curva)
            self.t = 0
        else:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(1, curva)
            self.ponto_final = f.CalculaPontoXYDaCurva(0, curva)
            self.t = 1
        self.comprimento_curva = f.calculaComprimentoDaCurva(curva)


""" Classe Instancia """
class InstanciaBZ:   
    def __init__(self, pontos_curvas, grupos_de_pontos, usuario:bool,curva):
        self.info_proxima_curva:InfoProximaCurva = None
        self.grupos_de_pontos = grupos_de_pontos
        self.flag = False
        self.flag2 = False
        self.direcao = True
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (0.3,0.3,0.3)
        self.rotacao:float = 0.0
        self.modelo = None 
        self.indice_curva = curva
        self.t = 0.5
        self.curva_atual = pontos_curvas[self.indice_curva]
        self.velocidadeInicial = 1.5
        self.velocidade = self.velocidadeInicial
        if usuario:
            self.cor = Red
            self.width = 5
        else:
            self.cor = random.choice(coresPersonagem)
            self.width = 3
        self.tempo_inicial = 0.0
        self.comprimento_curva = f.calculaComprimentoDaCurva(self.curva_atual)
        self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
        self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
        self.curvas_adjacentes = self.calcularCurvasAdjacentes(self.ponto_final,self.grupos_de_pontos)
        self.usuario = usuario

    
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
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        glRotatef(self.rotacao, 0,0,1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        SetColor(self.cor)
        glLineWidth(self.width)
        self.modelo.desenhaPoligono()
        glPopMatrix()
        

    def verifica_colisao(self, Personagens):
        for outro in Personagens:
            if outro != self:  
                if outro.curva_atual == self.curva_atual:
                    distancia = math.sqrt( (self.posicao.x - outro.posicao.x)  ** 2 + (self.posicao.y - outro.posicao.y)   ** 2)

                    if distancia < (0.35):
                        return True
                else:
                    if self.ponto_final == outro.ponto_final:
                        distancia_self = math.sqrt((self.posicao.x - self.ponto_final.x) ** 2 + (self.posicao.y - self.ponto_final.y) ** 2)
                        distancia_outro = math.sqrt((outro.posicao.x - outro.ponto_final.x) ** 2 + (outro.posicao.y - outro.ponto_final.y) ** 2)
                    
                        if (distancia_self < 0.01) and (distancia_outro < 0.01):  
                            return True

        return False

    
    def SelecionaCurva(self):
        indice = 0
        self.curva_atual.espessura = 2
        if self.info_proxima_curva is not None:
            if self.info_proxima_curva.indice >= len(self.curvas_adjacentes):
                self.info_proxima_curva.indice = 0
            self.curvas_adjacentes[self.info_proxima_curva.indice].espessura = 2
            indice = self.info_proxima_curva.indice + 1
            if indice >= len(self.curvas_adjacentes):
                indice = 0

        direcao = self.calculaDirecao(self.ponto_final, self.curvas_adjacentes[indice].P0)
        self.info_proxima_curva = InfoProximaCurva(self.curvas_adjacentes[indice], direcao, indice)
        self.curvas_adjacentes[indice].espessura = 10

    def MudaDirecao(self, direcao):
        if self.info_proxima_curva != None:
            self.curvas_adjacentes[self.info_proxima_curva.indice].espessura = 2
        self.direcao = direcao
        ponto_destino = self.calculaPontoDestino(self.direcao, self.curva_atual.P0, self.curva_atual.P2)
        self.curvas_adjacentes = self.calcularCurvasAdjacentes(ponto_destino,self.grupos_de_pontos)
        if direcao:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
            self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
        else:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(1, self.curva_atual)
            self.ponto_final = f.CalculaPontoXYDaCurva(0,  self.curva_atual)
        self.SelecionaCurva()
        
    def MudaDirecaoInimigos(self,direcao):
        self.direcao = direcao
        ponto_destino = self.calculaPontoDestino(self.direcao, self.curva_atual.P0, self.curva_atual.P2)
        self.curvas_adjacentes = self.calcularCurvasAdjacentes(ponto_destino,self.grupos_de_pontos)
        if direcao:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(0, self.curva_atual)
            self.ponto_final = f.CalculaPontoXYDaCurva(1, self.curva_atual)
        else:
            self.ponto_inicial = f.CalculaPontoXYDaCurva(1, self.curva_atual)
            self.ponto_final = f.CalculaPontoXYDaCurva(0,  self.curva_atual)

    def AtualizaPosicao(self,Personagens,tempo_atual):
        
        
        if self.flag2:
            tempo_decorrido = tempo_atual - self.tempo_inicial  
        else:
            tempo_decorrido = 0.0        
            self.flag2 = True

        if self.usuario:
            colisao = self.verifica_colisao(Personagens)
            if colisao == True:
                self.velocidade = 0
                os._exit(0)

        self.tempo_inicial = tempo_atual

        deslocamento = self.velocidade * tempo_decorrido

        deltaT = deslocamento / self.comprimento_curva

        esta_no_meio = self.t > 0.4 and self.info_proxima_curva == None

        chegou_ao_fim = False
        if self.direcao:
            self.t += deltaT
            chegou_ao_fim = self.t >= 1
        else: 
            self.t -= deltaT
            chegou_ao_fim = self.t <= 0  
        
        if self.usuario and self.info_proxima_curva == None:
            self.SelecionaCurva()
        
        if esta_no_meio and not self.usuario: #
            ponto_destino = self.calculaPontoDestino(self.direcao, self.curva_atual.P0, self.curva_atual.P2)
            self.curvas_adjacentes = self.calcularCurvasAdjacentes(ponto_destino,self.grupos_de_pontos)
            indice = self.calculaProximoInidiceDeCurva(self.curvas_adjacentes)
            while indice == self.indice_curva:
                indice = self.calculaProximoInidiceDeCurva(self.curvas_adjacentes)
            direcao = self.calculaDirecao(self.ponto_final,self.curvas_adjacentes[indice].P0)
            self.info_proxima_curva = InfoProximaCurva(self.curvas_adjacentes[indice], direcao,indice)
        elif chegou_ao_fim:  
            self.vaiParaProximaCurva(self.info_proxima_curva, self.curvas_adjacentes)
            self.flag = False
            self.info_proxima_curva = None
            self.flag2 = False
            ponto_destino = self.calculaPontoDestino(self.direcao, self.curva_atual.P0, self.curva_atual.P2)
            self.curvas_adjacentes = self.calcularCurvasAdjacentes(ponto_destino,self.grupos_de_pontos)

        self.posicao = f.CalculaPontoXYDaCurva(self.t, self.curva_atual)
        self.rotacao = f.Rotacao(self.t, self.curva_atual, self.direcao)
    
    def calculaPontoDestino(self, direcao, ponto_inicial, ponto_final):
        if direcao:
            return ponto_final
        else:
            return ponto_inicial
    
    def calcularCurvasAdjacentes(self, ponto, grupos_de_pontos):
        chave = geraChave(ponto)
    
        result = grupos_de_pontos[chave]

        return result
    
    def calculaDirecao(self, ponto_curva_atual,ponto_proxima_curva):
            if posicaoAproximada(ponto_curva_atual, ponto_proxima_curva):
                return True
            else:
                return  False
    
    def indiceAleatorio(self, maxIdx):
        indice_curva = random.randint(0, maxIdx - 1)
        while self.info_proxima_curva != None and self.info_proxima_curva.indice == indice_curva:  
            indice_curva = random.randint(0, maxIdx - 1)
        return indice_curva
    
    def calculaProximoInidiceDeCurva(self, curvas_adjacentes):
        indice = self.indiceAleatorio(len(curvas_adjacentes))
        return indice

    def vaiParaProximaCurva(self, info_proxima_curva:InfoProximaCurva, curvas_adjacentes):
        self.curva_atual = curvas_adjacentes[info_proxima_curva.indice]
        self.direcao = info_proxima_curva.direcao
        self.t = info_proxima_curva.t
        self.ponto_inicial = info_proxima_curva.ponto_inicial
        self.ponto_final = info_proxima_curva.ponto_final
        self.comprimento_curva = info_proxima_curva.comprimento_curva
        self.indice_curva = info_proxima_curva.indice
        return 

def posicaoAproximada(ponto, posicao):
    aproximacao = 0.2
    result =  (posicao.x < ponto.x+aproximacao and posicao.x > ponto.x-aproximacao) and (posicao.y < ponto.y+aproximacao and posicao.y > ponto.y-aproximacao)
    return result
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
