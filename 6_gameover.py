import pygame
import random
import os
####################################################################
pygame.init()

#화면크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Balloon Pang")

# FPS 설정
clock = pygame.time.Clock()

#####################################################################

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) 
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 불러오기 
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # 이미지의 크기
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

character_to_left = 0
character_to_right = 0
character_speed = 0.3

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []
weapon_speed = 0.6

# 공 만들기
ball_images = [
  pygame.image.load(os.path.join(image_path, "balloon1.png")),
  pygame.image.load(os.path.join(image_path, "balloon2.png")),
  pygame.image.load(os.path.join(image_path, "balloon3.png")),
  pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

ball_speed_y = [-18, -15, -12, -9]

balls = []

# 최초로 생기는 공
balls.append({
  "pos_x" : 50,
  "pos_y" : 50,
  "img_idx" :0,
  "to_x" : 3,
  "to_y" : -6 ,
  "init_spd_y" : ball_speed_y[0] # y 최초 속도
})

# 사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# FONT 정의
game_font = pygame.font.Font(None, 40)
finish_font = pygame.font.Font(None, 80)
total_time = 40
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"




# 이벤트 루프
running = True # 게임 진행 중인지 여부
while running:
  dt = clock.tick(60)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        character_to_left -= character_speed
      if event.key == pygame.K_RIGHT:
        character_to_right += character_speed
      if event.key == pygame.K_SPACE:
        weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
        weapon_y_pos = character_y_pos
        weapons.append([weapon_x_pos, weapon_y_pos])


    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        character_to_left = 0
      elif event.key == pygame.K_RIGHT:
        character_to_right = 0
  
  character_x_pos += (character_to_left + character_to_right)*dt

  if character_x_pos < 0:
    character_x_pos = 0
  elif character_x_pos > screen_width - character_width:
    character_x_pos = screen_width - character_width

  # 무기 위치 조정
  weapons = [ [w[0], w[1] - weapon_speed*dt] for w in weapons]
  
  # 천장에 닿은 무기 없애기
  weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

  # 공 위치 정의
  for ball_idx, ball_val in enumerate(balls):
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_idx = ball_val["img_idx"]

    ball_size = ball_images[ball_img_idx].get_rect().size
    ball_width = ball_size[0]
    ball_height = ball_size[1]
    
    # 가로 벽에 닿았을 때 공 이동 방향 변경
    if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
      ball_val["to_x"] = ball_val["to_x"] * (-1)
    
    # 세로 벽에 닿았을 때 공 이동 방향 변경
    # 스테이지에 닿았을 때
    if ball_pos_y > screen_height - stage_height - ball_height:
      ball_val["to_y"] = ball_val["init_spd_y"]
    else: # 그 외의 모든 경우 속도를 변경
      ball_val["to_y"] += 0.3

    ball_val["pos_x"] += ball_val["to_x"]
    ball_val["pos_y"] += ball_val["to_y"]


  # 충돌 처리

  # 캐릭터 rect 정보 업데이트
  character_rect = character.get_rect()
  character_rect.left = character_x_pos
  character_rect.top = character_y_pos

  for ball_idx, ball_val in enumerate(balls):
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_idx = ball_val["img_idx"]

    # 공 rect 정보 업데이트
    ball_rect = ball_images[ball_img_idx].get_rect()
    ball_rect.left = ball_pos_x
    ball_rect.top = ball_pos_y

    # 공과 캐릭터 충돌 처리
    if character_rect.colliderect(ball_rect):
      game_result = "Game Over"
      running = False
      break

    # 공과 무기 충돌 처리
    for weapon_idx, weapon_val in enumerate(weapons):
      weapon_pos_x = weapon_val[0]
      weapon_pos_y = weapon_val[1]

      # 무기 rect 업데이트
      weapon_rect = weapon.get_rect()
      weapon_rect.left = weapon_pos_x
      weapon_rect.top = weapon_pos_y

      if weapon_rect.colliderect(ball_rect):
        weapon_to_remove = weapon_idx
        ball_to_remove = ball_idx

        if ball_img_idx < 3:
          # 현재 공 크기 정보
          ball_width = ball_rect.size[0]
          ball_height = ball_rect.size[1]

          small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
          small_ball_width = small_ball_rect.size[0]
          small_ball_height = small_ball_rect.size[1]

          # 왼쪽으로 튕겨나가는 작은 공
          balls.append({
            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
            "pos_y" : ball_pos_y + (ball_height /2 ) - (small_ball_height / 2),
            "img_idx" : ball_img_idx + 1,
            "to_x" : -3,
            "to_y" : -6,
            "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
          })

          # 오른쪽으로 튕겨나가는 작은 공
          balls.append({
            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
            "pos_y" : ball_pos_y + (ball_height /2 ) - (small_ball_height / 2),
            "img_idx" : ball_img_idx + 1,
            "to_x" : 3,
            "to_y" : -6,
            "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
          })
        break



  # 닿은 공과 무기 없애기
  if ball_to_remove > -1:
    del balls[ball_to_remove]
    ball_to_remove = -1

  if weapon_to_remove > -1:
    del weapons[weapon_to_remove]
    weapon_to_remove = -1

  if len(balls) == 0:
    game_result = "Mission Complete!"
    running = False

  # 배경 그리기
  screen.blit(background, (0, 0))

  for weapon_x_pos, weapon_y_pos in weapons:
    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
  
  for idx, val in enumerate(balls):
    ball_pos_x = val["pos_x"]
    ball_pos_y = val["pos_y"]
    ball_img_idx = val["img_idx"]
    screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
  screen.blit(stage, (0, screen_height - stage_height))
  screen.blit(character, (character_x_pos, character_y_pos))
  

  elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
  timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
  screen.blit(timer, (10, 10))

  if total_time - elapsed_time <= 0:
    game_result = "Time Over"
    running = False
  
  pygame.display.update() # 게임화면을 프레임마다 다시 그리기

msg_bg = pygame.image.load(os.path.join(image_path, "finish_background.png"))
msg = finish_font.render(game_result, True, (255, 255, 255))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg_bg, (0, 0))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)
# 게임 종료시 pygame 종료
pygame.quit()