import turtle as tt
import functools
import random
import time
import pygame

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90.00
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 4
BOLA_START_POS = (1, 1)
playerA = input('Qual o nome do jogador vermelho: ')
playerB = input('Qual o nome do jogador azul: ')

# Funções responsáveis pelo movimento dos jogadores no ambiente.
# O número de unidades que o jogador se pode movimentar é definida pela constante
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado
# do jogo e o jogador que se está a movimentar.
''' O código foi escrito na versao 3.11.6 do python. De forma a correr o código corretamente, deve instalar o pip. '''

def jogador_cima(estado_jogo, jogador):
    jogador = estado_jogo[jogador]
    if jogador.ycor() + RAIO_JOGADOR + PIXEIS_MOVIMENTO <= ALTURA_JANELA / 2:
        jogador.sety(jogador.ycor() + PIXEIS_MOVIMENTO)


def jogador_baixo(estado_jogo, jogador):
    jogador = estado_jogo[jogador]
    if jogador.ycor() - RAIO_JOGADOR - PIXEIS_MOVIMENTO >= -ALTURA_JANELA / 2:
        jogador.sety(jogador.ycor() - PIXEIS_MOVIMENTO)


def jogador_direita(estado_jogo, jogador):
    jogador = estado_jogo[jogador]
    if jogador.xcor() + RAIO_JOGADOR + PIXEIS_MOVIMENTO <= LARGURA_JANELA / 2:
        jogador.setx(jogador.xcor() + PIXEIS_MOVIMENTO)


def jogador_esquerda(estado_jogo, jogador):
    jogador = estado_jogo[jogador]
    if jogador.xcor() - RAIO_JOGADOR - PIXEIS_MOVIMENTO >= -LARGURA_JANELA / 2:
        jogador.setx(jogador.xcor() - PIXEIS_MOVIMENTO)


def retangulo(lado_maior, lado_menor):
    for i in range(2):
        tt.fd(lado_maior)
        tt.lt(90)
        tt.fd(lado_menor)
        tt.lt(90)


def desenha_linhas_campo():
    def centro_do_campo():
        tt.pu()
        tt.home()
        tt.lt(90)
        tt.pensize(10)
        tt.pencolor('white')
        tt.pd()
        tt.fd(ALTURA_JANELA / 2)
        tt.fd(-ALTURA_JANELA)
        tt.home()
        tt.seth(0)
        tt.penup()
        tt.fd(RAIO_MEIO_CAMPO*2)
        tt.lt(90)
        tt.pd()
        tt.circle(RAIO_MEIO_CAMPO*2)

    def baliza(LADO_MAIOR_AREA, LARGURA_JANELA, LADO_MENOR_AREA):
        tt.penup()
        tt.home()
        tt.fd(LARGURA_JANELA / 2)
        tt.lt(90)
        tt.back(LADO_MAIOR_AREA / 2)
        tt.pd()
        retangulo(LADO_MAIOR_AREA, LADO_MENOR_AREA)

    def linhas_de_fora():
        # Desenhar Linhas de Fora
        tt.back(LADO_MAIOR_AREA)
        retangulo(ALTURA_JANELA, -LARGURA_JANELA)
        tt.hideturtle()

    centro_do_campo()
    baliza(LADO_MAIOR_AREA, LARGURA_JANELA, LADO_MENOR_AREA)
    baliza(LADO_MAIOR_AREA, -LARGURA_JANELA, -LADO_MENOR_AREA)
    linhas_de_fora()


