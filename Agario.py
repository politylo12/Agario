from math import hypot
from pygame import*
from random import randint

my_player = [0,0,20]

init()

win = display.set_mode((800,800))
clok = time.Clock()

f = font.Font(None, 50)
all_players = []
lose = False

class Eat():
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.radius = r
        self.color = c
    def check_collision(self, player_x, player_y, player_r):
        dx = self.x - player_x
        dy = self.y - player_y

        return hypot(dx,dy) <= self.radius + player_r
eats = [Eat(randint(-2000,2000), randint(-2000,2000), 10,
            (randint(0,255), randint(0,255), randint(0,255))) for i in range(300)]
running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    win.fill((255,255,255))
    scale = max(0.3, min(50/my_player[2], 1.5))
    draw.circle(win, (0,255,0), (400,400), int(my_player[2]*scale))
    to_remove = []

    for eat in eats:
        if eat.check_collision(my_player[0], my_player[1], my_player[2]):
            to_remove.append(eat)
            my_player[2] += int(eat.radius*0.2)
        else:
            sx = int((eat.x - my_player[0])* scale + 400)
            sy = int((eat.y - my_player[1]) * scale + 400)

            draw.circle(win, eat.color, (sx,sy), int(eat.radius))

    for eat in to_remove:
        eats.remove(eat)

    display.update()
    clok.tick(60)

    keys = key.get_pressed()

    if keys[K_w]: my_player[1] -= 15
    if keys[K_s]: my_player[1] += 15
    if keys[K_a]: my_player[0] -= 15
    if keys[K_d]: my_player[0] += 15




