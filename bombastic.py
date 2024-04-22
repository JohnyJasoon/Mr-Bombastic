import curses
import time
import threading
import random

COLUMNS = 50
ROWS = 25

class Board:

    def __init__(self):
        self.score = 0
        self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.player = (int(ROWS/2), int(COLUMNS/2))
        self.direction = 1  # 1: Góra, 2: Prawo, 3: Dół, 4: Lewo
        self.bombs = {}
        self.game_over = False

        # Użyj Lock jako bazy dla Condition
        self.lock = threading.Lock()
        self.condition_move = threading.Condition(self.lock)

    def __str__(self):
        score = f"Wynik: {self.score}"
        area = "#" * COLUMNS + score + "\n"
        for row in self.field:
            area += "#"
            for slot in row:
                area += slot
            area += "#\n"
        area += "#" * COLUMNS
        return area

    def refresh(self):
        with self.lock:
            self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
            r, c = self.player
            self.field[r][c] = 'P'
            for (r, c), _ in self.bombs.items():
                self.field[r][c] = 'B'

    def controller(self, new_direction):
        with self.condition_move:
            if not abs(self.direction - new_direction) == 2:
                self.direction = new_direction
            self.condition_move.notify()

    def place_bomb(self):
        with self.lock:
            r, c = self.player
            self.bombs[(r, c)] = time.time() + 2  # Czas wybuchu bomby po 2 sekundach

    def check_bombs(self):
        with self.lock:
            current_time = time.time()
            exploded_bombs = []
            for (r, c), explode_time in list(self.bombs.items()):
                if current_time >= explode_time:
                    exploded_bombs.append((r, c))
            for bomb in exploded_bombs:
                del self.bombs[bomb]

    def move(self):
        with self.condition_move:
            r, c = self.player
            if self.direction == 1:
                r -= 1
            elif self.direction == 2:
                c += 1
            elif self.direction == 3:
                r += 1
            elif self.direction == 4:
                c -= 1

            # Zapobieganie wychodzeniu poza planszę
            r = max(0, min(ROWS - 1, r))
            c = max(0, min(COLUMNS - 1, c))

            self.player = (r, c)
            self.condition_move.notify()  # Notify jest bezpieczne, ponieważ blokada jest nabyta

def controller(window, board):
    while not board.game_over:
        char = window.getch()
        if char == curses.KEY_UP:
            board.controller(1)
        elif char == curses.KEY_RIGHT:
            board.controller(2)
        elif char == curses.KEY_DOWN:
            board.controller(3)
        elif char == curses.KEY_LEFT:
            board.controller(4)
        elif char == ord(' '):  # Spacja do umieszczania bomby
            board.place_bomb()

def bomb_manager(board):
    while not board.game_over:
        board.check_bombs()
        time.sleep(0.1)  # Co 100 ms sprawdzaj bomby

def start(window):
    board = Board()

    control_thread = threading.Thread(target=controller, args=(window, board))
    control_thread.start()

    bomb_thread = threading.Thread(target=bomb_manager, args=(board,))
    bomb_thread.start()

    while not board.game_over:
        window.clear()
        window.insstr(0, 0, str(board))
        window.refresh()
        time.sleep(0.2)

        board.move()
        board.refresh()

    control_thread.join()
    bomb_thread.join()

if __name__ == "__main__":
    curses.wrapper(start)
