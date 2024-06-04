import pygame #파이 게임 모듈 임포트
import random

pygame.init() #파이 게임 초기화
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 
pygame.key.set_repeat(1, 1)

#변수

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE= (255, 255, 255)
more_large_font=pygame.font.SysFont('malgungothic', 100)
large_font = pygame.font.SysFont('malgungothic', 72)
small_font = pygame.font.SysFont('malgungothic', 36)
score = 0
game_over = False

bomb_image = pygame.image.load('bomb.png')
man_image = pygame.image.load('man.png')

pygame.mixer.init()
pygame.mixer.music.load('music.mp3') #배경 음악
game_over_sound = pygame.mixer.Sound('game_over.wav')
boom_sound=pygame.mixer.Sound('boom.mp3')

def start_game():
    global score, game_over, man, bombs
    score = 0
    game_over = False
    man = man_image.get_rect(centerx = SCREEN_WIDTH // 2, bottom = SCREEN_HEIGHT)
    bombs = []
    for i in range(8):
        bomb = bomb_image.get_rect(left=random.randint(0,800-bomb_image.get_width()), top=-100)
        dy = random.randint(10, 14)
        bombs.append((bomb, dy))
    pygame.mixer.music.play(-1)

start_game()

while True: #게임 루프
    screen.fill(BLACK) #단색으로 채워 화면 지우기

    #변수 업데이트

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # 게임 종료를 위해 pygame.quit() 호출
            exit()  # 프로그램 종료
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over: # 게임 오버 상태에서 스페이스바를 누르면 재시작
                start_game()
            if not game_over:  # 게임이 종료되지 않은 경우에만 키 입력 처리
                if event.key == pygame.K_LEFT:
                    man.left -= 1
                elif event.key == pygame.K_RIGHT: 
                    man.right += 1

    if not game_over:  
        for bomb, dy in bombs:
            bomb.top += dy
            if bomb.top > SCREEN_HEIGHT:
                bombs.remove((bomb, dy))
                bomb = bomb_image.get_rect(left=random.randint(0, SCREEN_WIDTH), top=-100)
                dy = random.randint(7, 11)
                bombs.append((bomb, dy))
                score += 1

        if man.left < 0:
            man.left = 0
        elif man.right > SCREEN_WIDTH:
            man.right = SCREEN_WIDTH

        for bomb, dy in bombs:
            if bomb.colliderect(man):
                game_over = True
                pygame.mixer.music.stop()
                game_over_sound.play()
                boom_sound.play()

    #화면 그리기

    for bomb, dy in bombs:
        screen.blit(bomb_image, bomb)

    screen.blit(man_image, man)

    score_image = small_font.render('점수 {}'.format(score), True, YELLOW)
    screen.blit(score_image, (10, 10))

    if game_over:
        game_over_image = more_large_font.render('GAME OVER', True, RED)
        restart_image = small_font.render('PRESS ENTER TO RESTART THE GAME', True, WHITE)
        screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
        screen.blit(restart_image, restart_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 1.5))

    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값


pygame.quit()
