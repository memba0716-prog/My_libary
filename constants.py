import pygame

# Размеры окна
HEIGHT = 800 
WIDTH = 800 
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

# Цвета (RGB)
RED = (180, 50, 50)
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
GREEN = (50, 100, 50)
DARK_GREEN = (35, 75, 35)
BEIGE = (235, 205, 150)
BLUE = (70, 130, 200)
YELLOW = (255, 220, 100)

# Радиус шашки
PIECE_RADIUS = SQUARE_SIZE // 2 - 10

# Корона для дамки (загружаем и масштабируем)
try:
    CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (35, 25))
except:
    # Если файл не найден, создаем простую поверхность-заглушку
    CROWN = pygame.Surface((35, 25))
    CROWN.fill(YELLOW)

# FPS
FPS = 60