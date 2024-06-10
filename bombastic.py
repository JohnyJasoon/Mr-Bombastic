import curses
import time
import threading
import random
from threading import Semaphore

COLUMNS = 50
ROWS = 25
EXPLOSION_DURATION = 0.5  # Duration to show explosion in seconds
ENEMY_SPAWN_RATE = 5  # In seconds, how often new enemies spawn

class Board:
    def __init__(self):
        self.score = 0
        self.enemy_count = 0
        self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.player = (int(ROWS / 2), int(COLUMNS / 2))
        self.bombs = {}
        self.explosions = {}
        self.enemies = []
        self.game_over = False
        self.lock = threading.Lock()
        self.bomb_sem = Semaphore(value=1)
        self.enemy_sem = Semaphore(value=1)
        self.initialize_walls()
        self.spawn_initial_enemies()

    def initialize_walls(self, wall_density=0.15, wall_proportion=0.5):
        num_walls = int(ROWS * COLUMNS * wall_density)
        for _ in range(num_walls):
            while True:
                r = random.randint(0, ROWS - 1)
                c = random.randint(0, COLUMNS - 1)
                if self.is_position_safe_for_walls(r, c):
                    wall_type=random.randint(1, 100)/100
                    if wall_type <= wall_proportion:
                        self.field[r][c] = '#'
                    else:
                        self.field[r][c] = '&'
                    break

    def is_position_safe_for_walls(self, r, c):
        pr, pc = self.player
        if (pr == r and abs(pc - c) <= 1) or (pc == c and abs(pr - r) <= 1):
            return False
        return self.field[r][c] == " "

    def spawn_initial_enemies(self):
        for _ in range(5):
            self.spawn_enemy()

    def spawn_enemy(self):
        with self.enemy_sem:
            while True:
                r = random.randint(0, ROWS - 1)
                c = random.randint(0, COLUMNS - 1)
                if self.field[r][c] == " ":
                    self.enemies.append(Enemy(r, c))
                    self.enemy_count+=1
                    break

    def __str__(self):
        with self.lock:
            score = f" Score: {self.score} "
            #time = f" Time: {self.time} up to 180s"
            enemy_count = f"Enemies: {self.enemy_count}"
            area = "#" * (COLUMNS + 2) + "\n"
            for row in self.field:
                area += "#" + "".join(row) + "#\n"
            area += "#" * (COLUMNS + 2) + score + "|||" + enemy_count
            return area

    def refresh(self):
        with self.lock:
            temp_field = [[self.field[r][c] if self.field[r][c] == '#' or self.field[r][c] == '&' else " " for c in range(COLUMNS)] for r in range(ROWS)]
            r, c = self.player
            temp_field[r][c] = 'B'
            self.bomb_sem.acquire()
            for (r, c), _ in self.bombs.items():
                temp_field[r][c] = 'o'
            self.bomb_sem.release()
            self.enemy_sem.acquire()
            for enemy in self.enemies:
                temp_field[enemy.row][enemy.col] = 'E'
            self.enemy_sem.release()
            for (r, c), expire_time in self.explosions.items():
                if time.time() < expire_time:
                    temp_field[r][c] = '*'
            self.field = temp_field

    def move(self, new_direction):
        with self.lock:
            r, c = self.player
            if new_direction == 1:
                r -= 1
            elif new_direction == 2:
                c += 1
            elif new_direction == 3:
                r += 1
            elif new_direction == 4:
                c -= 1

            if 0 <= r < ROWS and 0 <= c < COLUMNS and self.field[r][c] != '#' and self.field[r][c] != '&':
                self.player = (r, c)
            if self.field[r][c] == 'E':
                self.game_over = True

    def place_bomb(self):
        with self.lock:
            r, c = self.player
            if (r, c) not in self.bombs:
                self.bomb_sem.acquire()
                self.bombs[(r, c)] = time.time() + 2  # Bomb explodes after 2 seconds
                self.bomb_sem.release()

    def update_bombs_and_explosions(self):
        while not self.game_over:
            current_time = time.time()
            to_explode = []
            self.bomb_sem.acquire()
            for (r, c), explode_time in list(self.bombs.items()):
                if current_time >= explode_time:
                    to_explode.append((r, c))
            for bomb in to_explode:
                self.explode_bomb(bomb)
                del self.bombs[bomb]
            self.bomb_sem.release()
            time.sleep(0.1)

    def explode_bomb(self, position):
        r, c = position
        explosion_range = 3  # Explosion range is 3 tiles in each direction

        with self.lock:
            explosion_positions = [(r, c)]
            explosion_dir_stop = [0, 0, 0, 0]
            for i in range(1, explosion_range + 1):
                if r - i >= 0 and self.field[r - i][c] != '*' and explosion_dir_stop[0] == 0:
                    if self.field[r - i][c] == '#':
                        explosion_dir_stop[0] = 1
                    else:
                        explosion_positions.append((r - i, c))
                if r + i < ROWS and self.field[r + i][c] != '*' and explosion_dir_stop[1] == 0:
                    if self.field[r + i][c] == '#':
                        explosion_dir_stop[1] = 1
                    else:
                        explosion_positions.append((r + i, c))
                if c - i >= 0 and self.field[r][c - i] != '*' and explosion_dir_stop[2] == 0:
                    if self.field[r][c - i] == '#':
                        explosion_dir_stop[2] = 1
                    else:
                        explosion_positions.append((r, c - i))
                if c + i < COLUMNS and self.field[r][c + i] != '*' and explosion_dir_stop[3] == 0:
                    if self.field[r][c + i] == '#':
                        explosion_dir_stop[0] = 1
                    else:
                        explosion_positions.append((r, c + i))

            for (er, ec) in explosion_positions:
                self.explosions[(er, ec)] = time.time() + EXPLOSION_DURATION
                if (er, ec) == self.player:
                    self.game_over = True
                for enemy in self.enemies:
                    if (er, ec) == (enemy.row, enemy.col):
                        self.enemies.remove(enemy)
                        self.enemy_count -= 1
                        self.score += 10

    def clear_explosions(self):
        while not self.game_over:
            with self.lock:
                current_time = time.time()
                self.explosions = {k: v for k, v in self.explosions.items() if current_time < v}
            time.sleep(0.1)

    def move_enemies(self):
        while not self.game_over:
            with self.enemy_sem:
                for enemy in self.enemies:
                    enemy.move(self.field)
            time.sleep(0.5)

    def spawn_enemies(self):
        while not self.game_over:
            self.spawn_enemy()
            time.sleep(ENEMY_SPAWN_RATE)


