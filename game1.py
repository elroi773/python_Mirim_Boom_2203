import pygame
import random
import time
import os

# 초기화
pygame.init()

size = [400, 900]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pygameEX")

clock = pygame.time.Clock()
black_color = (0, 0, 0)
white_color = (255, 255, 255)
font = pygame.font.SysFont(None, 40)  # 점수/목숨 표시 폰트

img_path = r"./img/game_background_img.png"

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

# 배경
background = Img_Object()
try:
    background.add_img(img_path)
    background.change_size(*size)
except Exception as e:
    print(f"[ERROR] 배경 이미지 오류: {e}")
    pygame.quit()
    exit()

selected_hero_img = "hero2.png"  # 실제 hero 이미지 파일명으로 변경
hero = Img_Object()
try:
    hero.add_img(f"./img/{selected_hero_img}")
    hero.change_size(130, 180)
except Exception as e:
    print(f"[ERROR] hero 이미지 오류: {e}")
    pygame.quit()
    exit()

hero.x = round(size[0] / 2) - round(hero.width / 2)
hero.y = size[1] - hero.height - 100
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

    # 적기 생성: enemy, java, js (js는 목숨 깎는 적)
    if random.random() >= 0.98:
        obj = Img_Object()
        try:
            r = random.random()
            if r > 0.5:
                obj.add_img(f"./img/enemy.png")  # enemy: 점수 +1
            elif r > 0.2:
                obj.add_img(f"./img/java.png")   # java: 점수 +1
            obj.change_size(35, 35)
        except Exception as e:
            print(f"[ERROR] 적기 이미지 오류: {e}")
            continue
        obj.x = random.randrange(round(hero.width / 2), size[0] - obj.width - round(hero.width / 2))
        obj.y = 15
        obj.move = 3
        enemy_list.append(obj)

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

    bonus_point = 0 

    for m in missile_list:
        for e in enemy_list:
            # 미사일과 적 충돌 범위 조건 (간단 충돌 감지)
            if (m.x - e.width <= e.x <= m.x + m.width) and (m.y - e.height <= e.y <= m.y + e.height):
                if "java.png" in e.img_path:
                    score += 1
                    crash_m_list.append(m)
                    crash_e_list.append(e)
                    print(f"Java 맞음! 점수: {score}")

                    if score % 10 == 0 and score != 0:
                        bonus_point += 10
                        print(f"보너스 점수! 현재 보너스: {bonus_point}")
                        score += bonus_point
                else:
                    # 다른 적(예: enemy.png 등)은 점수 오르지 않고 무시 (또는 제거만)
                    crash_m_list.append(m)
                    crash_e_list.append(e)


    for m in crash_m_list:
        if m in missile_list:
            missile_list.remove(m)
    for e in crash_e_list:
        if e in enemy_list:
            enemy_list.remove(e)

    # 주인공과 적기 충돌 검사 (java, enemy 모두 충돌 시 게임 오버)
    crash_hero_enemy_list = []
    for e in enemy_list:
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
                print(f"Java 충돌! 점수: {score}")
                enemy_list.remove(e)
                # 보너스 점수 처리
                if score % 10 == 0:
                    bonus_point += 10
                    score += bonus_point
                    print(f"보너스 점수! 현재 보너스: {bonus_point}")


    # 화면 그리기
    background.show_img()
    hero.show_img()
    for m in missile_list:
        m.show_img()
    for e in enemy_list:
        e.show_img()

    # 점수, 목숨 표시 (우측 상단)
    draw_text(f"Score: {score}", size[0] - 150, 10)
    draw_text(f"Lives: {lives}", size[0] - 150, 50)

    pygame.display.flip()

pygame.quit()
