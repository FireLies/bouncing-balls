import math
import pygame

# Color list
#---------------------------
C_BLACK = (0, 0, 0)
C_GREY = (209, 209, 214)
C_WHITE = (255, 255, 255)
C_RED = (255, 0, 0)
#---------------------------

pygame.init()

WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Bouncing Balls")

class Balls:

    def __init__(self, x_pos, y_pos, radius, x_vel, y_vel, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color

        self.x_vel = x_vel
        self.y_vel = y_vel

        self.line_trail = []
        self.max_line_trail = 500

    def draw(self):
        if len(self.line_trail) > 1:
            pygame.draw.lines(SCREEN, C_GREY, False, self.line_trail, 1)

        pygame.draw.circle(
            SCREEN,
            self.color,
            (self.x_pos, self.y_pos),
            self.radius
        )

    def update_position(self, obs_x, obs_y, obs_rad):
        self.x_pos += (self.x_vel * self.radius) / 10
        self.y_pos += (self.y_vel * self.radius) / 10

        if self.x_pos - self.radius <= 0 or self.x_pos + self.radius >= WIDTH:
            self.x_vel *= - 1

        if self.y_pos - self.radius <= 0 or self.y_pos + self.radius >= HEIGHT:
            self.y_vel *= - 1
        
        dist_x = self.x_pos - obs_x
        dist_y = self.y_pos - obs_y

        dist_xy = math.hypot(dist_x, dist_y)
        min_dist = self.radius + obs_rad

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

    obs_x, obs_y, obs_rad = (WIDTH / 2), (HEIGHT / 2), 30
    obstacle = Balls(obs_x, obs_y, obs_rad, 0, 0, C_RED)

    circles = [
        Balls(WIDTH / 2, HEIGHT / 2, 16, 0.51, 0.3, C_BLACK),
        Balls(WIDTH / 2, HEIGHT / 2, 12, -0.44, 0.25, C_BLACK),
        Balls(WIDTH / 2, HEIGHT / 2, 10, 0.24, 0.5, C_BLACK),
        Balls(WIDTH / 2, HEIGHT / 2, 17, 0.3, -0.43, C_BLACK),
        Balls(WIDTH / 2, HEIGHT / 2, 7, -0.42, -0.22, C_BLACK)
    ]

    while run:

        SCREEN.fill(C_WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        obstacle.draw()

        for c in circles:
            c.update_position(obs_x, obs_y, obs_rad)
            c.draw()

        pygame.display.update()
        CLOCK.tick(480)

    pygame.quit()

main()