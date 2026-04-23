import asyncio
import pygame
import os
import random

# Configurações globais
TELA_LARGURA = 500
TELA_ALTURA = 800

async def main():
    # INICIALIZAÇÃO BLINDADA
    pygame.init()
    pygame.font.init()
    
    # Carregamento de Assets
    try:
        # Procurar imagens na pasta 'imgs' relativa ao main.py
        base_path = os.path.dirname(__file__)
        img_dir = os.path.join(base_path, "imgs")
        
        IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "pipe.png")))
        IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "base.png")))
        IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "bg.png")))
        IMAGENS_PASSARO = [
            pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(img_dir, "bird3.png"))),
        ]
        FONTE_PONTOS = pygame.font.SysFont("arial", 50)
    except pygame.error as e:
        print(f"Erro ao carregar imagens: {e}")
        return

    class Passaro:
        IMGS = IMAGENS_PASSARO
        ROTACAO_MAXIMA = 25
        VELOCIDADE_ROTACAO = 20
        TEMPO_ANIMACAO = 5
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.angulo = 0
            self.velocidade = 0
            self.altura = self.y
            self.tempo = 0
            self.contagem_imagem = 0
            self.imagem = self.IMGS[0]
        def pular(self):
            self.velocidade = -8.5
            self.tempo = 0
            self.altura = self.y
        def mover(self):
            self.tempo += 1
            deslocamento = 1.2 * (self.tempo**2) + self.velocidade * self.tempo
            if deslocamento > 16: deslocamento = 16
            elif deslocamento < 0: deslocamento -= 2
            self.y += deslocamento
            if deslocamento < 0 or self.y < (self.altura + 50):
                if self.angulo < self.ROTACAO_MAXIMA: self.angulo = self.ROTACAO_MAXIMA
            else:
                if self.angulo > -90: self.angulo -= self.VELOCIDADE_ROTACAO
        def desenhar(self, tela):
            self.contagem_imagem += 1
            if self.contagem_imagem < self.TEMPO_ANIMACAO: self.imagem = self.IMGS[0]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2: self.imagem = self.IMGS[1]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3: self.imagem = self.IMGS[2]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4: self.imagem = self.IMGS[1]
            else: self.imagem = self.IMGS[0]; self.contagem_imagem = 0
            if self.angulo <= -80: self.imagem = self.IMGS[1]; self.contagem_imagem = self.TEMPO_ANIMACAO * 2
            imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
            pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
            retangulo = imagem_rotacionada.get_rect(center=pos_centro)
            tela.blit(imagem_rotacionada, retangulo.topleft)
        def get_mask(self): return pygame.mask.from_surface(self.imagem)

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
        def mover(self): self.x -= self.VELOCIDADE
        def desenhar(self, tela):
            tela.blit(self.TOPO_CANO, (self.x, self.pos_topo))
            tela.blit(self.BASE_CANO, (self.x, self.pos_base))
        def colidir(self, passaro):
            p_mask = passaro.get_mask()
            t_mask = pygame.mask.from_surface(self.TOPO_CANO)
            b_mask = pygame.mask.from_surface(self.BASE_CANO)
            dist_t = (self.x - passaro.x, self.pos_topo - round(passaro.y))
            dist_b = (self.x - passaro.x, self.pos_base - round(passaro.y))
            if p_mask.overlap(t_mask, dist_t) or p_mask.overlap(b_mask, dist_b): return True
            return False

    class Chao:
        VELOCIDADE = 6
        LARGURA = IMAGEM_CHAO.get_width()
        def __init__(self, y):
            self.y, self.x1, self.x2 = y, 0, self.LARGURA
        def mover(self):
            self.x1 -= self.VELOCIDADE
            self.x2 -= self.VELOCIDADE
            if self.x1 + self.LARGURA < 0: self.x1 = self.x2 + self.LARGURA
            if self.x2 + self.LARGURA < 0: self.x2 = self.x1 + self.LARGURA
        def desenhar(self, tela):
            tela.blit(IMAGEM_CHAO, (self.x1, self.y))
            tela.blit(IMAGEM_CHAO, (self.x2, self.y))

    def desenhar_tela(tela, passaro, canos, chao, pontos):
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        if passaro: passaro.desenhar(tela)
        for cano in canos: cano.desenhar(tela)
        texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
        chao.desenhar(tela)
        pygame.display.update()

    # --- Início do Loop Real ---
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    relogio = pygame.time.Clock()

    while True:
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
                    pygame.quit(); return
                if evento.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE) or evento.type == pygame.MOUSEBUTTONDOWN:
                        if morto: rodando = False
                        else: passaro.pular()
            
            if not morto:
                passaro.mover()
                chao.mover()
                adc_cano = False
                remover = []
                for cano in canos:
                    if cano.colidir(passaro): morto = True
                    if not cano.passou and cano.x < passaro.x:
                        cano.passou = True; adc_cano = True
                    cano.mover()
                    if cano.x + cano.TOPO_CANO.get_width() < 0: remover.append(cano)
                if adc_cano:
                    pontos += 1; canos.append(Cano(600))
                for c in remover: canos.remove(c)
                if passaro.y + IMAGENS_PASSARO[0].get_height() > chao.y or passaro.y < 0: morto = True

            desenhar_tela(tela, passaro, canos, chao, pontos)
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
