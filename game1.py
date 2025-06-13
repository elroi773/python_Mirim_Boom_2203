import pygame
import random
import time
import os
import pymysql
import subprocess
import sys  # Add this missing import


def get_logged_in_username():
    try:
        with open("logged_in_user.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None



class Img_Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.move = 0
        self.img_path = ""
        self.img = None

    def add_img(self, address):
        if not os.path.exists(address):
            print(f"[경고] 이미지 파일을 찾을 수 없습니다: {address}")
            # 기본 이미지 생성 (색상 사각형)
            self.img = pygame.Surface((50, 50))
            if "hero" in address:
                self.img.fill((0, 255, 0))  # 초록색 - 영웅
            elif "missile" in address:
                self.img.fill((255, 255, 0))  # 노란색 - 미사일
            elif "java" in address or "html" in address or "python" in address or "php" in address or "css" in address:
                self.img.fill((0, 0, 255))  # 파란색 - 과목
            elif "enemy" in address:
                self.img.fill((255, 0, 0))  # 빨간색 - 적
            else:
                self.img.fill((128, 128, 128))  # 회색 - 기본
            self.img_path = address
            return
            
        try:
            if address.lower().endswith(".png"):
                self.img = pygame.image.load(address).convert_alpha()
            else:
                self.img = pygame.image.load(address).convert()
            self.img_path = address
        except pygame.error as e:
            print(f"[경고] 이미지 로드 실패: {address}, 오류: {e}")
            # 기본 이미지로 대체
            self.img = pygame.Surface((50, 50))
            self.img.fill((128, 128, 128))
            self.img_path = address

    def change_size(self, width, height):
        if self.img:
            self.img = pygame.transform.scale(self.img, (width, height))
            self.width, self.height = self.img.get_size()

    def show_img(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))