class Enemy:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, field):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLUMNS and field[nr][nc] == " ":
                self.row, self.col = nr, nc
                break


def controller(window, board):
    while not board.game_over:
        char = window.getch()
        if char == curses.KEY_UP:
            board.move(1)
        elif char == curses.KEY_RIGHT:
            board.move(2)
        elif char == curses.KEY_DOWN:
            board.move(3)
        elif char == curses.KEY_LEFT:
            board.move(4)
        elif char == ord(' '):  # Space to place a bomb
            board.place_bomb()
        board.refresh()


def start(window):
    window.nodelay(True)
    curses.curs_set(0)
    board = Board()
    control_thread = threading.Thread(target=controller, args=(window, board))
    bomb_thread = threading.Thread(target=board.update_bombs_and_explosions)
    explosion_clean_thread = threading.Thread(target=board.clear_explosions)
    enemy_move_thread = threading.Thread(target=board.move_enemies)
    enemy_spawn_thread = threading.Thread(target=board.spawn_enemies)

    control_thread.start()
    bomb_thread.start()
    explosion_clean_thread.start()
    enemy_move_thread.start()
    enemy_spawn_thread.start()

    while not board.game_over:
        window.clear()
        height, width = window.getmaxyx()
        board_str = str(board)
        if len(board_str.split('\n')) <= height and max(map(len, board_str.split('\n'))) <= width:
            window.addstr(0, 0, board_str)
        else:
            window.addstr(0, 0, "Window size too small!")
        window.refresh()
        time.sleep(0.001)


    control_thread.join()
    bomb_thread.join()
    explosion_clean_thread.join()
    enemy_move_thread.join()
    enemy_spawn_thread.join()


if __name__ == "__main__":
    curses.wrapper(start)