import pygame
import pymysql
from db import connect_db  # db.py 파일에서 connect_db 함수 import
import subprocess
import sys


pygame.init()

# 화면 설정
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("로그인 & 회원가입")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 80, 200)
LIGHT_BLUE = (170, 190, 255)

# 폰트 설정
try:
    font_path = "GmarketSansMedium.otf"
    font = pygame.font.Font(font_path, 24)
    label_font = pygame.font.Font(font_path, 30)
    button_font = pygame.font.Font(font_path, 28)
    status_font = pygame.font.Font(font_path, 22)
except:
    font = pygame.font.SysFont("malgungothic", 24)
    label_font = pygame.font.SysFont("malgungothic", 30)
    button_font = pygame.font.SysFont("malgungothic", 28)
    status_font = pygame.font.SysFont("malgungothic", 22)

# 입력 필드 상태
username_input = ""
password_input = ""
active_input = None

# 로그인/회원가입 모드
mode = "login"
status_message = ""

# 배경 이미지
background_img = pygame.image.load("./img/backgroundimg.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# 텍스트 출력
def draw_shadow_text(text, x, y, font, color=WHITE):
    shadow = font.render(text, True, BLACK)
    screen.blit(shadow, (x + 2, y + 2))
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# 버튼 출력
def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=10)
    text_surface = button_font.render(text, True, text_color)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2,
                                y + (h - text_surface.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# 로그인 함수
def login_user(username, password):
    conn = connect_db()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

# 회원가입 함수
def register_user(username, password):
    if not username or not password:
        return "⚠️ 아이디와 비밀번호를 입력하세요."

    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 아이디 중복 확인
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            if cursor.fetchone():
                return "❌ 이미 존재하는 아이디입니다."

            # 회원가입
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            conn.commit()
            return "✅ 회원가입 성공!"
    except Exception as e:
        return f"❌ 오류 발생: {e}"
    finally:
        conn.close()

# 메인 루프
running = True
while running:
    screen.blit(background_img, (0, 0))

    # UI 요소 위치
    input_x, input_w, input_h = 250, 200, 35
    username_rect = pygame.Rect(input_x, 140, input_w, input_h)
    password_rect = pygame.Rect(input_x, 200, input_w, input_h)

    # 텍스트
    draw_shadow_text("아이디", 150, 145, label_font)
    draw_shadow_text("비밀번호", 130, 205, label_font)

    # 입력 상자
    pygame.draw.rect(screen, WHITE, username_rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, password_rect, border_radius=8)

    pygame.draw.rect(screen, BLUE if active_input == "username" else BLACK, username_rect, 2, border_radius=8)
    pygame.draw.rect(screen, BLUE if active_input == "password" else BLACK, password_rect, 2, border_radius=8)

    screen.blit(font.render(username_input, True, BLACK), (username_rect.x + 10, username_rect.y + 5))
    screen.blit(font.render("*" * len(password_input), True, BLACK), (password_rect.x + 10, password_rect.y + 5))

    # 버튼
    if mode == "login":
        login_button = draw_button("로그인", 290, 270, 120, 45, BLUE, WHITE)
        switch_button = draw_button("회원가입", 290, 330, 120, 40, WHITE, BLUE)
    else:
        register_button = draw_button("회원가입", 290, 270, 120, 45, BLUE, WHITE)
        switch_button = draw_button("로그인으로", 290, 330, 120, 40, WHITE, BLUE)

    # 상태 메시지 출력
    if status_message:
        screen.blit(status_font.render(status_message, True, BLACK), (WIDTH // 2 - 120, 390))

    pygame.display.flip()

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if username_rect.collidepoint(x, y):
                active_input = "username"
            elif password_rect.collidepoint(x, y):
                active_input = "password"
            elif mode == "login" and login_button.collidepoint(x, y):
                if login_user(username_input, password_input):
                    status_message = "🎉 로그인 성공!"
                    pygame.display.flip()
                    pygame.time.delay(1000)  # 잠시 메시지를 보여주기 위해 1초 대기
                    pygame.quit()  # 현재 Pygame 창 닫기
                    subprocess.Popen([sys.executable, "game.py"])  # game.py 실행
                    sys.exit()  # 현재 로그인 프로그램 종료
                else:
                    status_message = "❌ 로그인 실패!"

            elif mode == "register" and register_button.collidepoint(x, y):
                status_message = register_user(username_input, password_input)
            elif switch_button.collidepoint(x, y):
                mode = "register" if mode == "login" else "login"
                username_input = ""
                password_input = ""
                status_message = ""

        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                if active_input == "username":
                    username_input = username_input[:-1]
                elif active_input == "password":
                    password_input = password_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                if active_input == "username":
                    username_input += event.unicode
                elif active_input == "password":
                    password_input += event.unicode

pygame.quit()
