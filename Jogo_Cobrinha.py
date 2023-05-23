import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

musica_de_fundo = pygame.mixer.music.load(
    'musicas/X2Download.app - Let It Happen - Guitar Riff Cover (Attempt 2) (128 kbps).mp3')
pygame.mixer.music.play(-1)  # para tocar a musica de fundo o -1 faz rodar em loop
pygame.mixer.music.set_volume(0.1)  # Defina o volume para 0.1 (10%)

barulho_colisao = pygame.mixer.Sound(
    'musicas/Bass Drop - Sound Effect (HD)-YoutubeConvert.cc.wav')  # sound effect para quando tocar no objeto
barulho_colisao.set_volume(0.06)  # Defina o volume para 0.06 (06%)

fudeu=pygame.mixer.Sound(
    'musicas/TA FUDIDO FILHO DA PUTA EU VOU LHE PEGAR (UDYR)-YoutubeConvert.cc.wav')
fudeu.set_volume(0.07)

largura = 1080
altura = 720

x_cobra = altura / 2
y_cobra = altura / 2

velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = randint(60, 680)
y_maca = randint(50, 430)

pontos = 0
fonte = pygame.font.SysFont('arial', 40, True,True)  # definindo a fonte do texto 1 o nome da fonte , 2 tamanho da letra, 3 se quer em negrito,
# 4 se quer em italico

lista_cobra = []  # lista para fora, para nao ser resetada
comprimento_inicial = 5  # para determinar o tamanho da cobra

morreu = False

screen = pygame.display.set_mode((largura, altura))  # tamanho da tela
pygame.display.set_caption("Cobrinha")  # Titulo
relogio = pygame.time.Clock()  # para determinar o FPS


"         Funções      "


def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        # XeY = [x,y]
        # XeY[0] = x
        # XeY[1] = y
        pygame.draw.rect(screen, (0, 255, 0), (XeY[0], XeY[1], 50, 50))


def reiniciar_jogo():
    global pontos,comprimento_inicial,x_cobra,y_cobra,lista_cobra,lista_cabeca,x_maca,y_maca,morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = altura / 2
    y_cobra = altura / 2
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(60, 680)
    y_maca = randint(50, 430)
    morreu = False


while True:  # onde coloca o script do jogo para rodar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Codigo para quando clicar no x, ele fechar o jogo

        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade

    x_cobra+=x_controle
    y_cobra+=y_controle

    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))  # parametro , se quer anti-alising , cor

    relogio.tick(60)  # fps
    screen.fill((255, 255, 255))  # Cor da tela de fundo

    cobra = pygame.draw.rect(screen, (0, 255, 0), (x_cobra, y_cobra, 50, 50))
    maca = pygame.draw.rect(screen, (200, 0, 0), (x_maca, y_maca, 50, 50))
    # chao = pygame.draw.line(screen, (0, 0, 0), (0, 350), (720, 350), 5)
    if cobra.colliderect(maca):
        x_maca = randint(60, 680)
        y_maca = randint(50, 430)

        pontos += 1

        barulho_colisao.play()
        comprimento_inicial += 1

    lista_cabeca = []  # aramazena por onde a cobra anda
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1 :   # Diz se a cobra encostou nela mesma

        fonte2 = pygame.font.SysFont('arial ',20,True,True)
        mensagem='Game Over! Pressione a tecla "R" para jogar novamente!'
        texto_formatado=fonte2.render(mensagem,True,(0,0,0))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:

            if not pygame.mixer.get_busy():
                fudeu.play()
            screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            ret_texto.center = (largura//2, altura//2)
            screen.blit(texto_formatado,ret_texto)
            pygame.display.flip()

    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra > altura:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = altura

    if len(lista_cobra) > comprimento_inicial:    # Deleta o primeiro elemento da lista para ficar com o numero certo da cobra
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    screen.blit(texto_formatado, (890, 30))  # para aparecer a mensagem na posicao indicada
    pygame.display.flip()  # para ficar atualizando o jogo
