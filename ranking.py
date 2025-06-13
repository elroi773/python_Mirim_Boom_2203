import pygame
import pymysql
import math
import time

# DB에서 랭킹 불러오기
def get_rankings():
    conn = pymysql.connect(host='localhost', user='root', password='Mysql4344!', db='user_db', charset='utf8')
    rankings = []
    try:
        with conn.cursor() as cursor:
            sql = "SELECT username, score FROM users ORDER BY score DESC LIMIT 10"
            cursor.execute(sql)
            rankings = cursor.fetchall()
    finally:
        conn.close()
    return rankings

# 그라데이션 배경 그리기
def draw_gradient_background(screen, width, height):
    for y in range(height):
        # 상단에서 하단으로 갈수록 어두워지는 그라데이션
        ratio = y / height
        r = int(20 + (50 - 20) * ratio)
        g = int(20 + (30 - 20) * ratio)
        b = int(60 + (100 - 60) * ratio)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, y), (width, y))

# 반짝이는 별 효과
def draw_stars(screen, width, height, time_offset):
    star_positions = [
        (100, 80), (200, 120), (300, 60), (450, 90), (550, 110),
        (80, 200), (180, 250), (320, 180), (480, 220), (580, 190),
        (120, 320), (250, 370), (380, 340), (520, 380), (620, 350),
        (60, 450), (160, 420), (290, 480), (410, 440), (540, 470)
    ]
    
    for x, y in star_positions:
        # 시간에 따른 반짝임 효과
        alpha = int(128 + 127 * math.sin(time_offset * 2 + x * 0.01))
        size = 2 + int(1 * math.sin(time_offset * 3 + y * 0.01))
        
        # 별 모양 그리기
        star_color = (255, 255, 255, alpha)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size)
        
        # 십자 모양 광선 효과
        if size > 2:
            pygame.draw.line(screen, (255, 255, 255), (x-4, y), (x+4, y), 1)
            pygame.draw.line(screen, (255, 255, 255), (x, y-4), (x, y+4), 1)

# 왕관 아이콘 그리기 (1위용)
def draw_crown(screen, x, y):
    # 왕관 색상 (금색)
    crown_color = (255, 215, 0)
    gem_color = (255, 0, 0)
    
    # 왕관 베이스
    points = [(x-15, y+5), (x-10, y-5), (x-5, y), (x, y-8), (x+5, y), (x+10, y-5), (x+15, y+5)]
    pygame.draw.polygon(screen, crown_color, points)
    
    # 보석들
    pygame.draw.circle(screen, gem_color, (x-8, y-2), 2)
    pygame.draw.circle(screen, gem_color, (x, y-5), 2)
    pygame.draw.circle(screen, gem_color, (x+8, y-2), 2)

