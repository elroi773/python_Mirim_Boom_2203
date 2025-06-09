# pip install pygame
import pygame
import random
import time
import os

# 1. 초기화
pygame.init()

# 2. 게임 화면 설정
size = [400, 900]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pygameEX")

# 3. 게임 설정 변수
clock = pygame.time.Clock()
black_color = (0, 0, 0)
img_path = r"./img/game_background_img.png"

class Img_Object:
    def __init__(self):
        self.x = 0
        self.y = 0

    def add_img(self, address):
        if not os.path.exists(address):
            raise FileNotFoundError(f"[경고] 이미지 파일을 찾을 수 없습니다: {address}")
        if address.lower().endswith(".png"):
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address).convert()

    def change_size(self, width, height):
        self.img = pygame.transform.scale(self.img, (width, height))
        self.width, self.height = self.img.get_size()

    def show_img(self):
        screen.blit(self.img, (self.x, self.y))

# 배경 이미지 설정
background = Img_Object()
try:
    background.add_img(img_path)
    background.change_size(*size)  # 화면 크기에 맞게 조절
except Exception as e:
    print(f"[ERROR] 배경 이미지 오류: {e}")
    pygame.quit()
    exit()


# 주인공 초기화
hero = Img_Object()
try:
    hero.add_img(f"./img/hero.png")
    hero.change_size(130, 180)

except Exception as e:
    print(f"[ERROR] hero 이미지 오류: {e}")
    pygame.quit()
    exit()

hero.x = round(size[0] / 2) - round(hero.width / 2)
hero.y = size[1] - hero.height - 100
hero.move = 5
k = 0

# 입력 상태
left_move = False
right_move = False
space_on = False

# 객체 리스트
missile_list = []
enemy_list = []

# 게임 루프
system_exit = 0
while system_exit == 0:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            system_exit = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_move = True
            elif event.key == pygame.K_RIGHT:
                right_move = True
            elif event.key == pygame.K_SPACE:
                space_on = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_move = False
            elif event.key == pygame.K_RIGHT:
                right_move = False
            elif event.key == pygame.K_SPACE:
                space_on = False

    # 움직임 처리
    if left_move:
        hero.x -= hero.move
        if hero.x <= 0:
            hero.x = 0
    if right_move:
        hero.x += hero.move
        if hero.x >= size[0] - hero.width:
            hero.x = size[0] - hero.width

    # 미사일 발사
    if space_on and k % 6 == 0:
        missile = Img_Object()
        try:
            missile.add_img(f"./img/missile.png")
            missile.change_size(25, 40)
        except Exception as e:
            print(f"[ERROR] missile 이미지 오류: {e}")
            continue
        missile.x = hero.x + hero.width / 2 - missile.width / 2
        missile.y = hero.y - missile.height - 10
        missile.move = 8
        missile_list.append(missile)
    k += 1

    # 미사일 이동 및 제거
    new_missile_list = []
    for m in missile_list:
        m.y -= m.move
        if m.y > -m.height:
            new_missile_list.append(m)
    missile_list = new_missile_list

    # 적기 생성
    if random.random() >= 0.98:
        enemy = Img_Object()
        try:
            enemy.add_img(f"./img/enemy.png")
            enemy.change_size(35, 35)
        except Exception as e:
            print(f"[ERROR] enemy 이미지 오류: {e}")
            continue
        enemy.x = random.randrange(round(hero.width / 2), size[0] - enemy.width - round(hero.width / 2))
        enemy.y = 15
        enemy.move = 3
        enemy_list.append(enemy)

    # 적기 이동 및 제거
    new_enemy_list = []
    for e in enemy_list:
        e.y += e.move
        if e.y <= size[1]:
            new_enemy_list.append(e)
    enemy_list = new_enemy_list

    # 미사일과 적기 충돌 검사
    crash_m_list = []
    crash_e_list = []
    for m in missile_list:
        for e in enemy_list:
            if (m.x - e.width <= e.x <= m.x + m.width) and (m.y - e.height <= e.y <= m.y + m.height):
                crash_m_list.append(m)
                crash_e_list.append(e)

    for m in crash_m_list:
        if m in missile_list:
            missile_list.remove(m)
    for e in crash_e_list:
        if e in enemy_list:
            enemy_list.remove(e)

    # 주인공과 적기 충돌
    crash_hero_enemy_list = []
    for e in enemy_list:
        if (hero.x - e.width <= e.x <= hero.x + hero.width) and (hero.y - e.height <= e.y <= hero.y + hero.height):
            crash_hero_enemy_list.append(e)

    for e in crash_hero_enemy_list:
        if e in enemy_list:
            enemy_list.remove(e)
            print("주인공과 충돌한 적기 제거")

    if crash_hero_enemy_list:
        print("게임 오버: 주인공과 적기 충돌")
        time.sleep(3)
        system_exit = 1

    # 화면 그리기
    background.show_img()

    hero.show_img()
    for m in missile_list:
        m.show_img()
    for e in enemy_list:
        e.show_img()
    pygame.display.flip()

# 게임 종료
pygame.quit()
