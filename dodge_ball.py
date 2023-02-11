import pygame
import math
import random

# region init
pygame.init()
# endregion init

# region constants
# display constants
WIN_WIDTH = 800
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
FPS = 60
FONT = "Caveat-VariableFont_wght.ttf"

# color constants
BACKGROUND_COLOR = (254, 245, 239)
PLAYER_COLOR = (228, 187, 151)
SCORE_TEXT_COLOR  = (0, 0, 0)
# endregion constants

class Ball():
    def __init__(self, start_pos: tuple[int, int], mode: int, line_theta_raidians: float = 0, size:float = 20, speed:float = 10, color: tuple[int, int, int] = (0, 0, 0)):
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.mode = mode # 0:straight line
        self.line_theta_raidians = line_theta_raidians
        self.size = size
        self.speed = speed
        self.color = color
        if self.mode == 0:
            self.v_x = self.speed * math.cos(self.line_theta_raidians)
            self.v_y = self.speed * math.sin(self.line_theta_raidians)

    # return pos tuple
    def get_pos(self) -> tuple[int, int]:
        return (self.pos_x, self.pos_y)

    # draw ball
    def draw(self):
        pygame.draw.circle(WIN, self.color, self.get_pos(), self.size)

    # move ball
    def move(self):
        self.pos_x += self.v_x
        self.pos_y += self.v_y
        
        # bounce
        if self.pos_x <= self.size:
            self.v_x *= -1
        if self.pos_y <= self.size:
            self.v_y *= -1
        if self.pos_x >= WIN_WIDTH - self.size:
            self.v_x *= -1
        if self.pos_y >= WIN_HEIGHT - self.size:
            self.v_y *= -1

class Player():
    def __init__(self):
        self.size = (40, 40)
        self.speed = 5
        self.rect = pygame.Rect(WIN_WIDTH / 2 - self.size[0] / 2, WIN_HEIGHT / 2 - self.size[1] / 2, self.size[0], self.size[1])

    # draw player
    def darw(self):
        pygame.draw.rect(WIN, PLAYER_COLOR, self.rect)

    # move player
    def move(self, key_pressed):
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speed
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speed

        # clamp in window
        self.rect.x = min(max(self.rect.x, 0), WIN_WIDTH - self.size[0])
        self.rect.y = min(max(self.rect.y, 0), WIN_HEIGHT - self.size[1])

    # check collision with circle
    def collide_circle(self, center: tuple[int, int], radius: int) -> bool:
        if center[0] < self.rect.x + self.size[0] + radius and center[0] > self.rect.x - radius and center[1] < self.rect.y + self.size[1] + radius and center[1] > self.rect.y - radius:
            return True
        return False

class Game():
    def __init__(self, ball_num: int):
        self.ball_num = ball_num
        self.balls: list[Ball] = []
        for _ in range(ball_num):
            ball_size = random.randint(20, 30)
            ball_pos = (random.randint(ball_size, WIN_WIDTH - ball_size), random.randint(ball_size, WIN_HEIGHT - ball_size))
            ball_direction = random.random() * 2 * math.pi
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ball = Ball(ball_pos, 0, line_theta_raidians=ball_direction, size=ball_size, color=ball_color)
            self.balls.append(ball)
        self.player = Player()
        self.end = False
        self.score = 0
        self.font = pygame.font.Font(FONT, 36) 

    # update game
    def update(self, key_pressed):
        WIN.fill(BACKGROUND_COLOR)

        # upate player
        self.player.move(key_pressed)
        self.player.darw()

        # update balls
        for ball in self.balls:
            ball.move()
            ball.draw()
            if self.player.collide_circle(ball.get_pos(), ball.size):
                self.end = True

        # update score
        self.score += 5 / FPS
        WIN.blit(self.font.render(f"score: {int(self.score)}", True, SCORE_TEXT_COLOR), (10, 10))

        # update screen
        pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        state = "game"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if state == "game":
            game = Game(10)
            while not game.end:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.end = True
                        run = False
                
                key_pressed = pygame.key.get_pressed()
                game.update(key_pressed)

if __name__ == '__main__':
    main()