def criar_bola():
    '''
    Função responsável pela criação da bola.
    Deverá considerar que esta tem uma forma redonda, é de cor preta,
    começa na posição BOLA_START_POS com uma direção aleatória.
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores.
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola,
    a sua direção no eixo dos xx, a sua direção no eixo dos yy,
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''
    bola = tt.Turtle()
    bola.shape('circle')
    bola.pu()
    bola.color('black')
    bola.goto(BOLA_START_POS)
    resultado = dict()
    resultado['objeto'] = bola
    resultado['dirx'] = random.uniform(-1, 1)
    resultado['diry'] = random.uniform(-1, 1)
    resultado['pos_anterior'] = None
    return resultado


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle).
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo,
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros:
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    jogador = tt.Turtle()
    jogador.speed(0)
    jogador.penup()
    jogador.shape("circle")
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    jogador.color(cor)
    jogador.goto(x_pos_inicial, y_pos_inicial)
    return jogador


def init_state():
    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola': [],
        'jogador_vermelho': [],
        'jogador_azul': [],
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0
    return estado_jogo


def cria_janela():
    # create a window and declare a variable called window and call the screen()
    window = tt.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    window.tracer(0)
    return window


def cria_quadro_resultados():
    # Code for creating pen for scorecard update
    quadro = tt.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0, 260)
    quadro.write("%s: 0\t\t%s: 0 "%(playerA,playerB), align="center", font=('Monaco', 24, "normal"))
    return quadro

def terminar_jogo(estado_jogo):
    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro
     ''historico_resultados.csv'' com o número total de jogos até ao momento,
     e o resultado final do jogo. Caso o ficheiro não exista,
     ele deverá ser criado com o seguinte cabeçalho:
     NJogo,JogadorVermelho,JogadorAzul.
    '''
    nome = 'historico_resultados.csv' # Verifica se o ficheiro existe,caso exista nao faz nada, se existir vai criá-lo
    ficheiro = open(nome, 'a')    
    ficheiro.close()
    ficheiro = open(nome, 'r')
    linhas = ficheiro.readlines()
    total_linhas = len(linhas)
    ficheiro.close()    
    if total_linhas == 0:
        ficheiro = open(nome, 'w')
        numerodejogos = 1
        ficheiro.writelines(['NJogo,JogadorVermelho,JogadorAzul\n', str(numerodejogos) + ',' + str(estado_jogo['pontuacao_jogador_vermelho']) + ',' + str(estado_jogo['pontuacao_jogador_azul']) + '\n'])
        ficheiro.close()
    else:
        numerodejogos = total_linhas
        ficheiro = open(nome, 'a')
        ficheiro.writelines([str(numerodejogos) + ',' + str(estado_jogo['pontuacao_jogador_vermelho']) + ',' + str(estado_jogo['pontuacao_jogador_azul']) + '\n'])
        ficheiro.close()    
    print("Adeus")
    pygame.quit()  #Parar a Música Ambiente
    estado_jogo['janela'].bye()
    

def setup(estado_jogo, jogar):
    janela = cria_janela()
    # Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho'), 'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho'), 's')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho'), 'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho'), 'd')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul'), 'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul'), 'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul'), 'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul'), 'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), 'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write(("%s: {}\t\t%s: {} "%(playerA,playerB)).format(estado_jogo['pontuacao_jogador_vermelho'],
                                                                           estado_jogo['pontuacao_jogador_azul']),
                                    align="center", font=('Monaco', 24, "normal"))


def movimenta_bola(estado_jogo):
    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''
    bola = estado_jogo['bola']['objeto']
    pos_bola = bola.pos()
    bola.goto(pos_bola[0] + estado_jogo['bola']['dirx'], pos_bola[1] + estado_jogo['bola']['diry'])


