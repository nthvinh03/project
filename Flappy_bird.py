import pygame,sys,random
pygame.init()


#Hàm tạo sàn 
def draw_floor():
    #sàn 1
    screen.blit(floor,(floor_x_pos,650))
    #sàn 2
    screen.blit(floor,(floor_x_pos+432,650))

#Hàm tạo ống    
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe.get_rect(midtop=(500,random_pipe_pos))
    top_pipe=pipe.get_rect(midtop=(500,random_pipe_pos-750))
    return bottom_pipe,top_pipe 
#Hàm di chuyển ống 
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes

def draw_pipe(pipes):
    for pipee in pipes:
        if pipee.bottom >=768:
            screen.blit(pipe,pipee)
        else :
            flip_pipe=pygame.transform.flip(pipe,False,True)
            screen.blit(flip_pipe,pipee)
#Hàm xử lý va chạm
def check_collision(pipes):
    for pipee in pipes: 
        if bird_rect.colliderect(pipee):
            return False
    if bird_rect.top<=-75 or bird_rect.bottom>=650:   
            return False
    return True 
def bird_rotate(bird1):
    new_bird1=pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird1
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect
#Hàm xử lí 
def display_score(game_state):
    if game_state =="main game":
        score_display=game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_display.get_rect(center=(216,100))
        screen.blit(score_display,score_rect)
    if game_state=="game over":
        score_display=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect=score_display.get_rect(center=(216,100))
        screen.blit(score_display,score_rect)

        hight_score_display=game_font.render(f'Hight Score: {int(hight_score)}',True,(255,255,255))
        hight_score_rect=score_display.get_rect(center=(170,630))
        screen.blit(hight_score_display,hight_score_rect)

def update_score(score,hight_score):
    if score > hight_score:
        hight_score=score
    return hight_score
#biến khởi tạo cửa sổ game
screen=pygame.display.set_mode((432,768))
#biến cài đặt fps
clock=pygame.time.Clock()
#biến chền hình nền 
bg=pygame.image.load("assets/background-night.png").convert()
#Gấp dôi hình nền 
bg=pygame.transform.scale2x(bg)
#biến chèn sàn
floor=pygame.image.load('assets/floor.png').convert()
#gấp đôi sàn
floor=pygame.transform.scale2x(floor)
#biến khỏi tạo vị trí sàn theo trục x
floor_x_pos=0
#biến khởi tạo trọng lực
gravity=0.25
#biến di chuyển của chim
bird_movement=0
#Khởi tạo vị trí ngẫu nhiên của ống 
pipe_height=[300,400,500]
#Biến dừng trò chơi 
game_active=True
#Biến cài đặt font chữ
game_font=pygame.font.Font('04B_19.ttf',30)
score=0
hight_score=0
#Man hinh ket thuc 
game_over_image=pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect=game_over_image.get_rect(center=(216,384))
#tạo chim
bird_down=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png')).convert_alpha()
bird_mid=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png')).convert_alpha()
bird_up=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png')).convert_alpha()

bird_list=[bird_down,bird_mid,bird_up]
bird_index=0
bird=bird_list[bird_index]
bird_rect=bird.get_rect(center=(100,384))
bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
#tạo ống 
pipe=pygame.image.load('assets/pipe-green.png').convert()
pipe=pygame.transform.scale2x(pipe)
pipe_list=[]

#tạo thời gian xuất hiện ống
time_pipe=pygame.USEREVENT
pygame.time.set_timer(time_pipe,1200)


while True:                               
    #lấy tất cả event trong pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement=-9
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,384)
                score=0
                bird_movement=0
        if event.type==time_pipe:
            pipe_list.extend(create_pipe())
        if event.type==bird_flap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,bird_rect =bird_animation()
                
    #thêm hình ảnh vào cửa sổ game
    screen.blit(bg,(0,0))
    if game_active:
        #chim
        bird_movement+=gravity
        bird_rotated=bird_rotate(bird)
        bird_rect.centery+=bird_movement
        screen.blit(bird_rotated,bird_rect)
         #Ống
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        game_active=check_collision(pipe_list)
        score+=0.01
        display_score("main game")
    else:
        screen.blit(game_over_image,game_over_rect)
        hight_score=update_score(score,hight_score)
        display_score("game over")
    
    floor_x_pos -=1
    #hàm chèn sàn
    draw_floor()
    #điều kiện để 2 sàn không tạo ra khoảng trống
    if floor_x_pos<=-432:
        floor_x_pos=0
    #hiển thị cửa sổ game
    pygame.display.update()
    #cài đặt fps
    clock.tick(80)