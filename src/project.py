import pygame
import os
import sys

class Button:
    """A class for creating clickable buttons in Pygame."""
    
    def __init__(self, x, y, width, height, inactive_image, active_image, tool="None", tooltip_text="", action=None):
        """
        Initializes the button object.

        :param x: The x-coordinate of the top-left corner.
        :param y: The y-coordinate of the top-left corner.
        :param width: The width of the button.
        :param height: The height of the button.
        :param inactive_image: The image to show when the mouse is not hovering above the button.
        :param active_image: The image when the mouse is hovering above the button.
        :param tool: Specify the tool associated with this button.
        :param tooltip_text: Specify the text to display when the mouse is hovering over the button.
        :param action: The function to call when the button is clicked.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_image = pygame.transform.scale(pygame.image.load(inactive_image), (width, height))
        self.active_image = pygame.transform.scale(pygame.image.load(active_image), (width, height))
        self.action = action
        self.tooltip = tooltip_text
        self.is_active = False
        self.tool = tool

        # Setup Font
        self.font = pygame.font.SysFont('Arial', 12)
        self.text_color = (0, 0, 0) # Black text

    def draw(self, screen):
        """Draws the button on the screen, changing color on hover."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state based on hover
        if self.rect.collidepoint(mouse_pos) or self.is_active:
            current_image = self.active_image
        else:
            current_image = self.inactive_image
            
        # Draw the button
        screen.blit(current_image, (self.rect.left, self.rect.top))

    def draw_tooltip(self, screen):
        """Draws the button on the screen, changing color on hover."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state based on hover
        if self.rect.collidepoint(mouse_pos):
            if self.tooltip != "":
                text_surface = self.font.render(self.tooltip, True, BLACK)
                padding = 5
                box_rect = text_surface.get_rect()
                #box_rect.topleft = (mouse_pos[0] + 20, mouse_pos[1] - 20)  # Offset from cursor
                box_rect.topright = (mouse_pos[0] + 20, mouse_pos[1] - 20)  # Offset from cursor
                box_rect.inflate_ip(padding * 2, padding * 2)

                # Draw background and border
                pygame.draw.rect(screen, TOOLTIP_BG, box_rect)
                pygame.draw.rect(screen, BLACK, box_rect, 1)
                screen.blit(text_surface, (box_rect.x + padding, box_rect.y + padding))

    def handle_event(self, event):
        """Checks for a mouse click on the button and executes the action."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the click occurred within the button area
                if self.rect.collidepoint(mouse_pos):
                    # Execute the button's action if one is defined
                    self.is_active = True
                    if self.action is not None:
                        self.action(self)
                        return True # Return True if the button was clicked
        return False # Return False otherwise

# --- Define action functions for buttons ---
def quit_program(instance):
    """Function to exit the program."""
    global running
    running = False
    print("Exiting ...")

