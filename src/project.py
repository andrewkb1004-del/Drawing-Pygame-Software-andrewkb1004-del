import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Drawing Pygame Software")
    fullscreen = False
    if fullscreen:
        screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        infoObject = pygame.display.Info()
        resolution = (infoObject.current_w, infoObject.current_h)
    else:
        window_width = 1920
        window_height = 1080
        resolution = (window_width, window_height)
        screen = pygame.display.set_mode(resolution)
    running = True
    pause = False
    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape key
                    running = False

        if not pause:                
            white = pygame.Color(255, 255, 255)
            screen.fill(white)
            pygame.display.flip()
    pygame.quit()


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()