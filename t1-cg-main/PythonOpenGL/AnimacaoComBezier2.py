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
# ***********************************************************************************

# Modelos de Objetos
MeiaSeta = Polygon()
Mastro = Polygon()
Mapa = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = [] 

# ***********************************************************************************
# Lista de curvas Bezier
Curvas = []

angulo = 0.0
# ***********************************************************************************
#
# ***********************************************************************************
def CarregaModelos():
    global MeiaSeta, Mastro
    MeiaSeta.LePontosDeArquivo("MeiaSeta.txt")
    Mastro.LePontosDeArquivo("Mastro.txt")
    Mapa.LePontosDeArquivo("EstadoRS.txt");
    A, B = Mapa.getLimits()
    print("Limites do Mapa")
    A.imprime()
    B.imprime()


# Chame a nova função em init()
def init():
    global Min, Max
    glClearColor(1, 1, 1, 1)
    
    CarregaModelos()
    CriaCurvasEPersonagens()  # Chame a função unificada aqui
    
    d = 15
    Min = Ponto(-d, -d)
    Max = Ponto(d, d)

# ***********************************************************************************
def DesenhaPersonagem():
    SetColor(YellowGreen)
    glTranslatef(53,33,0)
    Mapa.desenhaPoligono()
    pass

#####################################################################################
def CriaCurvasEPersonagens():
    global Curvas, Personagens
    
    # Lê pontos de controle e curvas do arquivo
    pontos_controle = ler_pontos_de_controle('pontos.txt')
    curvas = ler_curvas('curvas.txt')
    
    # Instancia as curvas de Bézier
    for curva in curvas:
        P0 = pontos_controle[curva[0]]
        P1 = pontos_controle[curva[1]]
        P2 = pontos_controle[curva[2]]
        Curvas.append(Bezier(P0, P1, P2))

    # Cria instâncias dos personagens
    for i in range(10):  # Supondo que você tenha uma instância por curva (mudei pra 10)
        personagem = InstanciaBZ()
        personagem.modelo = DesenhaPersonagem  # Você pode alterar isso se necessário
        personagem.rotacao = 0
        personagem.posicao = Ponto(0, 0)  # Altere conforme necessário
        personagem.escala = Ponto(1, 1, 1)
        Personagens.append(personagem)

# Chame a nova função em init()
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    DesenhaPersonagens()  # Desenha todos os personagens
    desenhaBezier(100, [curva for curva in Curvas], ler_pontos_de_controle('pontos.txt'))  # Chame a função de desenho das curvas

    glutSwapBuffers()

#########################################################
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
# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens

    Personagens.append(InstanciaBZ())
    Personagens[0].modelo = DesenhaPersonagem
    Personagens[0].rotacao = 0
    Personagens[0].posicao = Ponto(0,0)
    Personagens[0].escala = Ponto (1,1,1) 


# ***********************************************************************************
def CriaCurvas():
    global Curvas
    C = Bezier(Ponto (-5,-5), Ponto (0,6), Ponto (5,-5))
    Curvas.append(C)
    C = Bezier(Ponto(5, -5), Ponto(15, 0), Ponto(12, 12))
    Curvas.append(C)
    C = Bezier(Ponto(-10, -5), Ponto(-15, 15), Ponto(12, 12))
    Curvas.append(C)

# ***********************************************************************************
#def init():
    global Min, Max
    # Define a cor do fundo da tela
    glClearColor(1, 1, 1, 1)

    CarregaModelos()
    CriaInstancias()
    CriaCurvas()

    d:float = 15
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)

# ****************************************************************
def animate():
    global angulo
    print('a')
    angulo = angulo + 1
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
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# **************************************************************
def DesenhaPersonagens():
    for I in Personagens:
        I.Desenha()


# ***********************************************************************************
# Versao 
def DesenhaPoligonoDeControle(curva):
    glBegin(GL_LINE_STRIP)
    for v in range(0,3):
        P = Curvas[curva].getPC(v)
        glVertex2d(P.x, P.y)
    glEnd()

# ***********************************************************************************
def DesenhaCurvas():
    v = 0
    #for v, I in enumerate(Curvas):
    for I in Curvas:
        glLineWidth(3)
        SetColor(Blue)
        I.Traca()
        glLineWidth(2)
        SetColor(Bronze)
        I.TracaPoligonoDeControle()
        DesenhaPoligonoDeControle(v)


# ***********************************************************************************
#def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(1,1,1) # R, G, B  [0..1]
   # DesenhaEixos()

    DesenhaPersonagens()
   # DesenhaCurvas()

    pontos_controle = ler_pontos_de_controle('pontos.txt')
    curvas = ler_curvas('curvas.txt')
    desenhaBezier(100, curvas, pontos_controle)
    
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
        Personagens[0].posicao.x -= 0.5
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        Personagens[0].rotacao += 1

    glutPostRedisplay()


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
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