def set_active_tool(instance):
    """Function to set pen as current active tool."""
    global active_tool
    global start_pos

    start_pos = None
    active_tool = instance.tool
    print(f"Set {active_tool} as active!")

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
    fps = 60

    # Font Setup
    font = pygame.font.SysFont('Arial', 12)

    # --- Create Button Instances ---
    edge_padding = 15
    button_padding = 10

    # Left side buttons
    button_x = edge_padding
    button_y = 50
    button_w = 50
    button_h = 50

    pen_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "pen_inactive.png"), active_image=os.path.join("assets", "pen_active.png"),
        tool="pen",
        tooltip_text="Pen",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    eraser_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "eraser_inactive.png"), active_image=os.path.join("assets", "eraser_active.png"),
        tool="eraser",
        tooltip_text="Eraser",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + (button_h + button_padding)*2
    square_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "square_inactive.png"), active_image=os.path.join("assets", "square_active.png"),
        tool="square",
        tooltip_text="Square",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    rect_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "rect_inactive.png"), active_image=os.path.join("assets", "rect_active.png"),
        tool="rect",
        tooltip_text="Rectangle",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + button_h + button_padding
    circle_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "circle_inactive.png"), active_image=os.path.join("assets", "circle_active.png"),
        tool="circle",
        tooltip_text="Circle",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    oval_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "oval_inactive.png"), active_image=os.path.join("assets", "oval_active.png"),
        tool="oval",
        tooltip_text="Oval",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    triangle_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "triangle_inactive.png"), active_image=os.path.join("assets", "triangle_active.png"),
        tool="triangle",
        tooltip_text="Triangle",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + (button_h + button_padding)*3
    quit_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "quit_inactive.png"), active_image=os.path.join("assets", "quit_active.png"),
        tool="quit",
        tooltip_text="Quit Program",
        action=quit_program # Pass the function reference
    )
    
    # Right side buttons
    button_w = 50
    button_h = 50
    button_x = screen_width - edge_padding - button_w
    button_y = 50

    color_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "color_inactive.png"), active_image=os.path.join("assets", "color_active.png"),
        tool="color bar",
        tooltip_text="Color Bar",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + (button_h + button_padding)*7
    save_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "save.png"), active_image=os.path.join("assets", "save.png"),
        tool="save",
        tooltip_text="Save",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + button_h + button_padding
    load_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "load.png"), active_image=os.path.join("assets", "load.png"),
        tool="load",
        tooltip_text="Load",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    import_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "import.png"), active_image=os.path.join("assets", "import.png"),
        tool="import",
        tooltip_text="Import",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    export_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "export.png"), active_image=os.path.join("assets", "export.png"),
        tool="export",
        tooltip_text="Export",
        action=set_active_tool # Pass the function reference
    )

    tool_buttons_list = [pen_button, eraser_button, square_button, rect_button, circle_button, oval_button, triangle_button, quit_button,
                         color_button, save_button, load_button, import_button, export_button]

    # Create a separate surface for drawing.
    canvas = pygame.Surface((screen_width, screen_height))
    canvas.fill(background_color)

    global running
    global active_tool
    global start_pos

    active_tool = "None"
    running = True
    start_pos = None # Use for square, rect, circle, oval, and triangle
    drawing = False # Flag to check if the mouse button is held down
    last_pos = None # To store the last mouse position for continuous lines
    clock = pygame.time.Clock() # To control the frame rate

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                    if event.pos[0] > edge_padding + button_w + edge_padding and event.pos[0] < screen_width - (edge_padding + button_w + edge_padding):
                        last_pos = event.pos # Start drawing from current position

            # Mouse Button Up Event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    drawing = False
                    last_pos = None # Reset last_pos when button is released

            # Mouse Motion Event
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if event.pos[0] > edge_padding + button_w + edge_padding and event.pos[0] < screen_width - (edge_padding + button_w + edge_padding):
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

            # Handling event for the buttons
            for button in tool_buttons_list:
                button.handle_event(event)

        # --- Drawing ---
        # Blit (copy) the canvas surface onto the main screen display
        screen.blit(canvas, (0, 0))

        # Draw the buttons onto the screen
        for button in tool_buttons_list:
            if button.tool != active_tool:
                button.is_active = False
            button.draw(screen)  

        # Draw tooltip over buttons
        for button in tool_buttons_list:
            button.draw_tooltip(screen)        

        # Display mouse coordinate at the bottom left of the screen
        mouse_pos = pygame.mouse.get_pos()
        mouse_coordinate_text = f"{mouse_pos[0]} , {mouse_pos[1]}"
        text_surface = font.render(mouse_coordinate_text , True, BLACK)
        screen.blit(text_surface, (15, screen_height-15))

        # --- Update the Display ---
        pygame.display.flip()

        # --- Frame Rate Control ---
        clock.tick(fps) # Limit frames per second to fps

    pygame.quit()



if __name__ == "__main__":
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    TOOLTIP_BG = (255, 255, 200)

    main()