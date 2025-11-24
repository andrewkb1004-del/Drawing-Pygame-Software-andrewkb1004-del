import pygame
import os
import sys

class Button:
    """A class for creating clickable buttons in Pygame."""
    
    def __init__(self, x, y, width, height, inactive_image, active_image, tool="None", action=None):
        """
        Initializes the button object.

        :param x: The x-coordinate of the top-left corner.
        :param y: The y-coordinate of the top-left corner.
        :param width: The width of the button.
        :param height: The height of the button.
        :param inactive_image: The image to show when the mouse is not hovering above the button.
        :param active_image: The image when the mouse is hovering above the button.
        :param tool: Specify the tool associated with this button.
        :param action: The function to call when the button is clicked.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_image = pygame.transform.scale(pygame.image.load(inactive_image), (width, height))
        self.active_image = pygame.transform.scale(pygame.image.load(active_image), (width, height))
        self.action = action
        self.is_active = False
        self.tool = tool

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

    # Create a separate surface for drawing.
    canvas = pygame.Surface((screen_width, screen_height))
    canvas.fill(background_color)

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
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    eraser_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "eraser_inactive.png"), active_image=os.path.join("assets", "eraser_active.png"),
        tool="eraser",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + (button_h + button_padding)*2
    square_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "square_inactive.png"), active_image=os.path.join("assets", "square_active.png"),
        tool="square",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    rect_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "rect_inactive.png"), active_image=os.path.join("assets", "rect_active.png"),
        tool="rect",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + button_h + button_padding
    circle_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "circle_inactive.png"), active_image=os.path.join("assets", "circle_active.png"),
        tool="circle",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    oval_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "oval_inactive.png"), active_image=os.path.join("assets", "oval_active.png"),
        tool="oval",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    triangle_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "triangle_inactive.png"), active_image=os.path.join("assets", "triangle_active.png"),
        tool="triangle",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + (button_h + button_padding)*3
    quit_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "quit_inactive.png"), active_image=os.path.join("assets", "quit_active.png"),
        tool="quit",
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
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + (button_h + button_padding)*7
    save_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "save.png"), active_image=os.path.join("assets", "save.png"),
        tool="save",
        action=set_active_tool # Pass the function reference
    )
    
    button_y = button_y + button_h + button_padding
    load_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "load.png"), active_image=os.path.join("assets", "load.png"),
        tool="load",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    import_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "import.png"), active_image=os.path.join("assets", "import.png"),
        tool="import",
        action=set_active_tool # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    export_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "export.png"), active_image=os.path.join("assets", "export.png"),
        tool="export",
        action=set_active_tool # Pass the function reference
    )

    tool_buttons_list = [pen_button, eraser_button, square_button, rect_button, circle_button, oval_button, triangle_button, quit_button,
                         color_button, save_button, load_button, import_button, export_button]

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
    PURPLE = (128, 0, 128) # Added a new color
    main()