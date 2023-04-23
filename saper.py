import pygame,sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
RED = (255, 0, 0)

WINDOW_SIZE = (400, 400)
TILE_SIZE = 20
ROWS = 20
COLS = 20
NUM_MINES = 40

pygame.init()

pygame.mixer.init()
mine_sound = pygame.mixer.Sound("mine_explosion.mp3")
click = pygame.mixer.Sound("click.mp3")
start = pygame.mixer.Sound("start.mp3")
win = pygame.mixer.Sound("win.mp3")

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Minesweeper")

font = pygame.font.SysFont("Calibri", 20)
font_small = pygame.font.SysFont("Calibri",14)

board = [[0 for j in range(COLS)] for i in range(ROWS)]

mines = random.sample(range(ROWS*COLS), NUM_MINES)
for m in mines:
    row = m // COLS
    col = m % COLS
    board[row][col] = -1


for i in range(ROWS):
    for j in range(COLS):
        if board[i][j] != -1:
            count = 0
            for ii in range(max(0, i-1), min(ROWS, i+2)):
                for jj in range(max(0, j-1), min(COLS, j+2)):
                    if board[ii][jj] == -1:
                        count += 1
            board[i][j] = count


revealed = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        row.append(False)
    revealed.append(row)

lives = 3
lives_pos = (10, 10)
score = 0
score_pos = (WINDOW_SIZE[0]-120, 10)

game_over = False

lives_surface = font.render("Lives: " + str(lives), True, BLACK)
score_surface = font.render("Score: " + str(score), True, BLACK)

start.play();
while not game_over:
   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            i = pos[1] // TILE_SIZE
            j = pos[0] // TILE_SIZE
            if not revealed[i][j]:
                revealed[i][j] = True

                if board[i][j] == -1:
                    lives -= 1
                    mine_sound.play()
                    if lives == 0:
                        game_over = True
                    else:
                        game_over=False;
                 
                        pygame.draw.rect(screen, BLACK, (lives_pos[0], lives_pos[1], lives_surface.get_width(), lives_surface.get_height()))
                        lives_surface = font.render("Lives: " + str(lives), True, WHITE)
                  
                elif board[i][j] == 0:
                    for ii in range(max(0, i-1), min(ROWS, i+2)):
                        for jj in range(max(0, j-1), min(COLS, j+2)):
                            if not revealed[ii][jj]:
                                revealed[ii][jj] = True
                    click.play();
                    pygame.draw.rect(screen, BLACK, (score_pos[0], score_pos[1], score_surface.get_width(), score_surface.get_height()))
                    score += 10

                else:
                    text = font.render(str(board[i][j]), True, BLACK)
                    screen.blit(text, (j*TILE_SIZE+4, i*TILE_SIZE+4))
                    click.play();
                    pygame.draw.rect(screen, BLACK, (score_pos[0], score_pos[1], score_surface.get_width(), score_surface.get_height()))
                    score += 10


    all_revealed = True
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] != -1 and not revealed[i][j]:
                all_revealed = False
                break
        if not all_revealed:
            break
                    


 
    for i in range(ROWS):
        for j in range(COLS):
            if revealed[i][j]:
                if board[i][j] == -1:
                    pygame.draw.rect(screen, RED, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, GREY, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    if board[i][j] > 0:
                        text = font.render(str(board[i][j]), True, BLACK)
                        screen.blit(text, (j*TILE_SIZE+4, i*TILE_SIZE+4))
                    else:
                        pygame.draw.rect(screen, GREY, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
  
    if all_revealed:
        win.play();
        win_text = font.render("You win!", True, WHITE)
        win_rect = win_text.get_rect(center=screen.get_rect().center)
        screen.fill(BLACK)
        screen.blit(win_text, win_rect)
        game_over=True;
    score_surface = font.render("Scores: " + str(score), True, WHITE)
    lives_surface = font.render("Lives: " + str(lives), True, RED)
    screen.blit(lives_surface, lives_pos)
    screen.blit(score_surface,score_pos)
    pygame.display.flip()


score_text = font_small.render("Final score: " + str(score), True, RED)
score_rect = score_text.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery+30))
game_over_text = font.render("Game over!", True, RED)
game_over_rect = game_over_text.get_rect(center=screen.get_rect().center)
screen.fill(WHITE)
screen.blit(game_over_text, game_over_rect)
screen.blit(score_text, score_rect)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
