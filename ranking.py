import pygame
import pymysql

# DB에서 랭킹 불러오기
def get_rankings():
    conn = pymysql.connect(host='localhost', user='root', password='Mysql4344!', db='user_db', charset='utf8')
    rankings = []
    try:
        with conn.cursor() as cursor:
            sql = "SELECT username, score FROM users ORDER BY score DESC"
            cursor.execute(sql)
            rankings = cursor.fetchall()
    finally:
        conn.close()
    return rankings

# Pygame으로 랭킹 화면 띄우기
def show_ranking_screen(current_user=None):
    pygame.init()
    WIDTH, HEIGHT = 700, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("점수 랭킹")

    font_title = pygame.font.SysFont("malgungothic", 40)
    font_text = pygame.font.SysFont("malgungothic", 28)
    clock = pygame.time.Clock()

    rankings = get_rankings()
    running = True

    while running:
        screen.fill((30, 30, 30))  # 다크 배경

        title_surface = font_title.render("사용자 점수 랭킹", True, (255, 215, 0))
        title_surface = font_title.render("미림 탈출을 축하합니다!", True, (255, 215, 0))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 30))

        for idx, (username, score) in enumerate(rankings):
            text = f"{idx+1}위 | {username} | 점수: {score}"
            color = (255, 255, 255)
            if username == current_user:
                color = (0, 255, 127)  # 현재 사용자 강조
            text_surface = font_text.render(text, True, color)
            screen.blit(text_surface, (100, 100 + idx * 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 테스트 실행
if __name__ == "__main__":
    show_ranking_screen(current_user="홍길동")  # 게임 끝난 사용자 이름
