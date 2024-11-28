import pygame
import time
import random
from PIL import Image  # For handling GIF frames

# access pygame
pygame.init()

# access font
pygame.font.init()

# import font
FONT = pygame.font.SysFont("comicsans", 30)

# Game window caption
pygame.display.set_caption("8-bit Game")

# Display Resolution
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set BG picture and Scale the image to match the background size
BG = pygame.transform.scale(pygame.image.load("./asset/Background/test background.jpg"), (WIDTH, HEIGHT))

# Set Player size
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_VEL = 5

# Sprite animation class
class SpriteSheet:
    def __init__(self, gif_path):
        # Load the GIF and extract frames
        gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                # Convert each frame to pygame surface
                frame = gif.convert('RGBA')
                pygame_image = pygame.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode)
                pygame_image = pygame.transform.scale(pygame_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.frames.append(pygame_image)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass  # End of frames
        
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 100  # Milliseconds between frames
        
        # Initialize the first frame for both directions
        self.frame_right = self.frames[0]
        self.frame_left = pygame.transform.flip(self.frames[0], True, False)

    def get_current_frame(self, facing_left):
        current_frame = self.frames[self.current_frame]
        if facing_left:
            return pygame.transform.flip(current_frame, True, False)
        return current_frame

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = current_time

# Initialize the player sprite
player_sprite = SpriteSheet("./asset/Character/Character Test.gif")

def backEnd(player, elapsed_time, facing_left):
    WIN.blit(BG, (0,0)) # Lock BG picture at coordinate top left

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,10))
    
    # Update animation and get current frame
    player_sprite.update()
    current_frame = player_sprite.get_current_frame(facing_left)
    WIN.blit(current_frame, (player.x, player.y))

    pygame.display.update()

def main():
    # Start
    run = True
    facing_left = True  # Initial direction

    # Time counting
    start_time = time.time()
    elapsed_time = 0

    # FPS
    clock = pygame.time.Clock()
    FPS = 60

    # Set where the player will be
    player = pygame.Rect((WIDTH / 2) - (PLAYER_WIDTH / 2), HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    while run:
        clock.tick(FPS) # FPS set is 60
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
            facing_left = False
        
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
            facing_left = True

        elif keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        elif keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL

        backEnd(player, elapsed_time, facing_left)
    
    pygame.quit()

if __name__ == "__main__":
    main()