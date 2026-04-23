import asyncio
import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
IMAGEM_CHAO = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png"))
)
IMAGEM_BACKGROUND = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png"))
)
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -12
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.7 * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 180
    VELOCIDADE = 6

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.TOPO_CANO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.BASE_CANO = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.TOPO_CANO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.TOPO_CANO, (self.x, self.pos_topo))
        tela.blit(self.BASE_CANO, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.TOPO_CANO)
        base_mask = pygame.mask.from_surface(self.BASE_CANO)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 6
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaro, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    if passaro:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    chao.desenhar(tela)
    pygame.display.update()


async def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    relogio = pygame.time.Clock()

    while True:
        # Loop principal (permite reiniciar)
        passaro = Passaro(230, 350)
        chao = Chao(730)
        canos = [Cano(700)]
        pontos = 0
        rodando = True
        morto = False

        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                # Espaço ou Clique para pular/reiniciar
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    if morto:
                        rodando = False # Sai do loop interno para reiniciar
                    else:
                        passaro.pular()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if morto:
                        rodando = False
                    else:
                        passaro.pular()
            
            if not morto:
                passaro.mover()
                chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    if cano.colidir(passaro):
                        morto = True
                    if not cano.passou and cano.x < passaro.x:
                        cano.passou = True
                        adicionar_cano = True
                    cano.mover()
                    if cano.x + cano.TOPO_CANO.get_width() < 0:
                        remover_canos.append(cano)

                if adicionar_cano:
                    pontos += 1
                    canos.append(Cano(600))
                for cano in remover_canos:
                    canos.remove(cano)

                if passaro.y + passaro.imagem.get_height() > chao.y or passaro.y < 0:
                    morto = True

            desenhar_tela(tela, passaro, canos, chao, pontos)
            
            # ESSENCIAL PARA O PYGBAG / NAVEGADOR
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
