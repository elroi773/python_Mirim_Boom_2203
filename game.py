import pygame
import random
import time
import os

# 초기화
pygame.init()

size = [500, 900]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pygameEX")

clock = pygame.time.Clock()
black_color = (0, 0, 0)
white_color = (255, 255, 255)
font = pygame.font.SysFont(None, 40)

img_path = r"./img/game_background.png"

class Img_Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.move = 0
        self.img_path = ""

    def add_img(self, address):
        if not os.path.exists(address):
            raise FileNotFoundError(f"[경고] 이미지 파일을 찾을 수 없습니다: {address}")
        if address.lower().endswith(".png"):
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address).convert()
        self.img_path = address

    def change_size(self, width, height):
        self.img = pygame.transform.scale(self.img, (width, height))
        self.width, self.height = self.img.get_size()

    def show_img(self):
        screen.blit(self.img, (self.x, self.y))

def draw_text(text, pos_x, pos_y, color=white_color):
    img = font.render(text, True, color)
    screen.blit(img, (pos_x, pos_y))

# 배경 이미지
background = Img_Object()
try:
    background.add_img(img_path)
    background.change_size(*size)
except Exception as e:
    print(f"[ERROR] 배경 이미지 오류: {e}")
    pygame.quit()
    exit()

# 시간표 이미지 추가 (왼쪽 고정)
timetable = Img_Object()
try:
    timetable.add_img("./img/timetable_php.png")  # 실제 시간표 이미지 파일명으로 수정 필요
    timetable.change_size(120, 600)
    timetable.x = 10
    timetable.y = 200
except Exception as e:
    print(f"[ERROR] 시간표 이미지 오류: {e}")
    pygame.quit()
    exit()

# 주인공 캐릭터
selected_hero_img = "hero.png"
hero = Img_Object()
try:
    hero.add_img(f"./img/{selected_hero_img}")
    hero.change_size(130, 180)
except Exception as e:
    print(f"[ERROR] hero 이미지 오류: {e}")
    pygame.quit()
    exit()

hero.x = round(size[0] / 2) - round(hero.width / 2)
hero.y = size[1] - hero.height - 160  # 캐릭터 위치를 더 위로
hero.move = 5

left_move = False
right_move = False
space_on = False

missile_list = []
enemy_list = []

score = 0
lives = 3

system_exit = 0
k = 0
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

    left_limit = 130
    right_limit = size[0] - hero.width

    # 움직임
    if left_move:
        hero.x -= hero.move
        if hero.x <= left_limit:
            hero.x = left_limit
    if right_move:
        hero.x += hero.move
        if hero.x >= right_limit:
            hero.x = right_limit

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

    new_missile_list = []
    for m in missile_list:
        m.y -= m.move
        if m.y > -m.height:
            new_missile_list.append(m)
    missile_list = new_missile_list



    if random.random() >= 0.98:
        obj = Img_Object()
        try:
            r = random.random()
            if r > 0.5:
                obj.add_img(f"./img/enemy.png")
            elif r > 0.2:
                obj.add_img(f"./img/java.png")
            obj.change_size(35, 35)
        except Exception as e:
            print(f"[ERROR] 적기 이미지 오류: {e}")
            continue

        left_margin = 130
        right_margin = size[0] - obj.width - 10
        obj.x = random.randint(left_margin, right_margin)
        obj.y = 15
        obj.move = 3
        enemy_list.append(obj)

    new_enemy_list = []
    for e in enemy_list:
        e.y += e.move
        if e.y <= size[1]:
            new_enemy_list.append(e)
    enemy_list = new_enemy_list


    crash_m_list = []
    crash_e_list = []

    bonus_point = 0
    for m in missile_list:
        for e in enemy_list:
            if (m.x - e.width <= e.x <= m.x + m.width) and (m.y - e.height <= e.y <= m.y + e.height):
                crash_m_list.append(m)
                crash_e_list.append(e)
                if "java.png" in e.img_path:
                    print(f"Java 맞음! 점수: {score}")
                    if score % 10 == 0 and score != 0:
                        bonus_point += 10
                        score += bonus_point
                if "java.png" in e.img_path:
                    score += 1

    for m in crash_m_list:
        if m in missile_list:
            missile_list.remove(m)
    for e in crash_e_list:
        if e in enemy_list:
            enemy_list.remove(e)

    for e in enemy_list[:]:
        if (hero.x - e.width <= e.x <= hero.x + hero.width) and (hero.y - e.height <= e.y <= hero.y + hero.height):
            if "enemy.png" in e.img_path:
                lives -= 1
                enemy_list.remove(e)
                if lives <= 0:
                    print(f"게임 오버: 주인공과 {e.img_path} 충돌")
                    time.sleep(3)
                    system_exit = 1
            elif "java.png" in e.img_path:
                score += 1
                enemy_list.remove(e)
                if score % 10 == 0:
                    bonus_point += 10
                    score += bonus_point

    # 화면 출력 순서 중요
    background.show_img()
    timetable.show_img()     # ← 추가: 왼쪽 시간표
    hero.show_img()
    for m in missile_list:
        m.show_img()
    for e in enemy_list:
        e.show_img()

    draw_text(f"Score: {score}", size[0] - 150, 10)
    draw_text(f"Lives: {lives}", size[0] - 150, 50)

    pygame.display.flip()

pygame.quit()
