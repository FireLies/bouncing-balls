import pygame

# Color list
#---------------------------
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_RED = (255, 0, 0)
#---------------------------

pygame.init()

WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Bouncing Balls")

class Bounce:

    def __init__(self, x_pos, y_pos, radius, x_vel, y_vel, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color

        self.x_vel = x_vel
        self.y_vel = y_vel

        self.x_rate = 1
        self.y_rate = 1

        self.line_trail = []
        self.max_line_trail = 500

    def draw(self):
        if len(self.line_trail) > 1:
            pygame.draw.lines(SCREEN, C_RED, False, self.line_trail, 1)

        pygame.draw.circle(
            SCREEN,
            self.color,
            (self.x_pos, self.y_pos),
            self.radius
        )

    def update_position(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        if self.x_pos - self.radius <= 0 or self.x_pos - self.radius >= WIDTH:
            self.x_vel *= - self.x_rate

        if self.y_pos - self.radius <= 0 or self.y_pos - self.radius >= HEIGHT:
            self.y_vel *= - self.y_rate
        
        self.line_trail.append((self.x_pos, self.y_pos))
        if len(self.line_trail) > self.max_line_trail:
            self.line_trail.pop(0)
        

def main():
    run = True

    circles = [
        Bounce(WIDTH/5, HEIGHT/2, 16, 0.2, 0.3, C_BLACK),
        Bounce(WIDTH/8, HEIGHT/3, 12, 0.5, 0.1, C_BLACK),
        Bounce(WIDTH/2, HEIGHT/1, 10, 0.1, 0.5, C_BLACK),
        Bounce(WIDTH/3, HEIGHT/3, 17, 0.3, 0.5, C_BLACK),
        Bounce(WIDTH/3, HEIGHT/7, 7, 0.8, 0.2, C_BLACK)
    ]

    while run:

        SCREEN.fill(C_WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for c in circles:
            c.update_position()
            c.draw()

        pygame.display.update()
        CLOCK.tick(480)

    pygame.quit()

main()