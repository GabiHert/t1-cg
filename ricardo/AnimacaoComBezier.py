# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from InstanciaBZ import *
from Bezier import *
from ListaDeCoresRGB import *
import Funcoes as f


# ***********************************************************************************

# Modelos de Objetos
modeloPersonagem = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

class PontosCurva:
    def __init__(self, P0, P1, P2) -> None:
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.espessura = 2

pontos_curvas = []
grupos_de_pontos = {}

# lista de instancias do Personagens
Personagens = [] 

# ***********************************************************************************

# ***********************************************************************************



# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens, pontos_controle, curvas, pontos_curvas, grupos_de_pontos

    pontos_controle = ler_pontos_de_controle('pontos.txt')
    curvas = ler_curvas('curvas.txt')
    modeloPersonagem.LePontosDeArquivo("seta.txt")

    for curva in curvas:
        P0 = pontos_controle[curva[0]]
        P1 = pontos_controle[curva[1]]
        P2 = pontos_controle[curva[2]]
        pontos_curvas.append(PontosCurva(P0,P1,P2))

    desenhaBezier(5)

    for pontos_curva in pontos_curvas:
        chave_p0 = geraChave(pontos_curva.P0)
        if chave_p0 not in grupos_de_pontos:
            grupos_de_pontos[chave_p0] = []
        grupos_de_pontos[chave_p0].append(pontos_curva)

        chave_p2 = geraChave(pontos_curva.P2)
            # Adiciona a curva ao grupo de P2
        if chave_p2 not in grupos_de_pontos:
            grupos_de_pontos[chave_p2] = []
        grupos_de_pontos[chave_p2].append(pontos_curva)

    curva = f.CurvaAleatoria(pontos_curvas)

    Personagens.append(InstanciaBZ(pontos_curvas))
    Personagens[0].modelo = modeloPersonagem
    Personagens[0].rotacao = 0
    Personagens[0].posicao = curva.P1
    Personagens[0].escala = Ponto(0.3,0.3,0.3) 
    Personagens[0].usuario = True

    Personagens.append(InstanciaBZ(pontos_curvas))
    Personagens[1].modelo = modeloPersonagem
    Personagens[1].rotacao = 0
    Personagens[1].posicao = curva.P1
    Personagens[1].escala = Ponto(0.3,0.3,0.3) 



# **
# ********************************************************************************

def DesenhaPersonagens(pontos_curvas):
    for I in Personagens:
        I.AtualizaPosicao(grupos_de_pontos, Personagens)
        I.Desenha()
        
def CriaPersonagem(posicao, direcao, i):
    Personagens.append(InstanciaBZ(pontos_curvas))
    Personagens[i].modelo = modeloPersonagem
    Personagens[i].posicao = posicao
    Personagens[i].direcao = direcao

# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela
    glClearColor(1, 1, 1, 1)

    CriaInstancias()
    
    d:float = 5
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)

# ****************************************************************
def animate():
    glutPostRedisplay()

# ****************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ****************************************************************
def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)

# ***********************************************************************************
def reshape(w,h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    gluOrtho2D(Min.x, Max.x, Min.y, Max.y)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# **************************************************************



# ***********************************************************************************
# # Versao 
# def DesenhaPoligonoDeControle(curva):
#     glBegin(GL_LINE_STRIP)
#     for v in range(0,3):
#         P = Curvas[curva].getPC(v)
#         glVertex2d(P.x, P.y)
#     glEnd()

# ***********************************************************************************
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

def desenhaBezier(smooth: int):
    global pontos_curvas
    for pontos_curva in pontos_curvas:
        s = 1 / smooth
        xs = (x * s for x in range(0, smooth + 1))

        glColor3f(pontos_curva.P0.x/2 + 0.3,pontos_curva.P1.x/3 + 0.3 ,pontos_curva.P2.x/2 + 0.3)
        glLineWidth(pontos_curva.espessura)
        glBegin(GL_LINE_STRIP)
        for x in xs:
            r = (pontos_curva.P0 * (1 - x) ** 2) + (pontos_curva.P1 * 2 * x * (1 - x)) + (pontos_curva.P2 * x ** 2)
            glVertex2f(r.x, r.y)
        glEnd()



# ***********************************************************************************
def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(1,0,0) # R, G, B  [0..1]

    desenhaBezier(50)

    DesenhaPersonagens(pontos_curvas)

    
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
# Forca o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        Personagens[0].direcao = False         
    if a_keys == GLUT_KEY_RIGHT:       # Se pressionar LEFT
        Personagens[0].direcao = True         


    glutPostRedisplay()


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(720, 720)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exemplo de Criacao de Curvas Bezier")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
