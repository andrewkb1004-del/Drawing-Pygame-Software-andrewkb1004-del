import pygame
import os
import sys

def main():
    pygame.init()
    pygame.display.set_caption("Drawing Pygame Software")
    fullscreen = False
    if fullscreen:
        screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        infoObject = pygame.display.Info()
        screen_width, screen_height = infoObject.current_w, infoObject.current_h
        resolution = (screen_width, screen_height)
    else:
        screen_width = 1280
        screen_height = 768
        resolution = (screen_width, screen_height)
        screen = pygame.display.set_mode(resolution)

    line_thickness = 2 # Initial brush size
    current_color = BLACK # Default drawing color
    background_color = WHITE

    # Font Setup
    font = pygame.font.SysFont('Arial', 12)

    # Create a separate surface for drawing.
    canvas = pygame.Surface((screen_width, screen_height))
    canvas.fill(background_color)

    running = True
    drawing = False # Flag to check if the mouse button is held down
    last_pos = None # To store the last mouse position for continuous lines

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                    last_pos = event.pos # Start drawing from current position

            # Mouse Button Up Event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    drawing = False
                    last_pos = None # Reset last_pos when button is released

            # Mouse Motion Event
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    current_pos = event.pos
                    if last_pos:
                        # Draw a line from the last position to the current position
                        # This makes the drawing smooth rather than just dots
                        pygame.draw.line(canvas, current_color, last_pos, current_pos, line_thickness)
                    last_pos = current_pos # Update last_pos for the next segment

            # Keyboard Events
            if event.type == pygame.KEYDOWN:
                # Change Color
                if event.key == pygame.K_1:
                    current_color = BLACK
                elif event.key == pygame.K_2:
                    current_color = RED
                elif event.key == pygame.K_3:
                    current_color = GREEN
                elif event.key == pygame.K_4:
                    current_color = BLUE
                elif event.key == pygame.K_5:
                    current_color = YELLOW
                elif event.key == pygame.K_6: # Assign PURPLE to key 6
                    current_color = PURPLE
                elif event.key == pygame.K_0: # Assign background_color to key 0.  This is essentially the eraser.
                    current_color = background_color

                # Clear Screen
                elif event.key == pygame.K_c:
                    canvas.fill(background_color) # Fill the canvas surface with background color

                # Change Brush Size
                elif event.key == pygame.K_LEFTBRACKET: # [ key
                    line_thickness = max(1, line_thickness - 1) # Decrease, min 1
                    #print(f'Thickness = {line_thickness}')
                elif event.key == pygame.K_RIGHTBRACKET: # ] key
                    line_thickness = min(50, line_thickness + 1) # Increase, max 50
                    #print(f'Thickness = {line_thickness}')

        # --- Drawing ---
        # Blit (copy) the canvas surface onto the main screen display
        screen.blit(canvas, (0, 0))

        # --- Update the Display ---
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128) # Added a new color
    main()