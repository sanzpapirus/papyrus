import pygame, math

# 1. 게임 초기화
pygame.init()
# 2. 게임창 옵션 설정
size =[500,900]
screen = pygame.display.set_mode(size)
title = "HANGMAN"
pygame.display.set_caption(title)
# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
hint_font=pygame.font.Font("C:\Windows\Fonts\ARLRDBD.TTF", 50)
entry_font=pygame.font.Font("C:\Windows\Fonts\ARLRDBD.TTF", 50)




def tup_r(tup):
    temp_list=[]
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)
try_num=0
drop=False
exit = False
k=0
entry_text=" "
# 4. 메인 이벤트
while not exit:
# 4-1. FPS 설정
    clock.tick(60)
# 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            key_name=pygame.key.name(event.key)
            entry_text=key_name
# 4-3. 입력, 시간에 따른 변화
    k=k+1
# 4-4. 그리기
    screen.fill(black)
    r_head=round(size[0]/12)
    I_arm=r_head*2
    L_leg=round(I_arm*1.5)
    A=tup_r((0,size[1]*2/3))
    B=(size[0],A[1])
    C=tup_r((size[0]/6,A[1]))
    D=(C[0],C[0])
    E=tup_r((size[0]/2,D[1]))
    F=tup_r((E[0],E[1]+size[0]/6))
    if drop == False:
        pygame.draw.line(screen, white, E, F, 3)
    if drop == True:
        G=(F[0],F[1]+r_head+k*5)
    else:
        G=(F[0],F[1]+r_head)
    H=(G[0],G[1]+r_head)
    I=(G[0],H[1]+r_head)
    J=(I[0]-I_arm*math.cos(30*math.pi/180),
       I[1]+I_arm*math.sin(30*math.pi/180))
    J=tup_r(J)
    K=(I[0]+I_arm*math.cos(30*math.pi/180),J[1])
    L=(I[0],I[1]+I_arm)
    M=(L[0]-L_leg*math.cos(60*math.pi/180),L[1]+L_leg*math.sin(60*math.pi/180))
    N=(L[0]+L_leg*math.cos(60*math.pi/180),M[1])
    M=tup_r(M)
    N=tup_r(N)

    pygame.draw.line(screen, white, A, B, 3)
    pygame.draw.line(screen, white, C, D, 3)
    pygame.draw.line(screen, white, D, E, 3)
    pygame.draw.circle(screen, white, G, r_head, 3)
    pygame.draw.line(screen, white, H, I, 3)
    pygame.draw.line(screen, white, I, J, 3)
    pygame.draw.line(screen, white, I, K, 3)
    pygame.draw.line(screen, white, I, L, 3)
    pygame.draw.line(screen, white, L, M, 3)
    pygame.draw.line(screen, white, L, N, 3)
    if drop == False and try_num == 8:
        O=tup_r((size[0]/2-size[0]/6,F[1]))
        P=tup_r((O[0]+k*2,O[1]))
        if P[0]>size[0]/2+size[0]/6:
            P=tup_r((size[0]/2+size[0]/6, O[1]))
            drop = True
            k=0
        pygame.draw.line(screen, red, O, P, 3)
    # 힌트 표시
    word_show="_ _ _ _"
    hint=hint_font.render(word_show, True, white)
    hint_size=hint.get_size()
    hint_pos=tup_r((size[0]/2 - hint_size[0]/2, size[1]*5/6-hint_size[1]/2))
    screen.blit(hint, hint_pos)
    #입력창 표시
    entry = entry_font.render(entry_text, True, black)
    entry_size = entry.get_size()
    entry_pos= tup_r((size[0]/2-entry_size[0]/2, size[1]*17/18-entry_size[1]/2))
    entry_big_size=80
    pygame.draw.rect(screen, white, (size[0]/2-entry_big_size/2, size[1]*17.2/18-entry_big_size/2, entry_big_size, entry_big_size))
    screen.blit(entry, entry_pos)
# 4-5. 업데이트
    pygame.display.flip()
# 5. 게임종료
pygame.quit()