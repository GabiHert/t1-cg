import math

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

translacaoX = 0
translacaoY = 0

left = 0
right = 0
top = 0
bottom = 0
panX = 0
panY = 0

class Ponto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self) -> None:
        print("Ponto (", self.x, ",", self.y, ")")

    def set(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Ponto(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Ponto(x, y)

    def __mul__(self, escalar: float):
        x = self.x * escalar
        y = self.y * escalar
        return Ponto(x, y)

def desenhaHermite(smooth):

    # Pontos da curva
    P0 = Ponto(0,0)
    P1 = Ponto(0.5, 0.3)
    M0 = Ponto(0, 1)
    M1 = Ponto(0, -0.5)

    s = 1 / smooth
    xs = (x * s for x in range(0, smooth + 1))

    glPushMatrix()
    glColor3f(1, 0, 0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(P0.x, P0.y)
    glVertex2f(P1.x, P1.y)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glColor3f(1, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(P0.x, P0.y)
    t = P0 + M0
    glVertex2f(t.x, t.y)
    glVertex2f(P1.x, P1.y)
    t = P1 + M1
    glVertex2f(t.x, t.y)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINE_STRIP)
    for x in xs:
        p = P0 * (2 * math.pow(x, 3.0) - 3 * math.pow(x, 2.0) + 1) + M0 * (math.pow(x, 3.0) - 2 * math.pow(x, 2.0) + x) + P1 * (-2 * math.pow(x, 3.0) + 3 * math.pow(x, 2.0)) + M1 * (math.pow(x, 3.0) - math.pow(x, 2.0))
        glVertex2f(p.x, p.y)

    glEnd()
    glPopMatrix()

    return

def ler_pontos_de_controle(nome_arquivo):
    pontos = []
    with open(nome_arquivo, 'r') as arquivo:
        numero_pontos = int(arquivo.readline().strip())
        for _ in range(numero_pontos):
            linha = arquivo.readline().strip()
            x, y = map(float, linha.split())
            pontos.append(Ponto(x, y))
    return pontos

def ler_curvas(nome_arquivo):
    curvas = []
    with open(nome_arquivo, 'r') as arquivo:
        numero_curvas = int(arquivo.readline().strip())
        for _ in range(numero_curvas):
            linha = arquivo.readline().strip()
            curvas.append(list(map(int, linha.split())))
    return curvas

def desenhaBezier(smooth: int, curvas, pontos_controle):
    for curva in curvas:
        P0 = pontos_controle[curva[0]]
        P1 = pontos_controle[curva[1]]
        P2 = pontos_controle[curva[2]]

        s = 1 / smooth
        xs = (x * s for x in range(0, smooth + 1))

        glColor3f(1, 1, 1)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for x in xs:
            r = (P0 * (1 - x) ** 2) + (P1 * 2 * x * (1 - x)) + (P2 * x ** 2)
            glVertex2f(r.x, r.y)
        glEnd()


def desenhaEixos():
    global left, right
    glColor3f(1, 1, 1)
    glLineWidth(1)

    glBegin(GL_LINES)
    glVertex2f(left, 0)
    glVertex2f(right, 0)
    glVertex2f(0, bottom)
    glVertex2f(0, top)
    glEnd()

    return


def desenhaCasinha():
    glLineWidth(3)

    glBegin(GL_LINE_LOOP)
    glVertex2f(-0.2, 0.1)
    glVertex2f(-0.2, -0.2)
    glVertex2f(0.2, -0.2)
    glVertex2f(0.2, 0.1)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 0)
    glVertex2f(-0.2, 0.1)
    glColor3f(1, 0, 0)
    glVertex2f(0.0, 0.22)
    glColor3f(0, 0, 1)
    glVertex2f(0.2, 0.1)
    glEnd()

    return


def Desenha():
    global translacaoX, translacaoY, left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    # Liam a janela de visualização com a cor branca
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glLoadIdentity()
    desenhaEixos()
    glPopMatrix()

   # desenhaBezier(100)
    # desenhaHermite(100)

    # Executa os comandos OpenGl

    pontos_controle = ler_pontos_de_controle('pontos.txt')
    curvas = ler_curvas('curvas.txt')

    desenhaBezier(100, curvas, pontos_controle)

    glFlush()

    return


# Função callback chamada para gerenciar eventos de teclas
def Teclado(key: chr, x: int, y: int):
    if key == 27:
        exit(0)

    return


def TeclasEspeciais(key: int, x: int, y: int):
    global translacaoX, translacaoY, left, right, top, bottom, panX, panY

    if key == GLUT_KEY_LEFT:
        translacaoX -= 0.1

    if key == GLUT_KEY_RIGHT:
        translacaoX += 0.1

    if key == GLUT_KEY_UP:
        translacaoY += 0.1

    if key == GLUT_KEY_DOWN:
        translacaoY -= 0.1

    if key == GLUT_KEY_END:
        left -= 0.1
        right += 0.1
        top += 0.1
        bottom -= 0.1

    if key == GLUT_KEY_HOME:
        left += 0.1
        right -= 0.1
        top -= 0.1
        bottom += 0.1

    if key == GLUT_KEY_F9:
        panX += 0.1

    if key == GLUT_KEY_F10:
        panX -= 0.1

    if key == GLUT_KEY_F11:
        panY += 0.1

    if key == GLUT_KEY_F12:
        panY -= 0.1

    # Redesenha
    glutPostRedisplay()
    return


def Inicializa():
    global left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    left = -10
    right = 10
    top = 10
    bottom = -10
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    return


def main():
    glutInit(sys.argv)

    # Define do modo de operação da GLUT
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    # Especifica o tamanho inicial em pixels da janela GLUT
    glutInitWindowSize(800, 800)

    # Cria a janela passando como argumento o título da mesma
    glutCreateWindow("Desenha OpenGL")

    # Registra a função callback de redesenho da janela de visualização
    glutDisplayFunc(Desenha)

    # Registra a função callback para tratamento das teclas ASCII
    glutKeyboardFunc(Teclado)
    glutSpecialFunc(TeclasEspeciais)

    # Chama a função responsável por fazer as inicializações
    Inicializa()

    try:
        # Inicia o processamento e aguarda interações do usuário
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()