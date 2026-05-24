import pygame
from constants import ROWS, COLS, SQUARE_SIZE
from piece import Piece

class Board:
    """Класс, представляющий игровую доску"""
    
    def __init__(self):
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.create_board()
    
    def create_board(self):
        """Создание начальной расстановки шашек"""
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # Расстановка шашек
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                if row < 3:
                    # Белые шашки (светлые) - внизу доски
                    self.board[row][col] = Piece(row, col, 'white')
                elif row > 4:
                    # Красные шашки (темные) - вверху доски
                    self.board[row][col] = Piece(row, col, 'red')
    
    def draw(self, win):
        """Отрисовка доски и всех шашек"""
        self.draw_squares(win)
        self.draw_pieces(win)
    
    def draw_squares(self, win):
        """Отрисовка клеток доски"""
        win.fill((0, 0, 0))  # Черный фон
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, (210, 180, 140),  # Бежевый цвет для темных клеток
                                 (row * SQUARE_SIZE, col * SQUARE_SIZE, 
                                  SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_pieces(self, win):
        """Отрисовка всех шашек"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(win)
    
    def get_piece(self, row, col):
        """Получение шашки по координатам"""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
    
    def move(self, piece, row, col):
        """Перемещение шашки"""
        # Сохраняем информацию о взятии
        skipped = self._get_skipped_piece(piece, row, col)
        
        # Перемещаем шашку
        self.board[piece.row][piece.col], self.board[row][col] = None, piece
        piece.move(row, col)
        
        # Превращение в дамку
        if (piece.color == 'white' and row == ROWS - 1) or \
           (piece.color == 'red' and row == 0):
            piece.make_king()
        
        # Удаляем сбитую шашку
        if skipped:
            self.remove(skipped)
            return True
        return False
    
    def _get_skipped_piece(self, piece, new_row, new_col):
        """Определение сбитой шашки при прыжке"""
        row_diff = new_row - piece.row
        col_diff = new_col - piece.col
        
        if abs(row_diff) == 2:
            skipped_row = piece.row + row_diff // 2
            skipped_col = piece.col + col_diff // 2
            return self.board[skipped_row][skipped_col]
        return None
    
    def remove(self, piece):
        """Удаление шашки с доски"""
        self.board[piece.row][piece.col] = None
        if piece.color == 'white':
            self.white_left -= 1
        else:
            self.red_left -= 1
    
    def get_valid_moves(self, piece):
        """Получение всех возможных ходов для шашки"""
        moves = {}
        row, col = piece.row, piece.col
        color = piece.color
        
        # Направления движения
        directions = []
        if piece.king:
            # Дамка может ходить во все стороны
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Простая шашка: белые ходят вверх (уменьшение row), красные - вниз
            if color == 'white':
                directions = [(-1, -1), (-1, 1)]  # Вверх-влево, вверх-вправо
            else:
                directions = [(1, -1), (1, 1)]    # Вниз-влево, вниз-вправо
        
        # Обычные ходы
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if self.board[new_row][new_col] is None:
                    moves[(new_row, new_col)] = []
        
        # Ходы со взятием
        jumps = self._get_all_jumps(piece)
        moves.update(jumps)
        
        return moves
    
    def _get_all_jumps(self, piece):
        """Рекурсивный поиск всех возможных взятий"""
        jumps = {}
        row, col = piece.row, piece.col
        color = piece.color
        
        # Направления для прыжков
        directions = []
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if color == 'white':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            jump_row, jump_col = row + 2 * dr, col + 2 * dc
            mid_row, mid_col = row + dr, col + dc
            
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece and mid_piece.color != color:
                    if self.board[jump_row][jump_col] is None:
                        # Сохраняем информацию о сбитой шашке
                        jumps[(jump_row, jump_col)] = [mid_piece]
        
        return jumps
    
    def has_any_jump(self, color):
        """Проверка, есть ли у игрока обязательные взятия"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    jumps = self._get_all_jumps(piece)
                    if jumps:
                        return True
        return False
    
    def get_all_pieces(self, color):
        """Получение всех шашек указанного цвета"""
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def winner(self):
        """Определение победителя"""
        if self.red_left <= 0:
            return 'white'
        elif self.white_left <= 0:
            return 'red'
        return None