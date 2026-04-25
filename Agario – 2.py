from math import hypot
from socket import *
from pygame import *
from threading import Thread
from random import randint

# Налаштування мережі
sock = socket(AF_INET, SOCK_STREAM)
try:
    sock.connect(("0.tcp.eu.ngrok.io", 15374))
    data = sock.recv(64).decode().strip()
    my_data = list(map(int, data.split(',')))
except Exception as e:
    print(f"Помилка підключення: {e}")
    exit()

my_id = my_data[0]
my_player = my_data[1:]  # [x, y, radius]
sock.setblocking(False)

init()
WIDTH, HEIGHT = 800, 800
win = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
f = font.Font(None, 50)

all_players = []
running = True
lose = False


def receive_data():
    global all_players, running, lose
    while running:
        try:
            data = sock.recv(4096).decode().strip()
            if "LOSE" in data:
                lose = True
            elif data:
                # Очікуємо формат: id,x,y,r|id,x,y,r
                parts = data.split('|')
                new_players = []
                for p in parts:
                    vals = p.split(',')
                    if len(vals) == 4:
                        new_players.append(list(map(int, vals)))
                all_players = new_players
        except:
            pass


Thread(target=receive_data, daemon=True).start()


class Eat():
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.radius = r
        self.color = c

    def check_collision(self, player_x, player_y, player_r):
        return hypot(self.x - player_x, self.y - player_y) <= player_r


eats = [Eat(randint(-1000, 1000), randint(-1000, 1000), 7,
            (randint(0, 255), randint(0, 255), randint(0, 255))) for i in range(200)]

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    if not lose:
        keys = key.get_pressed()
        if keys[K_w]: my_player[1] -= 5
        if keys[K_s]: my_player[1] += 5
        if keys[K_a]: my_player[0] -= 5
        if keys[K_d]: my_player[0] += 5

        # Відправка даних на сервер
        try:
            msg = f"{my_id},{my_player[0]},{my_player[1]},{my_player[2]}"
            sock.send(msg.encode())
        except:
            pass

    win.fill((255, 255, 255))

    # Розрахунок масштабу (камера)
    scale = max(0.2, min(50 / my_player[2], 1.5))
    CX, CY = WIDTH // 2, HEIGHT // 2

    # Малюємо їжу та перевіряємо колізії
    to_remove = []
    for eat in eats:
        if eat.check_collision(my_player[0], my_player[1], my_player[2]):
            to_remove.append(eat)
            my_player[2] += 1  # Збільшення радіусу
        else:
            sx = int((eat.x - my_player[0]) * scale + CX)
            sy = int((eat.y - my_player[1]) * scale + CY)
            if 0 < sx < WIDTH and 0 < sy < HEIGHT:  # Малюємо лише те, що в кадрі
                draw.circle(win, eat.color, (sx, sy), int(eat.radius * scale))

    for eat in to_remove:
        if eat in eats: eats.remove(eat)

    # Малюємо інших гравців
    for p in all_players:
        if p[0] == my_id:
            continue
        sx = int((p[1] - my_player[0]) * scale + CX)
        sy = int((p[2] - my_player[1]) * scale + CY)
        draw.circle(win, (255, 0, 0), (sx, sy), int(p[3] * scale))

    # Малюємо себе (завжди в центрі)
    draw.circle(win, (0, 255, 0), (CX, CY), int(my_player[2] * scale))

    if lose:
        t = f.render("Ти програв!", True, (200, 0, 0))
        win.blit(t, (WIDTH // 2 - 100, HEIGHT // 2))

    display.update()
    clock.tick(60)

quit()