def verifica_colisoes_ambiente(estado_jogo):
    '''
    Função responsável por verificar se há colisões com os limites do ambiente,
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais,
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''
    bola = estado_jogo['bola']['objeto']
    bolapos = bola.pos()
    if ((bolapos[0] + RAIO_BOLA >= LARGURA_JANELA / 2) or (bolapos[0] - RAIO_BOLA <= -LARGURA_JANELA / 2)):
        estado_jogo['bola']['dirx'] *= -1
    if ((bolapos[1] + RAIO_BOLA >= ALTURA_JANELA / 2) or (bolapos[1] - RAIO_BOLA <= -ALTURA_JANELA / 2)):
        estado_jogo['bola']['diry'] *= -1
    if (bolapos[1] > ALTURA_JANELA/2) or (bolapos[1] < -ALTURA_JANELA/2) or (bolapos[0] < -LARGURA_JANELA / 2) or (bolapos[0] > LARGURA_JANELA / 2): #Se a bola sair do campo é mandada para o centro
        print("Bola Fora")
        bola.goto(BOLA_START_POS)    

def reinicio_jogo(estado_jogo):        
    estado_jogo['bola']['dirx'] = 0
    estado_jogo['bola']['diry'] = 0
    estado_jogo['bola']['objeto'].goto(BOLA_START_POS)
    estado_jogo['jogador_vermelho'].goto(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)
    estado_jogo['jogador_azul'].goto(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)   
    estado_jogo['bola']['dirx'] = random.uniform(-1, 1)
    estado_jogo['bola']['diry'] = random.uniform(-1, 1)

def criar_ficheiro(estado_jogo):
    ficheiro = 'replay_golo_jv_%i_ja_%i.txt'%(estado_jogo['pontuacao_jogador_vermelho'],estado_jogo['pontuacao_jogador_azul'])
    var = open(ficheiro,'w')
    for i in estado_jogo['var'].values():
        count = len(i)
        for j in range(count):
            x,y=i[j]
            x1,y1=int(x),int(y)
            if j < count - 1:
                var.write('%s,%s;'%(format(float(x1), '.3f'), format(float(y1), '.3f')))
            else:
                var.write('%s,%s' % (format(float(x1), '.3f'), format(float(y1), '.3f')))

        var.write('\n')
    var.close()
    estado_jogo['var']['bola'].clear()
    estado_jogo['var']['jogador_vermelho'].clear()
    estado_jogo['var']['jogador_azul'].clear()    

def msg_de_golo(nome,cor,estado_jogo):
    msg = tt.Turtle()
    msg.ht()
    msg.pencolor(cor)
    msg.write('Golo marcado por: ' + nome,align='center',font=('monaco',35,'bold'))
    estado_jogo['janela'].update()
    time.sleep(2)
    msg.clear()

def verifica_golo_jogador_vermelho(estado_jogo):
    '''
    Função responsável por verificar se um determinado jogador marcou golo.
    Para fazer esta verificação poderá fazer uso das constantes:
    LADO_MAIOR_AREA e
    START_POS_BALIZAS.
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador,
    criar um ficheiro que permita fazer a análise da jogada pelo VAR,
    e reiniciar o jogo com a bola ao centro.
    O ficheiro para o VAR deverá conter todas as informações necessárias
    para repetir a jogada, usando as informações disponíveis no objeto
    estado_jogo['var']. O ficheiro deverá ter o nome

    replay_golo_jv_[TotalGolosJogadorVermelho]ja[TotalGolosJogadorAzul].txt

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul]
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma
    ',', e cada coordenada é separada por um ';'.
    '''
    bolapos = estado_jogo['bola']['objeto'].pos()
    if (bolapos[0] < -((LARGURA_JANELA / 2) - LADO_MENOR_AREA) and -LADO_MAIOR_AREA / 2 <= bolapos[1]  <= LADO_MAIOR_AREA / 2):      
        estado_jogo['pontuacao_jogador_azul'] += 1
        update_board(estado_jogo)
        reinicio_jogo(estado_jogo)
        msg_de_golo(playerB, 'blue',estado_jogo)
        criar_ficheiro(estado_jogo)
        
   
def verifica_golo_jogador_azul(estado_jogo):
    bolapos = estado_jogo['bola']['objeto'].pos()
    if (bolapos[0] > ((LARGURA_JANELA / 2) - LADO_MENOR_AREA) and -LADO_MAIOR_AREA / 2 <= bolapos[1]  <= LADO_MAIOR_AREA / 2):       
        estado_jogo['pontuacao_jogador_vermelho'] += 1
        update_board(estado_jogo)
        reinicio_jogo(estado_jogo)
        msg_de_golo(playerA, 'red',estado_jogo)
        criar_ficheiro(estado_jogo)

def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador(estado_jogo,jogador):
    x_jogador = estado_jogo[jogador].xcor()
    y_jogador = estado_jogo[jogador].ycor()
    x_bola = estado_jogo['bola']['objeto'].xcor()
    y_bola = estado_jogo['bola']['objeto'].ycor()
    if (x_jogador - x_bola) ** 2 + (y_jogador - y_bola) ** 2 < (DEFAULT_TURTLE_SIZE) ** 2:
        if x_jogador < x_bola and y_jogador < y_bola:
            estado_jogo['bola']['dirx'] = random.uniform(0, 1)
            estado_jogo['bola']['diry'] = random.uniform(0, 1)
        elif x_jogador > x_bola and y_jogador < y_bola:
            estado_jogo['bola']['dirx'] = random.uniform(-1, 0)
            estado_jogo['bola']['diry'] = random.uniform(0, 1)
        elif x_jogador > x_bola and y_jogador > y_bola:
            estado_jogo['bola']['dirx'] = random.uniform(-1, 0)
            estado_jogo['bola']['diry'] = random.uniform(-1, 0)
        elif x_jogador < x_bola and y_jogador > y_bola:
            estado_jogo['bola']['dirx'] = random.uniform(0, 1)
            estado_jogo['bola']['diry'] = random.uniform(-1, 0)

def music():
    pygame.mixer.init()
    pygame.mixer.music.load('Top Of The Morning - TrackTribe.mp3')
    pygame.mixer.music.play()

def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['objeto'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    music()
    while True:
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
            guarda_posicoes_para_var(estado_jogo)
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            '''verifica_toque_jogador_azul(estado_jogo)'''
            verifica_toque_jogador(estado_jogo, 'jogador_vermelho')
        if estado_jogo['jogador_azul'] is not None:
            '''verifica_toque_jogador_vermelho(estado_jogo)'''
            verifica_toque_jogador(estado_jogo, 'jogador_azul')


if __name__ == '__main__':
    main()