import math
import pygame
from random import randint, uniform

# Color list
#---------------------------
C_BLACK = (0, 0, 0)
C_LIGHTGREY = (209, 209, 214)
C_GREY = (96, 96, 96)
C_WHITE = (255, 255, 255)
C_RED = (255, 0, 0)
#---------------------------

pygame.init()
pygame.mixer.init()

# GLobal variables
# -----------------------------------------------------------------
WIDTH = HEIGHT = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

BALL_DISSAPEAR = pygame.mixer.Sound("audio\\ball_dissapear.mp3")
OBSTACLE_HIT = pygame.mixer.Sound("audio\\obstacle_hit.mp3")
# -----------------------------------------------------------------

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
        self.max_line_trail = 150

    def draw(self):
        if len(self.line_trail) > 1:
            pygame.draw.lines(SCREEN, self.color, False, self.line_trail, 1)

        pygame.draw.circle(
            SCREEN,
            self.color,
            (self.x_pos, self.y_pos),
            self.rad
        )

    def update_position(self, obs_x, obs_y, obs_rad, max_ball_rad):
        self.x_pos += (self.x_vel * self.rad) / max_ball_rad
        self.y_pos += (self.y_vel * self.rad) / max_ball_rad

        # Check ball to wall bounce
        if self.x_pos - self.rad <= 0 or self.x_pos + self.rad >= WIDTH:
            self.x_vel *= - 1
            self.color = C_LIGHTGREY

        if self.y_pos - self.rad <= 0 or self.y_pos + self.rad >= HEIGHT:
            self.y_vel *= - 1
            self.color = C_LIGHTGREY
        
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

            if self.rad < 10:
                self.rad += 1
            else:
                self.rad += uniform(-20, 5)

            OBSTACLE_HIT.play()
            self.color = C_BLACK

        self.line_trail.append((self.x_pos, self.y_pos))
        if len(self.line_trail) > self.max_line_trail:
            self.line_trail.pop(0)
        

def main():
    run = True

    font_style = pygame.font.SysFont('Arial', 20, True)

    obs_x, obs_y, obs_rad = (uniform(15, WIDTH)), (uniform(15, HEIGHT)), 5
    obstacle = Ball(obs_x, obs_y, obs_rad, 0, 0, C_GREY)

    balls = []
    max_ball_rad = 10
    num_of_balls = 50
    spwn_xy = 25

    for n in range(0, num_of_balls):
        balls.append(
            Ball(
                randint(spwn_xy, WIDTH - spwn_xy),  # x pos
                randint(spwn_xy, HEIGHT - spwn_xy), # y pos
                randint(5, max_ball_rad),   # radius
                uniform(-0.7, 0.7),         # x vel
                uniform(-0.7, 0.7),         # y vel
                C_BLACK                     # color
            )
        )

    while run:
        SCREEN.fill(C_WHITE)

        if len(balls) == 1:
            SCREEN.fill(C_BLACK)
            CLOCK.tick(1)
        else:
            CLOCK.tick(480)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        obstacle.draw()
       
        for ball in balls:        
            if ball.rad <= 1 or (ball.x_pos and ball.y_pos <= 0) or (ball.x_pos and ball.y_pos >= 700):
                BALL_DISSAPEAR.play()
                balls.remove(ball)
                print(ball, "got eaten!")
                print("Balls remaining: ", len(balls))

            ball.update_position(obs_x, obs_y, obs_rad, max_ball_rad)
            ball.draw()

            ball_rad_txt = font_style.render((f"{len(balls)}"), False, C_BLACK)
            SCREEN.blit(ball_rad_txt, ((WIDTH / 2), (HEIGHT / 2)))

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

                    b1.color, b2.color = C_RED, C_RED
                    b1.rad += (b1.rad - b2.rad) / 100 - 0.01
                    b2.rad += (b2.rad - b1.rad) / 100 - 0.01

        pygame.display.update()

    pygame.quit()

main()