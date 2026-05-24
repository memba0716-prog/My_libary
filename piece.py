import pygame
from constants import SQUARE_SIZE, PIECE_RADIUS, CROWN, WHITE, RED, BLACK

class Piece:
    """Класс, представляющий шашку"""
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color  # 'white' или 'red'
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def calc_pos(self):
        """Вычисление координат центра шашки для отрисовки"""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    def make_king(self):
        """Превращение шашки в дамку"""
        self.king = True
    
    def draw(self, win):
        """Отрисовка шашки на экране"""
        # Определяем цвет шашки
        color_value = WHITE if self.color == 'white' else RED
        
        # Рисуем тело шашки
        pygame.draw.circle(win, color_value, (self.x, self.y), PIECE_RADIUS)
        
        # Рисуем обводку
        pygame.draw.circle(win, BLACK, (self.x, self.y), PIECE_RADIUS, 2)
        
        # Если дамка - рисуем корону
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, 
                             self.y - CROWN.get_height() // 2))
    
    def move(self, row, col):
        """Перемещение шашки на новую позицию"""
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {self.color}, king={self.king})"
