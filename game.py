import pygame
import random
import time
import os

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

    def show_img(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Game:
    def __init__(self, difficulty):  # 난이도 매개변수
        pygame.init()
        self.difficulty = difficulty  # ✅ 난이도 기본값 추가 (1~5 사이 조정 가능)
        
        self.WIDTH = 600
        self.HEIGHT = 900
        self.GAME_WIDTH = 400
        self.TIMETABLE_WIDTH = self.WIDTH - self.GAME_WIDTH

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("pygameEX")

        self.clock = pygame.time.Clock()
        self.black_color = (0, 0, 0)
        self.white_color = (255, 255, 255)
        self.gray_color = (230, 230, 230)
        self.font = pygame.font.Font("GmarketSansMedium.otf", 20)

        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.missile_list = []
        self.enemy_list = []
        self.left_move = False
        self.right_move = False
        self.space_on = False
        self.k = 0
        self.start_time = time.time()
        self.time_limit = 30

        self.background = Img_Object()
        try:
            self.background.add_img("./img/game_background.png")
            self.background.change_size(self.GAME_WIDTH, self.HEIGHT)
        except Exception as e:
            print(f"[ERROR] 배경 이미지 오류: {e}")
            return False

        self.hero = Img_Object()
        try:
            self.hero.add_img("./img/hero.png")
            self.hero.change_size(130, 180)
        except Exception as e:
            print(f"[ERROR] hero 이미지 오류: {e}")
            return False

        self.hero.x = round(self.GAME_WIDTH / 2) - round(self.hero.width / 2)
        self.hero.y = self.HEIGHT - self.hero.height - 100
        self.hero.move = 5

        return True
    
    def handle_events(self):
        # 이벤트 처리 메소드
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_move = True
                elif event.key == pygame.K_RIGHT:
                    self.right_move = True
                elif event.key == pygame.K_SPACE:
                    self.space_on = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_move = False
                elif event.key == pygame.K_RIGHT:
                    self.right_move = False
                elif event.key == pygame.K_SPACE:
                    self.space_on = False
        return True
    
    def update_hero(self):
        # 영웅 위치 업데이트 메소드
        if self.left_move:
            self.hero.x -= self.hero.move
            if self.hero.x <= 0:
                self.hero.x = 0
        if self.right_move:
            self.hero.x += self.hero.move
            if self.hero.x >= self.GAME_WIDTH - self.hero.width:
                self.hero.x = self.GAME_WIDTH - self.hero.width
    
    def create_missile(self):
        # 미사일 생성 메소드
        if self.space_on and self.k % 6 == 0:
            missile = Img_Object()
            try:
                missile.add_img("./img/missile.png")
                missile.change_size(25, 40)
                missile.x = self.hero.x + self.hero.width / 2 - missile.width / 2
                missile.y = self.hero.y - missile.height - 10
                missile.move = 8
                self.missile_list.append(missile)
            except Exception as e:
                print(f"[ERROR] missile 이미지 오류: {e}")
    
    def update_missiles(self):
        # 미사일 위치 업데이트 메소드
        new_missile_list = []
        for m in self.missile_list:
            m.y -= m.move
            if m.y > -m.height:
                new_missile_list.append(m)
        self.missile_list = new_missile_list
    
    # 적 생성 메소드
    def create_enemy(self):
        # 난이도별 enemy 등장 확률 설정
        base_prob = 0.98 - (self.difficulty * 0.03)  # 난이도 1: 0.88, 난이도 5: 0.48

        if random.random() >= base_prob:
            obj = Img_Object()
            try:
                r = random.random()
                if r > 0.5:
                    obj.add_img("./img/enemy.png")
                elif r > 0.2:
                    obj.add_img("./img/java.png")
                obj.change_size(35, 35)
                obj.x = random.randrange(round(self.hero.width / 2), 
                                        self.GAME_WIDTH - obj.width - round(self.hero.width / 2))
                obj.y = 15
                # 난이도에 따라 enemy 속도 증가
                obj.move = 2 + self.difficulty  # 난이도 1: 3, 난이도 5: 7
                self.enemy_list.append(obj)
            except Exception as e:
                print(f"[ERROR] 적기 이미지 오류: {e}")

    
    def update_enemies(self):
        # 적 위치 업데이트 메소드
        new_enemy_list = []
        for e in self.enemy_list:
            e.y += e.move
            if e.y <= self.HEIGHT:
                new_enemy_list.append(e)
        self.enemy_list = new_enemy_list
    
    def check_missile_collisions(self):
        # 미사일과 적의 충돌 검사 메소드
        crash_m_list = []
        crash_e_list = []
        bonus_point = 0
        
        for m in self.missile_list:
            for e in self.enemy_list:
                if (m.x - e.width <= e.x <= m.x + m.width) and (m.y - e.height <= e.y <= m.y + m.height):
                    if "java.png" in e.img_path:
                        crash_m_list.append(m)
                        crash_e_list.append(e)
                        print(f"Java 맞음! 점수: {self.score}")
                        if self.score % 10 == 0 and self.score != 0:
                            bonus_point += 10
                            print(f"보너스 점수! 현재 보너스: {bonus_point}")
                            self.score += bonus_point
                    else:
                        crash_m_list.append(m)
                        crash_e_list.append(e)
        
        # 충돌한 객체들 제거
        for m in crash_m_list:
            if m in self.missile_list:
                self.missile_list.remove(m)
        for e in crash_e_list:
            if e in self.enemy_list:
                self.enemy_list.remove(e)
    
    def check_hero_collisions(self):
        for e in self.enemy_list[:]:  # 복사본으로 순회
            if (self.hero.x - e.width <= e.x <= self.hero.x + self.hero.width) and \
               (self.hero.y - e.height <= e.y <= self.hero.y + self.hero.height):
                if "enemy.png" in e.img_path:
                    self.lives -= 1
                    self.enemy_list.remove(e)
                    if self.lives <= 0:
                        print(f"게임 오버: 주인공과 {e.img_path} 충돌")
                        return False
                elif "java.png" in e.img_path:
                    self.score += 1
                    print(f"Java 충돌! 점수: {self.score}")
                    self.enemy_list.remove(e)
                    if self.score % 10 == 0:
                        bonus_point = 10
                        self.score += bonus_point
                        print(f"보너스 점수! 현재 보너스: {bonus_point}")
        return True
    
    def check_time_limit(self):
        # 시간 제한 검사 메소드
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, int(self.time_limit - elapsed_time))
        
        if elapsed_time >= self.time_limit:
            print("30초 시간 종료! 게임 오버")
            return False, remaining_time
        
        return True, remaining_time
    
    def draw_text(self, text, pos_x, pos_y, color=None):
        # 텍스트 그리기 메소드
        if color is None:
            color = self.white_color
        img = self.font.render(text, True, color)
        self.screen.blit(img, (pos_x, pos_y))
    
    def draw_game(self, remaining_time):
        # 게임 화면 그리기 메소드
        # 배경 그리기
        self.background.show_img(self.screen)
        pygame.draw.rect(self.screen, self.gray_color, 
                        [self.GAME_WIDTH, 0, self.TIMETABLE_WIDTH, self.HEIGHT])
        
        # 게임 객체들 그리기
        self.hero.show_img(self.screen)
        for m in self.missile_list:
            m.show_img(self.screen)
        for e in self.enemy_list:
            e.show_img(self.screen)
        
        # UI 텍스트 그리기
        self.draw_text(f"남은 시간: {remaining_time}초", 20, 10)
        self.draw_text(f"Score: {self.score}", 240, 10)
        self.draw_text(f"Lives: {self.lives}", 240, 50)
        
        # 시간표 그리기
        self.draw_text("오늘의 시간표", self.GAME_WIDTH + 20, 20, self.black_color)
        self.draw_text("1교시: JAVA", self.GAME_WIDTH + 20, 60, (0, 0, 255))
        self.draw_text("2교시: HTML", self.GAME_WIDTH + 20, 100, self.black_color)
        self.draw_text("3교시: PYTHON", self.GAME_WIDTH + 20, 140, self.black_color)
        self.draw_text("4교시: PHP", self.GAME_WIDTH + 20, 180, self.black_color)
        
        pygame.display.flip()
    
    def run_game(self):
        # 게임 메인 루프 메소드
        if not self.reset_game():
            print("게임 초기화 실패")
            return False
        
        running = True
        
        while running:
            self.clock.tick(60)
            
            # 시간 제한 검사
            time_ok, remaining_time = self.check_time_limit()
            if not time_ok:
                time.sleep(2)
                break
            
            # 이벤트 처리
            if not self.handle_events():
                break
            
            # 게임 로직 업데이트
            self.update_hero()
            self.create_missile()
            self.update_missiles()
            self.create_enemy()
            self.update_enemies()
            
            # 충돌 검사
            self.check_missile_collisions()
            if not self.check_hero_collisions():
                time.sleep(3)
                break
            
            # 화면 그리기
            self.draw_game(remaining_time)
            
            self.k += 1
        
        return True
    
    def quit_game(self):
        # 게임 종료 메소드
        pygame.quit()

def main():
    for level in range(1, 6):  # 난이도 1 ~ 5
        print(f"\n==== 난이도 {level}단계 시작 ====\n")
        game = Game(difficulty=level)

        try:
            success = game.run_game()
            if not success:
                print(f"난이도 {level}에서 게임 종료")
                break
        except Exception as e:
            print(f"난이도 {level} 실행 중 오류 발생: {e}")
            break
        finally:
            game.quit_game()
        
        time.sleep(2)  # 다음 단계로 넘어가기 전 잠시 대기

if __name__ == "__main__":
    main()