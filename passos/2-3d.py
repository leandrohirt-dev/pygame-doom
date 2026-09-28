import pygame
import math

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
mapa = [
    "###############",
    "#.....#.......#",
    "#.....#.......#",
    "#..#.....##...#",
    "#.............#",
    "#.....##..#...#",
    "####..#...#...#",
    "#.........#...#",
    "#......#......#",
    "###############",
]
T = 8
x, y, ang = 1.5, 4.5, 0.0
FOV = math.pi / 3
COLUNAS = 120
L = 600 // COLUNAS

def parede(px, py):
    return mapa[int(py)][int(px)] == "#"

def raio(a):
    c, s = math.cos(a), math.sin(a)
    d = 0
    while not parede(x + c * d, y + s * d):
        d += 0.02
    return d

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    k = pygame.key.get_pressed()
    ang += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 0.05
    passo = (k[pygame.K_UP] - k[pygame.K_DOWN]) * 0.08
    dx = math.cos(ang) * passo
    dy = math.sin(ang) * passo
    if not parede(x + dx * 4, y):
        x += dx
    if not parede(x, y + dy * 4):
        y += dy

    tela.fill("gray10")
    pygame.draw.rect(tela, "sienna4", (0, 200, 600, 200))
    for i in range(COLUNAS):
        a = ang - FOV / 2 + FOV * i / COLUNAS
        d = raio(a)
        px = x + math.cos(a) * d
        py = y + math.sin(a) * d
        d *= math.cos(a - ang)
        luz = max(30, 230 - d * 22)
        if abs(px - round(px)) < 0.03:
            luz *= 0.7
        h = min(400, 400 / d)
        cor = (luz, luz * 0.9, luz * 0.75)
        faixa = (i * L, 200 - h / 2, L, h)
        pygame.draw.rect(tela, cor, faixa)
        pygame.draw.line(tela, "yellow", (x * T, y * T),
                         (px * T, py * T))

    for my, linha in enumerate(mapa):
        for mx, c in enumerate(linha):
            if c == "#":
                bloco = (mx * T, my * T, T, T)
                pygame.draw.rect(tela, "gray40", bloco)
    pygame.draw.circle(tela, "white", (x * T, y * T), 5)

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()
