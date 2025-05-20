import pygame
import pymysql
from db import connect_db  # db.py 파일에서 connect_db() 함수 있어야 함

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("로그인 & 회원가입")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# 폰트 설정
try:
    font_path = "GmarketSansMedium.otf"  # 같은 폴더에 위치해야 함
    font = pygame.font.Font(font_path, 24)
    label_font = pygame.font.Font(font_path, 30)
    button_font = pygame.font.Font(font_path, 28)
except FileNotFoundError:
    font = pygame.font.SysFont("malgungothic", 24)
    label_font = pygame.font.SysFont("malgungothic", 30)
    button_font = pygame.font.SysFont("malgungothic", 28)

# 입력 필드 상태
username_input = ""
password_input = ""
active_input = None

# 로그인/회원가입 모드
mode = "login"

# 텍스트 출력 함수
def draw_text(text, x, y, color=BLACK):
    screen.blit(font.render(text, True, color), (x, y))

# 버튼 출력 함수
def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=5)
    text_surface = button_font.render(text, True, text_color)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2,
                                y + (h - text_surface.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# 회원가입 처리
def register_user(username, password):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            conn.commit()
            return "회원가입 성공!"
    except pymysql.err.IntegrityError:
        return "이미 존재하는 사용자입니다!"
    finally:
        conn.close()

# 로그인 처리
def login_user(username, password):
    conn = connect_db()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

# 메인 루프
running = True
while running:
    screen.fill(WHITE)

    # 라벨 출력
    draw_text("아이디:", 50, 100)
    draw_text("비밀번호:", 50, 150)

    # 입력 상자 테두리
    pygame.draw.rect(screen, GRAY if active_input == "username" else BLACK, (150, 100, 200, 30), 2)
    pygame.draw.rect(screen, GRAY if active_input == "password" else BLACK, (150, 150, 200, 30), 2)

    # 입력 텍스트 출력
    draw_text(username_input, 160, 105)
    draw_text("*" * len(password_input), 160, 155)

    # 버튼 출력
    if mode == "login":
        login_button = draw_button("로그인", 200, 250, 100, 40, BLACK, WHITE)
        switch_button = draw_button("회원가입", 350, 350, 100, 30, WHITE, BLUE)
    else:
        register_button = draw_button("회원가입", 200, 250, 100, 40, BLACK, WHITE)
        switch_button = draw_button("로그인으로", 330, 350, 120, 30, WHITE, BLUE)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 150 <= x <= 350 and 100 <= y <= 130:
                active_input = "username"
            elif 150 <= x <= 350 and 150 <= y <= 180:
                active_input = "password"
            elif mode == "login" and login_button.collidepoint(x, y):
                if login_user(username_input, password_input):
                    print("로그인 성공!")
                else:
                    print("로그인 실패!")
            elif mode == "register" and register_button.collidepoint(x, y):
                print(register_user(username_input, password_input))
            elif switch_button.collidepoint(x, y):
                mode = "register" if mode == "login" else "login"
                username_input = ""
                password_input = ""

        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                if active_input == "username":
                    username_input = username_input[:-1]
                else:
                    password_input = password_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass  # 엔터 기능 향후 추가
            else:
                if active_input == "username":
                    username_input += event.unicode
                else:
                    password_input += event.unicode

pygame.quit()