class Game:
    def __init__(self, difficulty, initial_score=0):  # initial_score 매개변수 추가
        pygame.init()
        self.difficulty = difficulty
        self.total_score = initial_score  # 누적 점수를 저장할 변수 추가
        
        # 시간표 정보 (난이도별)
        self.timetable = {
            1: {"subject": "JAVA", "good_img": "./img/java.png", "enemy_img": "./img/enemy.png", "color": (0, 0, 255)},
            2: {"subject": "HTML", "good_img": "./img/html.png", "enemy_img": "./img/css.png", "color": (255, 165, 0)},
            3: {"subject": "PYTHON", "good_img": "./img/python.png", "enemy_img": "./img/kotlin.png", "color": (255, 215, 0)},
            4: {"subject": "PHP", "good_img": "./img/php.png", "enemy_img": "./img/nodejs.png", "color": (128, 0, 128)},
            5: {"subject": "MY SQL", "good_img": "./img/mysql.png", "enemy_img": "./img/mariadb.png", "color": (255, 20, 147)}
        }
        
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
        
        # 폰트 로드 시도, 실패시 기본 폰트 사용
        try:
            self.font = pygame.font.Font("GmarketSansMedium.otf", 20)
        except:
            print("[경고] 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
            self.font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        self.score = 0  # 현재 단계에서의 점수만 초기화
        # self.total_score는 초기화하지 않음 (누적 유지)
        self.lives = 3
        self.missile_list = []
        self.enemy_list = []
        self.left_move = False
        self.right_move = False
        self.space_on = False
        self.k = 0
        self.start_time = time.time()
        self.time_limit = 30

        # 배경 설정
        self.background = Img_Object()
        self.background.add_img("./img/game_background.png")
        self.background.change_size(self.GAME_WIDTH, self.HEIGHT)

        # 영웅 설정
        self.hero = Img_Object()
        self.hero.add_img("./img/hero2.png")
        self.hero.change_size(130, 180)
        self.hero.x = round(self.GAME_WIDTH / 2) - round(self.hero.width / 2)
        self.hero.y = self.HEIGHT - self.hero.height - 100
        self.hero.move = 5

        return True
    
    def handle_events(self):
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
        if self.left_move:
            self.hero.x -= self.hero.move
            if self.hero.x <= 0:
                self.hero.x = 0
        if self.right_move:
            self.hero.x += self.hero.move
            if self.hero.x >= self.GAME_WIDTH - self.hero.width:
                self.hero.x = self.GAME_WIDTH - self.hero.width
    
    def create_missile(self):
        if self.space_on and self.k % 6 == 0:
            missile = Img_Object()
            missile.add_img("./img/missile.png")
            missile.change_size(25, 40)
            missile.x = self.hero.x + self.hero.width / 2 - missile.width / 2
            missile.y = self.hero.y - missile.height - 10
            missile.move = 8
            self.missile_list.append(missile)
    
    def update_missiles(self):
        new_missile_list = []
        for m in self.missile_list:
            m.y -= m.move
            if m.y > -m.height:
                new_missile_list.append(m)
        self.missile_list = new_missile_list
    
    def create_enemy(self):
        base_prob = 0.98 - (self.difficulty * 0.03)
        
        if random.random() >= base_prob:
            obj = Img_Object()
            r = random.random()
            
            # 현재 난이도에 맞는 이미지 사용
            current_level = self.timetable.get(self.difficulty, self.timetable[1])
            
            if r > 0.5:
                # 적 이미지 (enemy 역할)
                obj.add_img(current_level["enemy_img"])
            else:
                # 좋은 이미지 (과목 이미지)
                obj.add_img(current_level["good_img"])
                
            obj.change_size(35, 35)
            obj.x = random.randrange(round(self.hero.width / 2), 
                                    self.GAME_WIDTH - obj.width - round(self.hero.width / 2))
            obj.y = 15
            obj.move = 2 + self.difficulty
            self.enemy_list.append(obj)
    
    def update_enemies(self):
        new_enemy_list = []
        for e in self.enemy_list:
            e.y += e.move
            if e.y <= self.HEIGHT:
                new_enemy_list.append(e)
        self.enemy_list = new_enemy_list
    
    def check_missile_collisions(self):
        crash_m_list = []
        crash_e_list = []
        current_level = self.timetable.get(self.difficulty, self.timetable[1])
        
        for m in self.missile_list:
            for e in self.enemy_list:
                if (m.x < e.x + e.width and m.x + m.width > e.x and 
                    m.y < e.y + e.height and m.y + m.height > e.y):
                    crash_m_list.append(m)
                    crash_e_list.append(e)
                    
                    # 현재 난이도의 좋은 이미지인지 확인
                    if current_level["good_img"] in e.img_path:
                        print(f"{current_level['subject']} 맞음! 현재 점수: {self.score}, 총점: {self.total_score + self.score}")
                        # self.score += 1
                        if self.score % 10 == 0 and self.score != 0:
                            bonus_point = 10
                            self.score += bonus_point
                            print(f"보너스 점수! 현재 점수: {self.score}, 총점: {self.total_score + self.score}")
                    else:
                        # 적 이미지를 맞춘 경우
                        self.score += 1
        
        # 충돌한 객체들 제거
        for m in crash_m_list:
            if m in self.missile_list:
                self.missile_list.remove(m)
        for e in crash_e_list:
            if e in self.enemy_list:
                self.enemy_list.remove(e)
    
    def check_hero_collisions(self):
        current_level = self.timetable.get(self.difficulty, self.timetable[1])
        
        for e in self.enemy_list[:]:
            if (self.hero.x < e.x + e.width and self.hero.x + self.hero.width > e.x and
                self.hero.y < e.y + e.height and self.hero.y + self.hero.height > e.y):
                
                # 적 이미지와 충돌한 경우
                if current_level["enemy_img"] in e.img_path:
                    self.lives -= 1
                    self.enemy_list.remove(e)
                    print(f"적과 충돌! 남은 생명: {self.lives}")
                    if self.lives <= 0:
                        print(f"게임 오버: 생명력 소진")
                        return False
                # 좋은 이미지와 충돌한 경우
                elif current_level["good_img"] in e.img_path:
                    # self.score += 1
                    print(f"{current_level['subject']} 충돌! 현재 점수: {self.score}, 총점: {self.total_score + self.score}")
                    self.enemy_list.remove(e)
                    if self.score % 10 == 0:
                        bonus_point = 10
                        self.score += bonus_point
                        print(f"보너스 점수! 현재 점수: {self.score}, 총점: {self.total_score + self.score}")
        return True
    
    def check_time_limit(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, int(self.time_limit - elapsed_time))
        
        if elapsed_time >= self.time_limit:
            print("30초 시간 종료! 게임 오버")
            return False, remaining_time
        
        return True, remaining_time
    
    def draw_text(self, text, pos_x, pos_y, color=None):
        if color is None:
            color = self.white_color
        img = self.font.render(text, True, color)
        self.screen.blit(img, (pos_x, pos_y))
    
    def draw_game(self, remaining_time):
        # 화면 지우기
        self.screen.fill(self.black_color)
        
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
        
        # UI 텍스트 그리기 (현재 점수와 총점 모두 표시)
        self.draw_text(f"남은 시간: {remaining_time}초", 20, 10)
        self.draw_text(f"현재: {self.score}", 240, 10)
        self.draw_text(f"총점: {self.total_score + self.score}", 240, 30)
        self.draw_text(f"Lives: {self.lives}", 240, 50)
        self.draw_text(f"Level: {self.difficulty}", 20, 50)
        
        # 시간표 그리기 (현재 난이도 강조)
        self.draw_text("오늘의 시간표", self.GAME_WIDTH + 20, 20, self.black_color)
        
        timetable_subjects = [
            (1, "1교시: JAVA", (128, 128, 128)),      # 회색 (기본)
            (2, "2교시: HTML", (128, 128, 128)),      # 회색 (기본)
            (3, "3교시: PYTHON", (128, 128, 128)),    # 회색 (기본)
            (4, "4교시: PHP", (128, 128, 128)),       # 회색 (기본)
            (5, "5교시: MY SQL", (128, 128, 128))     # 회색 (기본)
        ]
        
        for i, (level, subject_text, default_color) in enumerate(timetable_subjects):
            y_pos = 60 + (i * 40)
            if level == self.difficulty:
                # 현재 난이도는 파란색으로 강조하고 배경색 추가
                pygame.draw.rect(self.screen, (255, 255, 200), 
                               [self.GAME_WIDTH + 15, y_pos - 5, 160, 30])
                self.draw_text(f">>> {subject_text} <<<", self.GAME_WIDTH + 20, y_pos, (0, 0, 255))  # 파란색
            else:
                self.draw_text(subject_text, self.GAME_WIDTH + 20, y_pos, default_color)  # 회색
        
        # 현재 과목 정보 표시
        current_level = self.timetable.get(self.difficulty, self.timetable[1])
        self.draw_text("현재 과목:", self.GAME_WIDTH + 20, 280, self.black_color)
        self.draw_text(current_level["subject"], self.GAME_WIDTH + 20, 310, current_level["color"])
        
        pygame.display.flip()

    
    
    def run_game(self):
        if not self.reset_game():
            print("게임 초기화 실패")
            return False, 0
        
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
        
        return True, self.score  # 현재 단계 점수 반환
    
    def quit_game(self):
        pygame.quit()



def update_ranking(username, score):
    conn = pymysql.connect(host='localhost', user='root', password='Mysql4344!', db='user_db', charset='utf8')
    cur = conn.cursor()
    
    try:
        # SCORE 컬럼이 없어도 오류가 발생하지 않도록 처리
        sql = "UPDATE USERS SET SCORE = %s WHERE username = %s"
        cur.execute(sql, (score, username))
        conn.commit()
        
    except pymysql.err.OperationalError as e:
        if "Unknown column 'SCORE'" in str(e):
            # SCORE 컬럼 추가 후 다시 시도
            cur.execute("ALTER TABLE USERS ADD COLUMN SCORE INT DEFAULT 0")
            cur.execute("UPDATE USERS SET SCORE = %s WHERE username = %s", (score, username))
            conn.commit()
        else:
            raise e
    finally:
        cur.close()
        conn.close()


def main():

    
    print("게임을 시작합니다!")
    

    username = get_logged_in_username()
    if username is None:
        print("로그인된 사용자 정보가 없습니다.")
        return

    total_accumulated_score = 0  # 전체 누적 점수
    
    for level in range(1, 6):
        print(f"\n==== 난이도 {level}단계 시작 ====")
        print(f"현재 누적 점수: {total_accumulated_score}")
        print()
        
        game = Game(difficulty=level, initial_score=total_accumulated_score)

        try:
            success, stage_score = game.run_game()
            total_accumulated_score += stage_score  # 각 단계 점수를 누적
            print(f"난이도 {level} - 이번 단계 점수: {stage_score}, 총 누적 점수: {total_accumulated_score}")
            
            if not success:
                print(f"난이도 {level}에서 게임 종료")
                break
        except Exception as e:
            print(f"난이도 {level} 실행 중 오류 발생: {e}")
            break
        finally:
            game.quit_game()
        
        print(f"난이도 {level} 완료!")
        time.sleep(2)
    
    print(f"\n게임 종료! 최종 누적 점수: {total_accumulated_score}")
    
    update_ranking(username, total_accumulated_score)
    subprocess.Popen([sys.executable, "./ranking.py"])

    


if __name__ == "__main__":
    main()