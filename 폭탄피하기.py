import pygame
import random

# pygame 라이브러리를 불러옵니다.
pygame.init()

# 화면 너비와 높이를 설정합니다.
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 900

# 화면을 생성합니다.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 화면 갱신을 조절하기 위한 시계를 생성합니다.
clock = pygame.time.Clock()

# 키 입력 반복 간격을 설정합니다.
pygame.key.set_repeat(1, 1)

# 색깔을 정의합니다.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# 사용할 폰트를 설정합니다.
large_font = pygame.font.SysFont('malgungothic', 72)
small_font = pygame.font.SysFont('malgungothic', 36)

# 점수와 게임 종료 여부를 초기화합니다.
score = 0
game_over = False
# 폭탄과 캐릭터 이미지를 불러옵니다.
bomb_image = pygame.image.load('bomb.png')
man_image = pygame.image.load('man.png')
# 방어막 아이템 이미지를 불러옵니다.
shield_image = pygame.image.load('shield.png')

# 사운드를 초기화합니다.
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
game_over_sound = pygame.mixer.Sound('game_over.wav')
boom_sound = pygame.mixer.Sound('boom.mp3')

# 게임을 시작하는 함수를 정의합니다.
def start_game():
    global score, game_over, man, bombs, shield_active, shield_count, game_start_time, last_shield_given
    score = 0
    game_over = False
    # 게임 시작 시간을 기록합니다.
    game_start_time = pygame.time.get_ticks()
    # 캐릭터의 초기 위치를 설정합니다.
    man = man_image.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT)
    bombs = []
    shield_active = False  # 방어막 아이템 활성화 여부를 초기화합니다.
    shield_count = 0  # 방어막 개수를 초기화합니다.
    # 초기에 폭탄들을 생성합니다.
    for i in range(18):
        # 폭탄의 초기 위치를 랜덤으로 설정합니다.
        bomb = bomb_image.get_rect(left=random.randint(0, 900 - bomb_image.get_width()), top=-100)
        # 폭탄의 초기 속도를 점수에 따라 설정합니다.
        min_speed = 6 + (score * 0.5)  # 최저속도
        max_speed = 22 + (score * 0.5)  # 최고속도
        dy = random.randint(min_speed, max_speed)
        bombs.append((bomb, dy))
    # 배경 음악을 재생합니다.
    pygame.mixer.music.play(-1)
    # 마지막으로 방어막 아이템을 주었던 시간을 초기화합니다.
    last_shield_given = pygame.time.get_ticks()

# 난이도를 증가시키는 함수를 정의합니다.
def increase_difficulty():
    global bombs
    for _, dy in bombs:
        # 난이도를 증가시킬 때마다 폭탄들의 속도를 업데이트합니다.
        min_speed = 6 + (score * 0.5)  # 최저속도
        max_speed = 22 + (score * 0.5)  # 최고속도
        dy += random.randrange(2, 8)
        # 속도가 최대 속도를 넘지 않도록 제한합니다.
        dy = min(dy, max_speed)
        bombs.append((bomb, dy))
# 방어막 아이템을 활성화하는 함수를 정의합니다.
def activate_shield():
    global shield_active, shield_count
    shield_active = True
    shield_count -= 1  # 방어막 아이템을 사용하면 방어막 개수를 1개 줄입니다.

# 방어막 아이템을 주는 함수를 정의합니다.
def give_shield():
    global shield_count, last_shield_given
    # 게임이 종료되지 않은 경우에만 방어막을 주도록 합니다.
    if not game_over:
        shield_count += 1
        last_shield_given = pygame.time.get_ticks()  # 방어막 아이템을 주었던 시간을 갱신합니다.

# 게임을 시작합니다.
start_game()

# 마지막으로 난이도가 증가한 시간을 저장합니다.
last_difficulty_increase = pygame.time.get_ticks()
# 마지막으로 방어막 아이템이 사용된 시간을 저장합니다.
last_shield_activation = pygame.time.get_ticks()
# 마지막으로 방어막 아이템을 주는 시간을 저장합니다.
last_shield_given = pygame.time.get_ticks()

