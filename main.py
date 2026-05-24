import sys
import pygame
from constants import WIDTH, HEIGHT, FPS, WHITE, RED, BEIGE
from game import Game

def draw_text(win, text, size, x, y, color):
    """Вспомогательная функция для отображения текста"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def main():
    """Основная функция - точка входа в игру"""
    # Инициализация Pygame
    pygame.init()
    
    # Создание окна
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Шашки")
    
    # Создание игрового объекта
    game = Game(win)
    
    # Переменные игрового цикла
    running = True
    clock = pygame.time.Clock()
    winner_message = None
    game_over = False
    
    # Основной игровой цикл
    while running:
        clock.tick(FPS)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()  # Гарантированный выход из программы
            
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = game.get_row_col_from_mouse(pos)
                game.select(row, col)
            
            # Перезапуск игры по клавише R
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Сброс игры
                    game = Game(win)
                    game_over = False
                    winner_message = None
                    sys.stdout.write("Игра перезапущена\n")  # Логирование в консоль
        
        # Обновление игры
        if not game_over:
            game.update()
            
            # Проверка победителя
            winner_message = game.check_winner()
            if winner_message:
                game_over = True
                
                # Вывод результата в консоль с помощью sys.stdout
                sys.stdout.write(f"\n=== ИГРА ОКОНЧЕНА ===\n{winner_message}\n")
                sys.stdout.flush()
        
        # Отображение сообщения о победе
        if game_over and winner_message:
            # Затемняем экран
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            win.blit(overlay, (0, 0))
            
            # Рисуем панель с сообщением
            panel_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 6)
            pygame.draw.rect(win, BEIGE, panel_rect)
            pygame.draw.rect(win, (0, 0, 0), panel_rect, 3)
            
            draw_text(win, winner_message, 48, WIDTH // 2, HEIGHT // 3 + 50, (50, 50, 50))
            draw_text(win, "Нажмите R для новой игры", 28, WIDTH // 2, HEIGHT // 2 + 50, (100, 100, 100))
            
            pygame.display.update()
        
        # Отображение текущего игрока (если игра не окончена)
        if not game_over:
            current_player = "Белые" if game.turn == 'white' else "Красные"
            player_color = WHITE if game.turn == 'white' else RED
            draw_text(win, f"Ход: {current_player}", 36, WIDTH - 100, 30, player_color)
        
        pygame.display.flip()
    
    # Завершение работы (резервный выход)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Обработка аргументов командной строки с помощью sys.argv
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            sys.stdout.write("""
Шашки
Управление:
    - Клик левой кнопкой мыши: выбор шашки / ход
    - Клавиша R: перезапуск игры
    - Закрытие окна или Ctrl+C: выход

Аргументы командной строки:
    --help, -h    Показать эту справку
    --debug       Включить отладочный режим (дополнительный вывод в консоль)
""")
            sys.exit(0)
        elif sys.argv[1] == "--debug":
            sys.stdout.write("Отладочный режим включен\n")
            # В отладочном режиме можно выводить дополнительную информацию
            main()
        else:
            sys.stderr.write(f"Неизвестный аргумент: {sys.argv[1]}\n")
            sys.stderr.write("Используйте --help для справки\n")
            sys.exit(1)
    else:
        main()