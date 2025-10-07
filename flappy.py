import pygame, random, time
from pygame.locals import *

# VARIABLES (feel free to adjust)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10  # Bird's flap speed
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT= 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
        ]
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed # Update height

    def bump(self):
        self.speed = -SPEED

    def reset(self):
        self.rect.x = SCREEN_WIDTH / 6
        self.rect.y = SCREEN_HEIGHT / 2
        self.speed = 0

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.passed = False

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = - (self.rect.height - ysize)
        else:
            self.rect.y = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect.x -= GAME_SPEED

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird AI')
        self.BACKGROUND = pygame.transform.scale(
            pygame.image.load('assets/sprites/background-day.png'),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.reset()

    def _create_sprites(self):
        self.bird_group = pygame.sprite.Group()
        self.bird = Bird()
        self.bird_group.add(self.bird)

        self.ground_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i)
            self.ground_group.add(ground)

        self.pipe_group = pygame.sprite.Group()
        for i in range(2):
            pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
            self.pipe_group.add(pipes[0])
            self.pipe_group.add(pipes[1])
            
    def reset(self):
        self._create_sprites()
        self.score = 0
        self.game_over = False

    def step(self, action):
        # Handle AI action
        if action == 1: # 1 means "flap"
            self.bird.bump()

        # Update sprites
        self.bird_group.update()
        self.ground_group.update()
        self.pipe_group.update()
        
        # --- Update world ---
        # Check if ground is off screen
        if self.ground_group.sprites()[0].rect.right < 0:
            self.ground_group.remove(self.ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            self.ground_group.add(new_ground)

        # Check if pipes are off screen
        if self.pipe_group.sprites()[0].rect.right < 0:
            self.pipe_group.remove(self.pipe_group.sprites()[0])
            self.pipe_group.remove(self.pipe_group.sprites()[0])
            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            self.pipe_group.add(pipes[0])
            self.pipe_group.add(pipes[1])

        # Check for collisions
        if (pygame.sprite.groupcollide(self.bird_group, self.ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False, pygame.sprite.collide_mask)):
            self.game_over = True
            
        # Update score
        self.update_score()
    
    def update_score(self):
        first_pipe_pair = self.pipe_group.sprites()[0:2]
        # We check the pipe that is on the bottom
        bottom_pipe = first_pipe_pair[0] if first_pipe_pair[0].rect.top > 0 else first_pipe_pair[1]
        
        if not bottom_pipe.passed and bottom_pipe.rect.centerx < self.bird.rect.centerx:
            self.score += 1
            bottom_pipe.passed = True
            # Mark the top pipe as passed too so we don't double count
            top_pipe = first_pipe_pair[1] if first_pipe_pair[1].rect.bottom < SCREEN_HEIGHT else first_pipe_pair[0]
            top_pipe.passed = True


    def render(self):
        self.screen.blit(self.BACKGROUND, (0, 0))
        self.bird_group.draw(self.screen)
        self.pipe_group.draw(self.screen)
        self.ground_group.draw(self.screen)
        
        score_text = pygame.font.Font(None, 50).render(f"{self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        pygame.display.update()
        self.clock.tick(30) # Control frame rate

if __name__ == '__main__':
    game = FlappyBirdGame()
    
    while not game.game_over:
        action = 0 # Default action is "do nothing"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    action = 1 # "flap"

        game.step(action)
        game.render()

    print("Game Over! Your Score:", game.score)
    pygame.quit()