# 게임 루프를 시작합니다.
while True:
    # 화면을 검은색으로 채웁니다.
    screen.fill(BLACK)

    # 이벤트를 처리합니다.
    for event in pygame.event.get():
        # 종료 이벤트가 발생하면 pygame을 종료합니다.   
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 키 이벤트를 처리합니다.
        if event.type == pygame.KEYDOWN:
            # 게임 오버 상태에서 Ctrl 키를 누르면 게임을 재시작합니다.
            if event.key == pygame.K_SPACE and game_over:
                start_game()
            # 게임이 진행 중일 때, 왼쪽 또는 오른쪽 화살표 키를 누르면 캐릭터를 이동시킵니다.
            if not game_over:
                if event.key == pygame.K_LEFT:
                    man.left -= 1
                elif event.key == pygame.K_RIGHT:
                    man.right += 1
                # Ctrl 키를 누르면 방어막 아이템을 사용합니다.
                elif event.key == pygame.K_LCTRL and shield_count > 0 and not shield_active:
                    activate_shield()
                    last_shield_activation = pygame.time.get_ticks()  # 방어막 아이템 사용 시간을 갱신합니다.

    # 게임이 종료되지 않았을 때 게임을 진행합니다.
    if not game_over:
        # 폭탄들을 이동시키고 화면에서 벗어난 폭탄들을 제거합니다.
        for bomb, dy in bombs:
            bomb.top += dy
            if bomb.top > SCREEN_HEIGHT:
                bombs.remove((bomb, dy))
                # 새로운 폭탄을 생성하고 리스트에 추가합니다.
                bomb = bomb_image.get_rect(left=random.randint(0, SCREEN_WIDTH), top=-100)
                dy = random.randint(12, 16)
                bombs.append((bomb, dy))
                score += 1

        # 캐릭터가 화면을 벗어나지 않도록 제한합니다.
        if man.left < 0:
            man.left = 0
        elif man.right > SCREEN_WIDTH:
            man.right = SCREEN_WIDTH

            # 폭탄과 캐릭터가 충돌했는지 확인합니다.
    for bomb, _ in bombs:
        if bomb.colliderect(man) and not shield_active:  # 방어막 아이템이 활성화되지 않았을 때만 충돌을 확인합니다.
            # 충돌하면 게임 오버 상태로 전환하고 사운드를 재생합니다.
            game_over = True
            pygame.mixer.music.stop()
            game_over_sound.play()
            boom_sound.play()
        # 방어막과 폭탄이 충돌했는지 확인합니다.
        elif bomb.colliderect(man) and shield_active:
            bombs.remove((bomb, _))  # 충돌한 폭탄을 제거합니다.
            shield_active = False  # 방어막을 비활성화합니다.

        # 방어막 아이템의 지속 시간을 확인하여 비활성화합니다.
        if shield_active and pygame.time.get_ticks() - last_shield_activation >= 2000:
            shield_active = False

        # 게임이 종료되지 않은 경우에만 방어막을 주도록 합니다.
        if not game_over:
            # 게임 시작 시간을 기준으로 15초가 지났을 때 방어막 개수를 증가시킵니다.
            if pygame.time.get_ticks() - game_start_time >= 15000:
                give_shield()
                game_start_time = pygame.time.get_ticks()  # 게임 시작 시간을 다시 설정합니다.


        # 일정 시간이 지날 때마다 난이도를 증가시킵니다.
        current_time = pygame.time.get_ticks()
        if current_time - last_difficulty_increase >= 10000:
            increase_difficulty()
            last_difficulty_increase = current_time

    # 화면에 폭탄과 캐릭터를 그립니다.
    for bomb, dy in bombs:
        screen.blit(bomb_image, bomb)

    screen.blit(man_image, man)

    # 방어막 아이템이 활성화된 경우, 화면에 방어막 아이템을 그립니다.
    if shield_active:
        screen.blit(shield_image, (man.centerx - shield_image.get_width() // 2, man.centery - shield_image.get_height() // 2))

    # 점수와 방어막 개수를 화면 오른쪽 상단에 표시합니다.
    score_image = small_font.render('점수 {}'.format(score), True, YELLOW)
    screen.blit(score_image, (10, 10))
    shield_count_image = small_font.render('쉴드: {}'.format(shield_count), True, YELLOW)
    screen.blit(shield_count_image, (SCREEN_WIDTH - shield_count_image.get_width() - 10, 10))

    # 게임 오버 상태일 때, 게임 오버 메시지와 재시작 안내를 화면에 표시합니다.
    if game_over:
        game_over_image = large_font.render('게임 오버', True, RED)
        restart_image = small_font.render('SPACE 키를 눌러 게임을 재시작하세요', True, WHITE)
        screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2.3))
        screen.blit(restart_image, restart_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 1.5))

    # 화면을 업데이트하고 프레임 속도를 조절합니다.
    pygame.display.update()
    clock.tick(30)