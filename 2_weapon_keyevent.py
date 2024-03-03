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
character_speed = 4

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []
weapon_speed = 8

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
  
  character_x_pos += character_to_left + character_to_right

  if character_x_pos < 0:
    character_x_pos = 0
  elif character_x_pos > screen_width - character_width:
    character_x_pos = screen_width - character_width

  # 무기 위치 조정
  weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
  
  # 천장에 닿은 무기 없애기
  weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

  # 배경 그리기
  screen.blit(background, (0, 0))
  for weapon_x_pos, weapon_y_pos in weapons:
    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
  screen.blit(stage, (0, screen_height - stage_height))
  screen.blit(character, (character_x_pos, character_y_pos))
  
  pygame.display.update() # 게임화면을 프레임마다 다시 그리기

pygame.time.delay(500)
# 게임 종료시 pygame 종료
pygame.quit()