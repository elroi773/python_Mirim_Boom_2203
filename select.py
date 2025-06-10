import pygame
import subprocess
import sys

def main():
    # 초기화
    pygame.init()

    # 색상 정의
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # 화면 크기
    screen_width = 600
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("캐릭터 선택")

    # 폰트
    title_font = pygame.font.SysFont("malgungothic", 40)  # 제목 폰트 크게!
    text_font = pygame.font.SysFont("malgungothic", 24)

    # 이미지 불러오기
    img1 = pygame.image.load("./img/hero.png")
    img1 = pygame.transform.scale(img1, (150, 200))

    img2 = pygame.image.load("./img/hero2.png")
    img2 = pygame.transform.scale(img2, (150, 200))

    # 버튼 위치
    button1_rect = img1.get_rect(topleft=(120, 150))
    button2_rect = img2.get_rect(topleft=(330, 150))

    selected_character = None
    running = True

    while running:
        screen.fill(WHITE)

        # 제목 텍스트 중앙 정렬
        title_text = title_font.render("캐릭터를 선택하세요!", True, BLACK)
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        # 이미지 버튼
        screen.blit(img1, button1_rect.topleft)
        screen.blit(img2, button2_rect.topleft)

        # 마우스 오버 효과
        mouse_pos = pygame.mouse.get_pos()
        if button1_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (220, 220, 220), button1_rect)
            screen.blit(img1, button1_rect.topleft)
        if button2_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (220, 220, 220), button2_rect)
            screen.blit(img2, button2_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    selected_character = "hero.png"
                    print("선택된 캐릭터: hero.png")
                    subprocess.Popen([sys.executable, "./game.py"])
                    running = False
                elif button2_rect.collidepoint(event.pos):
                    selected_character = "hero2.png"
                    print("선택된 캐릭터: hero2.png")
                    subprocess.Popen([sys.executable, "./game1.py"])
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# 💡 여기서만 실행되도록 설정
if __name__ == "__main__":
    main()
