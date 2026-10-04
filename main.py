import math
import pygame
from random import randint

# Mono color list
#---------------------------
C_BLACK = (0, 0, 0)
C_LIGHTGREY = (209, 209, 214)
C_GREY = (96, 96, 96)
C_WHITE = (255, 255, 255)
#---------------------------
# Colorful color list
RN_COLOR = [
    (245, 30, 30), # red
    (245, 55, 100), # magenta
    (245, 120, 55), # orange
    (220, 195, 50), # yellow
    (145, 220, 30), # lime
    (20, 210, 30), # green
    (20, 215, 180), # mint
    (15, 135, 215), # light blue
    (15, 25, 220), # dark blue
    (135, 15, 220) # purple
]

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Bouncing Ball")

class Ball:

    def __init__(self, x_pos, y_pos, rad, x_vel, y_vel, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rad = rad
        self.color = color

        self.x_vel = x_vel
        self.y_vel = y_vel

        self.line_trail = []
        self.max_line_trail = 250

    def draw(self):
        if len(self.line_trail) > 1:
            pygame.draw.lines(SCREEN, C_LIGHTGREY, False, self.line_trail, 1)

        pygame.draw.circle(
            SCREEN,
            self.color,
            (self.x_pos, self.y_pos),
            self.rad
        )

    def update_position(self, obs_x, obs_y, obs_rad):
        self.x_pos += (self.x_vel * self.rad) / 10
        self.y_pos += (self.y_vel * self.rad) / 10

        # Check ball to wall bounce
        if self.x_pos - self.rad <= 0 or self.x_pos + self.rad >= WIDTH:
            self.x_vel *= - 1

        if self.y_pos - self.rad <= 0 or self.y_pos + self.rad >= HEIGHT:
            self.y_vel *= - 1
        
        dist_x = self.x_pos - obs_x
        dist_y = self.y_pos - obs_y

        dist_xy = math.hypot(dist_x, dist_y)
        min_dist = self.rad + obs_rad

        # Check ball to obstacle bounce
        if 0 < dist_xy < min_dist:
            nx, ny = (dist_x / dist_xy), (dist_y / dist_xy)

            self.x_pos = obs_x + (nx * min_dist)
            self.y_pos = obs_y + (ny * min_dist)

            refl_vel = (self.x_vel * nx) + (self.y_vel * ny)
            if refl_vel < 0:
                self.x_vel -= 2 * refl_vel * nx
                self.y_vel -= 2 * refl_vel * ny

        self.line_trail.append((self.x_pos, self.y_pos))
        if len(self.line_trail) > self.max_line_trail:
            self.line_trail.pop(0)
        

def main():
    run = True

    obs_x, obs_y, obs_rad = (WIDTH / 2), (HEIGHT / 2), 40
    obstacle = Ball(obs_x, obs_y, obs_rad, 0, 0, C_GREY)

    balls = [
        Ball(WIDTH / 2, HEIGHT / 2, 16, 0.51, 0.3, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 15, -0.44, 0.25, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 19, 0.24, 0.5, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 17, 0.3, -0.43, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 20, -0.42, -0.22, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 14, 0.62, -0.57, C_BLACK),
        Ball(WIDTH / 2, HEIGHT / 2, 24, -0.35, 0.4, C_BLACK)
    ]

    while run:
        CLOCK.tick(480)
        SCREEN.fill(C_WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        obstacle.draw()

        for ball in balls:
            ball.update_position(obs_x, obs_y, obs_rad)
            ball.draw()

        # Check ball to ball bounce
        for i in  range(len(balls)):
            for j in range(i + 1, len(balls)):

                b1, b2 = balls[i], balls[j]
                dx = b2.x_pos - b1.x_pos
                dy = b2.y_pos - b1.y_pos
                dist_b1b2 = math.hypot(dx, dy)
                
                if 0 < dist_b1b2 < b1.rad + b2.rad:
                    b_nx, b_ny = dx / dist_b1b2, dy / dist_b1b2

                    b_ovr = (b1.rad + b2.rad) - dist_b1b2
                    b1.x_pos -= b_nx * b_ovr / 2
                    b1.y_pos -= b_ny * b_ovr / 2
                    b2.x_pos += b_nx * b_ovr / 2
                    b2.y_pos += b_ny * b_ovr / 2

                    n_vel = (b1.x_vel - b2.x_vel) * b_nx + (b1.y_vel - b2.y_vel) * b_ny
                
                    if n_vel > 0:
                        push = 2 * n_vel / (1 / b1.rad + 1 / b2.rad)
                        b1.x_vel -= (push / b1.rad) * b_nx
                        b1.y_vel -= (push / b1.rad) * b_ny
                        b2.x_vel += (push / b2.rad) * b_nx
                        b2.y_vel += (push / b2.rad) * b_ny            

                    b1.color, b2.color = RN_COLOR[randint(0, 9)], RN_COLOR[randint(0, 9)]

        pygame.display.update()

    pygame.quit()

main()