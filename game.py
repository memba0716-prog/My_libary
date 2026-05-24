import pygame
from constants import SQUARE_SIZE, ROWS, COLS, BLUE, WHITE, RED
from board import Board

class Game:
    """Класс, управляющий игровым процессом"""
    
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = 'white'  # Белые ходят первыми
        self.selected = None
        self.valid_moves = {}
    
    def update(self):
        """Обновление отображения"""
        self.board.draw(self.win)
        self.draw_valid_moves()
        pygame.display.update()
    
    def draw_valid_moves(self):
        """Подсветка возможных ходов для выбранной шашки"""
        if self.selected:
            for move in self.valid_moves:
                row, col = move
                pygame.draw.circle(self.win, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   15)
    
    def select(self, row, col):
        """Выбор шашки или выполнение хода"""
        # Если уже выбрана шашка - пробуем сделать ход
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        # Выбор новой шашки
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self, row, col):
        """Выполнение хода"""
        piece = self.selected
        if (row, col) in self.valid_moves:
            # Определяем, было ли взятие
            was_jump = abs(row - piece.row) == 2
            
            # Выполняем перемещение
            self.board.move(piece, row, col)
            
            # Проверяем возможность повторного взятия
            if was_jump:
                new_jumps = self.board.get_valid_moves(piece)
                if new_jumps:
                    self.selected = piece
                    self.valid_moves = new_jumps
                    return True
            
            # Смена игрока
            self.change_turn()
        else:
            return False
        
        return True
    
    def change_turn(self):
        """Смена очередности хода"""
        self.selected = None
        self.valid_moves = {}
        
        if self.turn == 'white':
            self.turn = 'red'
        else:
            self.turn = 'white'
        
        # Проверяем, есть ли у текущего игрока обязательные взятия
        if self.board.has_any_jump(self.turn):
            # Если есть - игрок обязан взять, подсветим его шашки особым цветом? (опционально)
            pass
    
    def get_row_col_from_mouse(self, pos):
        """Преобразование координат мыши в индексы клетки"""
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return int(row), int(col)
    
    def check_winner(self):
        """Проверка победителя"""
        winner = self.board.winner()
        if winner == 'white':
            return "Белые победили!"
        elif winner == 'red':
            return "Красные победили!"
        return None