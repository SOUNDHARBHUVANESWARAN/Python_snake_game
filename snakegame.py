import pygame as pg
import cv2
from random import randrange

# Initialize Pygame
pg.init()

# Constants
WINDOW = 800
TILE_SIZE = 30
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
FONT = pg.font.Font(None, 74)
BUTTON_FONT = pg.font.Font(None, 50)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)

# Functions
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def display_score(score):
    score_text = FONT.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (WINDOW // 2 - score_text.get_width() // 2, WINDOW // 2 - score_text.get_height() // 2 - 50))

def display_ok_button():
    button_text = BUTTON_FONT.render('OK', True, (0, 0, 0))
    button_rect = pg.Rect(WINDOW // 2 - 50, WINDOW // 2 + 50, 100, 50)
    pg.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, (button_rect.x + 25, button_rect.y + 10))
    return button_rect

# Game variables
snake = pg.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
score = 0
game_over = False

# Main game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN and not game_over:
            if event.key == pg.K_w:
                snake_dir = (0, -TILE_SIZE)
            if event.key == pg.K_s:
                snake_dir = (0, TILE_SIZE)
            if event.key == pg.K_a:
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_d:
                snake_dir = (TILE_SIZE, 0)
        if event.type == pg.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if ok_button.collidepoint(mouse_pos):
                play_video(r"C:\Users\priya\Desktop\soundhar\snake game\video1\video11.mp4")
                exit()

    screen.fill('black')

    if not game_over:
        # Check borders and self eating
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            game_over = True

        # Check food
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            score += 1

        # Draw food
        pg.draw.rect(screen, 'red', food)

        # Draw snake
        [pg.draw.rect(screen, 'green', segment) for segment in segments]

        # Move snake
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]
    else:
        display_score(score)
        ok_button = display_ok_button()

    pg.display.flip()
    clock.tick(60)