# 메달 그리기 (2, 3위용)
def draw_medal(screen, x, y, rank):
    if rank == 2:
        medal_color = (192, 192, 192)  # 은메달
    else:
        medal_color = (205, 127, 50)   # 동메달
    
    # 메달 원
    pygame.draw.circle(screen, medal_color, (x, y), 12)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 10)
    pygame.draw.circle(screen, medal_color, (x, y), 8)
    
    # 순위 숫자
    font = pygame.font.Font(None, 16)
    text = font.render(str(rank), True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# 애니메이션 효과가 있는 랭킹 항목 그리기
def draw_ranking_item(screen, rank, username, score, y_pos, width, is_current_user, time_offset):
    # 배경 패널
    panel_color = (40, 40, 60, 180) if not is_current_user else (0, 100, 50, 200)
    panel_rect = pygame.Rect(50, y_pos - 5, width - 100, 50)
    
    # 현재 사용자일 경우 펄싱 효과
    if is_current_user:
        pulse = int(20 * math.sin(time_offset * 4))
        panel_color = (0, 100 + pulse, 50 + pulse, 200)
    
    # 패널 그리기 (둥근 모서리 효과)
    pygame.draw.rect(screen, panel_color[:3], panel_rect, border_radius=10)
    
    # 순위별 아이콘
    if rank == 1:
        draw_crown(screen, 80, y_pos + 15)
    elif rank in [2, 3]:
        draw_medal(screen, 80, y_pos + 15, rank)
    else:
        # 4위 이하는 숫자로 표시
        font = pygame.font.Font(None, 36)
        rank_text = font.render(str(rank), True, (255, 255, 255))
        screen.blit(rank_text, (70, y_pos + 5))
    
    # 사용자명 (현재 사용자는 특별한 색상)
    font_name = pygame.font.SysFont("malgungothic", 28, bold=True)
    name_color = (255, 255, 255) if not is_current_user else (255, 255, 0)
    name_text = font_name.render(username, True, name_color)
    screen.blit(name_text, (120, y_pos + 5))
    
    # 점수 (그라데이션 효과)
    font_score = pygame.font.SysFont("malgungothic", 24)
    score_color = (200, 200, 255) if not is_current_user else (255, 255, 100)
    score_text = font_score.render(f"{score:,}점", True, score_color)
    screen.blit(score_text, (width - 200, y_pos + 10))
    
    # 현재 사용자 표시
    if is_current_user:
        badge_font = pygame.font.SysFont("malgungothic", 18)
        badge_text = badge_font.render("YOU", True, (255, 255, 255))
        badge_rect = pygame.Rect(width - 300, y_pos + 5, 60, 25)
        pygame.draw.rect(screen, (255, 100, 100), badge_rect, border_radius=5)
        screen.blit(badge_text, (width - 285, y_pos + 10))

# 타이틀 텍스트에 그라데이션 효과
def draw_gradient_text(screen, text, font, x, y, color1, color2):
    # 텍스트 렌더링
    text_surface = font.render(text, True, color1)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    
    # 그라데이션 효과를 위한 여러 레이어
    shadow_surface = font.render(text, True, (50, 50, 50))
    shadow_rect = shadow_surface.get_rect()
    shadow_rect.center = (x + 3, y + 3)
    screen.blit(shadow_surface, shadow_rect)
    
    screen.blit(text_surface, text_rect)

# 파티클 효과
def draw_particles(screen, width, height, time_offset):
    particles = []
    for i in range(20):
        x = (i * 35 + time_offset * 50) % width
        y = 50 + 30 * math.sin(time_offset + i * 0.5)
        size = 1 + int(1 * math.sin(time_offset * 2 + i))
        alpha = int(100 + 100 * math.sin(time_offset * 3 + i * 0.3))
        
        color = (255, 255, 255, alpha)
        pygame.draw.circle(screen, color[:3], (int(x), int(y)), size)

# Pygame으로 랭킹 화면 띄우기
def show_ranking_screen(current_user=None):
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🏆 미림 탈출 랭킹 🏆")
    
    # 폰트 로드
    try:
        font_title = pygame.font.Font("GmarketSansMedium.otf", 48)
        font_subtitle = pygame.font.Font("GmarketSansMedium.otf", 24)
    except:
        font_title = pygame.font.SysFont("malgungothic", 48, bold=True)
        font_subtitle = pygame.font.SysFont("malgungothic", 24)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    
    rankings = get_rankings()
    running = True
    
    while running:
        current_time = time.time()
        time_offset = current_time - start_time
        
        # 그라데이션 배경
        draw_gradient_background(screen, WIDTH, HEIGHT)
        
        # 반짝이는 별들
        draw_stars(screen, WIDTH, HEIGHT, time_offset)
        
        # 파티클 효과
        draw_particles(screen, WIDTH, HEIGHT, time_offset)
        
        # 메인 타이틀
        title_color1 = (255, 215, 0)  # 금색
        title_color2 = (255, 165, 0)  # 주황색
        draw_gradient_text(screen, "🏆 미림 탈출 랭킹 🏆", font_title, 
                          WIDTH // 2, 60, title_color1, title_color2)
        
        # 부제목
        subtitle_text = "최고의 탈출 전문가들을 축하합니다!"
        subtitle_surface = font_subtitle.render(subtitle_text, True, (200, 200, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # 구분선
        pygame.draw.line(screen, (100, 100, 150), (50, 130), (WIDTH - 50, 130), 3)
        
        # 랭킹 리스트
        if rankings:
            for idx, (username, score) in enumerate(rankings):
                if idx >= 10:  # 상위 10명만 표시
                    break
                    
                rank = idx + 1
                y_position = 160 + idx * 60
                is_current = (username == current_user)
                
                draw_ranking_item(screen, rank, username, score, y_position, 
                                WIDTH, is_current, time_offset)
        else:
            # 랭킹이 없을 때
            no_data_text = font_subtitle.render("아직 랭킹 데이터가 없습니다.", True, (150, 150, 150))
            no_data_rect = no_data_text.get_rect(center=(WIDTH // 2, 300))
            screen.blit(no_data_text, no_data_rect)
        
        # 하단 안내 텍스트
        info_font = pygame.font.SysFont("malgungothic", 18)
        info_text = "창을 닫으려면 X 버튼을 클릭하세요"
        info_surface = info_font.render(info_text, True, (150, 150, 150))
        info_rect = info_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(info_surface, info_rect)
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

# 로그인된 사용자 정보 가져오기
def get_logged_in_username():
    try:
        with open("logged_in_user.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# 테스트 실행
if __name__ == "__main__":
    current_user = get_logged_in_username()
    show_ranking_screen(current_user=current_user)