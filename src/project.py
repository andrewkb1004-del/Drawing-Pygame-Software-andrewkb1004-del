import pygame
import os
import sys
import tkinter as tk
from tkinter import filedialog

class Layer:
    """A class for creating a layer in Pygame."""
    
    def __init__(self, x, y, width, height, background_color=None):
        """
        Initializes the layer object.

        :param x: The x-coordinate of the top-left corner to be displayed on screen.
        :param y: The y-coordinate of the top-left corner to be displayed on screen.
        :param width: The width of the layer.
        :param height: The height of the layer.
        :param background_color: The background color of this layer.  This will be set as transparent.
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = background_color
        self.is_visible = True
        self.is_current = True
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(background_color)
        self.surface.fill(background_color)

    def clear(self):
        self.surface.fill(self.bg_color)

    def draw(self, screen):
        """Draws the layer on the screen"""
        screen.blit(self.surface, (self.x, self.y))

class Button:
    """A class for creating clickable buttons in Pygame."""
    
    def __init__(self, x, y, width, height, inactive_image=None, active_image=None, inactive_color=None, active_color=None, border_color=None, text=None, text_color=None, tool="None", tooltip_text="", action=None):
        """
        Initializes the button object.

        :param x: The x-coordinate of the top-left corner.
        :param y: The y-coordinate of the top-left corner.
        :param width: The width of the button.
        :param height: The height of the button.
        :param inactive_image: The image to show when the mouse is not hovering above the button.
        :param active_image: The image when the mouse is hovering above the button.
        :param inactive_color: The color to show when the mouse is not hovering above the button. Should not use with together with image.
        :param active_color: The color when the mouse is hovering above the button. Should not use with together with image.
        :param border_color: The color of the border around the button.
        :param text: The text to displayed at the center of the button.
        :param text_color: The color of the text.
        :param tool: Specify the tool associated with this button.
        :param tooltip_text: Specify the text to display when the mouse is hovering over the button.
        :param action: The function to call when the button is clicked.
        """

        self.rect = pygame.Rect(x, y, width, height)
        if inactive_image is not None:
            self.inactive_image = pygame.transform.scale(pygame.image.load(inactive_image), (width, height))
        else:
            self.inactive_image = None
        if active_image is not None:
            self.active_image = pygame.transform.scale(pygame.image.load(active_image), (width, height))
        else:
            self.active_image = None
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.border_color = border_color
        self.text = text
        if text_color is not None:
            self.text_color = text_color
        else:
            self.text_color = (0, 0, 0) # Black text
        self.action = action
        self.tooltip = tooltip_text
        self.is_active = False
        self.tool = tool

        # Setup Font
        self.font = pygame.font.SysFont('Arial', 12)

    def draw(self, screen):
        """Draws the button on the screen, changing color on hover."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state based on hover
        if self.rect.collidepoint(mouse_pos) or self.is_active:
            current_image = self.active_image
            current_color = self.active_color
        else:
            current_image = self.inactive_image
            current_color = self.inactive_color
            
        # Draw the button
        if current_image is not None:
            screen.blit(current_image, (self.rect.left, self.rect.top))
        elif current_color is not None:
            pygame.draw.rect(screen, current_color, self.rect)

        # Draw text
        if self.text is not None:
            text_surf = self.font.render(self.text, True, self.text_color)       
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        # Draw border
        if self.border_color is not None:
            pygame.draw.rect(screen, self.border_color, self.rect, 1)


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
                    if self.is_active:
                        self.is_active = False
                    else:
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
    #print("Exiting ...")

def set_active_tool(instance):
    """Function to set current active tool."""
    global active_tool
    global start_pos

    start_pos = None
    if instance.is_active and instance.tool in ["pen", "eraser", "square", "rect", "circle", "oval", "triangle"]:
        active_tool = instance.tool
    else:
        active_tool = "None"
    #print(f"Set {active_tool} as active!")

def open_file_dialog():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")]
    )

    return file_path

def save_file_dialog():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Save file dialog
    file_path = filedialog.asksaveasfilename(
        title="Save file as",
        defaultextension=".txt",  # Default extension
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")]
    )

    return file_path

def load_file(instance):
    file_path = open_file_dialog()
    print(f"File to load is {file_path}")

def save_file(instance):
    file_path = save_file_dialog()
    print(f"File to save is {file_path}")

def import_file(instance):
    file_path = open_file_dialog()
    print(f"File to import is {file_path}")

def export_file(instance):
    file_path = save_file_dialog()
    print(f"File to export is {file_path}")
        
def set_active_color(instance):
    """Function to set current color."""
    global current_color
    current_color = instance.active_color
    #print(f"Set {instance.tooltip} as active color!")

def decrease_lw(instance):
    global line_thickness
    global shape_width
    line_thickness = max(1, line_thickness - 1) # Decrease, min 1
    if shape_width != 0:
        shape_width = line_thickness

def increase_lw(instance):
    global line_thickness
    global shape_width
    line_thickness = min(50, line_thickness + 1) # Increase, max 50
    if shape_width != 0:
        shape_width = line_thickness

def decrease_alpha(instance):
    global alpha
    alpha_pct = int(round(alpha * 100 / 255 / 5.0) * 5)
    alpha_pct = max(5, alpha_pct - 5) # Decrease, min 5%
    alpha = int(alpha_pct / 100 * 255)

def increase_alpha(instance):
    global alpha
    alpha_pct = int(round(alpha * 100 / 255 / 5.0) * 5)
    alpha_pct = min(100, alpha_pct + 5) # Increase, max 100%
    alpha = int(alpha_pct / 100 * 255)

def get_square(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]

    width = abs(x2 - x1)
    height = abs(y2 - y1)
    size = min(width, height)

    if x1 < x2:
        x = x1
    else:
        x = x1 - size

    if y1 < y2:
        y = y1
    else:
        y = y1 - size

    return pygame.Rect(x, y, size, size)

def get_rect(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]

    if x1 < x2:
        x = x1
    else:
        x = x2

    if y1 < y2:
        y = y1
    else:
        y = y2

    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(x, y, width, height)

def get_circle(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]

    width = abs(x2 - x1)
    height = abs(y2 - y1)
    size = min(width, height)
    radius = size // 2

    if x1 < x2:
        x = x1 + radius
    else:
        x = x1 - radius

    if y1 < y2:
        y = y1 + radius
    else:
        y = y1 - radius

    return x, y, radius

def get_triangle(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]
    return ((x1, y1), (x1+(x2-x1)//2, y2), (x2,y1))

def create_left_buttons(edge_padding, button_padding, button_w, button_h):
    # --- Create left side buttons ---
    button_x = edge_padding
    button_y = 50

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

    global tool_buttons_list
    tool_buttons_list.extend([pen_button, eraser_button, square_button, rect_button, circle_button, oval_button, triangle_button, quit_button])    

def create_right_buttons(edge_padding, button_padding, button_w, button_h, screen_width):
    # --- Create right side buttons ---
    button_x = screen_width - edge_padding - button_w
    button_y = 50

    # color_button = Button(
    #    x=button_x, y=button_y, width=button_w, height=button_h,
    #    inactive_image=os.path.join("assets", "color_inactive.png"), active_image=os.path.join("assets", "color_active.png"),
    #    tool="color wheel",
    #    tooltip_text="Color Wheel",
    #    action=set_active_tool # Pass the function reference
    #)
    
    button_y = button_y + (button_h + button_padding)*6
    save_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "save.png"), active_image=os.path.join("assets", "save.png"),
        tool="save",
        tooltip_text="Save",
        action=save_file # Pass the function reference
    )
    
    button_y = button_y + button_h + button_padding
    load_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "load.png"), active_image=os.path.join("assets", "load.png"),
        tool="load",
        tooltip_text="Load",
        action=load_file # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    import_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "import.png"), active_image=os.path.join("assets", "import.png"),
        tool="import",
        tooltip_text="Import",
        action=import_file # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    export_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "export.png"), active_image=os.path.join("assets", "export.png"),
        tool="export",
        tooltip_text="Export",
        action=export_file # Pass the function reference
    )

    global misc_buttons_list
    # misc_buttons_list.extend([color_button, save_button, load_button, import_button, export_button])
    misc_buttons_list.extend([save_button, load_button, import_button, export_button])

def create_color_buttons(x_edge_padding, y_edge_padding, button_padding, button_w, button_h, screen_height):
    # --- Create color buttons at the bottom side ---
    button_x = x_edge_padding + 35 + x_edge_padding + (button_w + button_padding)*2
    button_y = screen_height - button_h - y_edge_padding

    colors = {
        "Eraser" : TRANSPARENT_BG,
        "Black"  : BLACK,
        "Gray"   : GRAY,
        "Silver" : SILVER,
        "White"  : WHITE,
        "Pink"   : PINK,
        "Red"    : RED,
        "Orange" : ORANGE,
        "Yellow" : YELLOW,
        "Green"  : GREEN,
        "Cyan"   : CYAN,
        "Blue"   : BLUE,
        "Indigo" : INDIGO,
        "Violet" : VIOLET,
        "Purple" : PURPLE,
        "Magenta": MAGENTA,
        "Maroon" : MAROON,
        "Brown"  : BROWN,
        "Peach"  : PEACH,
        "Gold"   : GOLD,
        "Lime"   : LIME,
        "Forest" : FOREST,
        "Aqua"   : AQUA,
    }

    global color_buttons_list
    for tooltip, color in colors.items():
        tmp_button = Button(
            x=button_x, y=button_y, width=button_w, height=button_h,
            inactive_color=color, active_color=color,
            border_color=BLACK,
            tool="color",
            tooltip_text=tooltip,
            action=set_active_color
        )
        color_buttons_list.append((tmp_button))
        button_x = button_x + button_w + button_padding
    
def create_lw_a_buttons(x_edge_padding, y_edge_padding, button_padding, button_w, button_h, screen_width, screen_height, lw, alpha):
    # --- Create the line_width and alpha buttons at the bottom right corner---
    button_x = screen_width - x_edge_padding - (button_w + button_padding)*14
    button_y = screen_height - button_h - y_edge_padding

    lw_label_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SCREEN_BG, active_color=SCREEN_BG,
        border_color=SCREEN_BG,
        text="LW:"
    )
    button_x = button_x + button_w + button_padding
    lw_minus_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SCREEN_BG,
        border_color=BLACK,
        text="-",
        tooltip_text="Decrease line width",
        action=decrease_lw
    )
    button_x = button_x + button_w + button_padding
    global lw_value_button
    lw_value_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SILVER,
        border_color=BLACK,
        text=f"{lw}"
    )
    button_x = button_x + button_w + button_padding
    lw_plus_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SCREEN_BG,
        border_color=BLACK,
        text="+",
        tooltip_text="Increase line width",
        action=increase_lw
    )

    button_x = screen_width - x_edge_padding - (button_w + button_padding)*7
    alpha_label_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SCREEN_BG, active_color=SCREEN_BG,
        border_color=SCREEN_BG,
        text="Alpha:"
    )
    button_x = button_x + button_w + button_padding
    alpha_minus_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SCREEN_BG,
        border_color=BLACK,
        text="-",
        tooltip_text="Decrease line width",
        action=decrease_alpha
    )
    button_x = button_x + button_w + button_padding
    global alpha_value_button
    alpha_percent = int(round(alpha * 100 / 255))
    alpha_value_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SILVER,
        border_color=BLACK,
        text=f"{alpha_percent}%"
    )
    button_x = button_x + button_w + button_padding
    alpha_plus_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_color=SILVER, active_color=SCREEN_BG,
        border_color=BLACK,
        text="+",
        tooltip_text="Increase line width",
        action=increase_alpha
    )

    global lw_a_buttons_list
    lw_a_buttons_list.extend([lw_label_button, lw_minus_button, lw_value_button, lw_plus_button, 
                              alpha_label_button, alpha_minus_button, alpha_value_button, alpha_plus_button])


def draw_shape(active_tool, layer, draw_color, start_pos, current_pos, shape_width):
    if active_tool == "square":
        pygame.draw.rect(layer, draw_color, get_square(start_pos, current_pos), shape_width)
    elif active_tool == "rect":
        pygame.draw.rect(layer, draw_color, get_rect(start_pos, current_pos), shape_width)
    elif active_tool == "circle":
        x, y , radius = get_circle(start_pos, current_pos)
        pygame.draw.circle(layer, draw_color, (x, y), radius, shape_width)
    elif active_tool == "oval":
        pygame.draw.ellipse(layer, draw_color, get_rect(start_pos, current_pos), shape_width)
    elif active_tool == "triangle":
        pygame.draw.polygon(layer, draw_color, get_triangle(start_pos, current_pos), shape_width)

def is_pos_in_canvas(pos, canvas_rect):
    if canvas_rect.collidepoint(pos):
        return True
    else:
        return False

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
        screen_width = 1600
        screen_height = 900
        resolution = (screen_width, screen_height)
        screen = pygame.display.set_mode(resolution)

    global line_thickness
    line_thickness = 2 # Initial brush size
    global alpha
    alpha = 255
    global current_color
    current_color = BLACK # Default drawing color
    fps = 60

    edge_padding = 15
    button_padding = 10
    button_w = 50
    button_h = 50
    x_canvas_border_width = edge_padding + button_w + edge_padding

    global tool_buttons_list
    tool_buttons_list = []
    create_left_buttons(edge_padding, button_padding, button_w, button_h)

    global misc_buttons_list
    misc_buttons_list = []
    create_right_buttons(edge_padding, button_padding, button_w, button_h, screen_width)

    global color_buttons_list
    color_buttons_list = []
    color_button_w = 30
    color_button_h = 30
    create_color_buttons(edge_padding, edge_padding, button_padding, color_button_w, color_button_h, screen_height)

    current_color_button = Button(
        x=x_canvas_border_width, y=screen_height - color_button_h - edge_padding, width=color_button_w*1.5, height=color_button_h,
        inactive_color=current_color, active_color=current_color,
        border_color=BLACK,
        tool="color",
        tooltip_text="Current Color",
    )

    global lw_a_buttons_list
    lw_a_buttons_list = []
    create_lw_a_buttons(edge_padding, edge_padding, 0, color_button_w, color_button_h, screen_width, screen_height, line_thickness, alpha)
    
    y_canvas_border_width = edge_padding * 2 + color_button_h
    canvas_width = screen_width - x_canvas_border_width*2
    canvas_height = screen_height - y_canvas_border_width
    canvas_rect = pygame.Rect(x_canvas_border_width, 0, canvas_width, canvas_height)

    # Create 1st drawing layer
    layer0 = Layer(
        x=x_canvas_border_width,
        y=0,
        width=canvas_width,
        height=canvas_height,
        background_color=TRANSPARENT_BG
    )

    # Create a surface to draw temp shapes
    tmp_layer = Layer(
        x=x_canvas_border_width,
        y=0,
        width=canvas_width,
        height=canvas_height,
        background_color=TRANSPARENT_BG
    )

    layers_list = [layer0]
    current_layer = layer0

    global running
    global active_tool
    global start_pos

    active_tool = "None"
    running = True
    start_pos = None # Use for square, rect, circle, oval, and triangle
    mouse_button_down = False # Flag to check if the mouse button is held down
    last_pos = None # To store the last mouse position for continuous lines
    clock = pygame.time.Clock() # To control the frame rate
    start_pos = None # Use for square, rect, circle, oval, and triangle
    global shape_width
    shape_width = 0  # Set to 0 to have the shape filled. Set to non-zero to specify the line width of the shape edges
    eraser_color = TRANSPARENT_BG
    current_layer_history = []

    while running:
        screen.fill(SCREEN_BG)                            # Fill the entire screen with SCREEN_BG color (e.g. gray)
        pygame.draw.rect(screen, CANVAS_BG, canvas_rect)  # Fill just the canvas area with CANVAS_BG color (e.g. white)

        if active_tool == "eraser":
            draw_color = eraser_color
        else:
            draw_color = current_color

        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_button_down = True
                    if is_pos_in_canvas(event.pos, canvas_rect):
                        last_pos = (event.pos[0] - x_canvas_border_width, event.pos[1]) # Start drawing from current position

                        # This section of code draws the shape for the click, release, click operation
                        if active_tool in ["square", "rect", "circle", "oval", "triangle"]:
                            if start_pos is None:
                                start_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                            else:
                                tmp_layer.clear()
                                current_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                                draw_shape(active_tool, current_layer.surface, draw_color, start_pos, current_pos, shape_width)
                                start_pos = None

            # Mouse Button Up Event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    mouse_button_down = False
                    last_pos = None # Reset last_pos when button is released

                    # This section of code draws the shape for the click, drag, release operation
                    current_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                    if active_tool in ["square", "rect", "circle", "oval", "triangle"] and start_pos is not None and current_pos != start_pos:
                        tmp_layer.clear()
                        draw_shape(active_tool, current_layer.surface, draw_color, start_pos, current_pos, shape_width)
                        start_pos = None

            # Mouse Motion Event
            if event.type == pygame.MOUSEMOTION:
                if active_tool in ["pen", "eraser"]:
                    if mouse_button_down:
                        if is_pos_in_canvas(event.pos, canvas_rect):
                            current_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                            if last_pos:
                                # Draw a line from the last position to the current position
                                # This makes the drawing smooth rather than just dots
                                pygame.draw.line(current_layer.surface, draw_color, last_pos, current_pos, line_thickness)
                            last_pos = current_pos # Update last_pos for the next segment
                
                # Follow the mouse movement and draw the shape and tmp_layer
                elif active_tool in ["square", "rect", "circle", "oval", "triangle"] and start_pos is not None:
                    tmp_layer.clear()
                    current_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                    if draw_color != eraser_color:
                        tmp_draw_color = draw_color
                        tmp_shape_width = shape_width
                    else:
                        tmp_draw_color = BLACK
                        tmp_shape_width = 1
                    draw_shape(active_tool, tmp_layer.surface, tmp_draw_color, start_pos, current_pos, tmp_shape_width)

            # Keyboard Events
            if event.type == pygame.KEYDOWN:
                # Clear Screen
                if event.key == pygame.K_c:
                    current_layer.clear()

                # Toggle shape fill
                elif event.key == pygame.K_f:
                    if shape_width == 0:
                        shape_width = line_thickness
                    else:
                        shape_width = 0

                # Add a layer
                elif event.key == pygame.K_EQUALS:
                    new_layer = Layer(
                        x=x_canvas_border_width,
                        y=0,
                        width=canvas_width,
                        height=canvas_height,
                        background_color=TRANSPARENT_BG
                    )
                    layers_list.append(new_layer)
                    current_layer_history.append(current_layer)
                    current_layer = new_layer

                # Delete current layer
                elif event.key == pygame.K_MINUS:
                    if len(layers_list) > 1:
                        layers_list.remove(current_layer)
                        current_layer = current_layer_history.pop() # Assign previous active layer to current_layer

                # Change Brush Size
                elif event.key == pygame.K_LEFTBRACKET: # [ key
                    line_thickness = max(1, line_thickness - 1) # Decrease, min 1
                    if shape_width != 0:
                        shape_width = line_thickness
                elif event.key == pygame.K_RIGHTBRACKET: # ] key
                    line_thickness = min(50, line_thickness + 1) # Increase, max 50
                    if shape_width != 0:
                        shape_width = line_thickness

            # Handling event for the buttons
            for button in tool_buttons_list + misc_buttons_list + color_buttons_list + lw_a_buttons_list:
                button.handle_event(event)

        # --- Drawing ---
        # Draw layers
        for layer in layers_list:
            if layer == current_layer:
                layer.is_current = True
            else:
                layer.is_current = False
            layer.draw(screen)

        tmp_layer.draw(screen)

        # Draw the buttons onto the on screen
        for button in tool_buttons_list:
            if button.tool != active_tool:
                button.is_active = False
            button.draw(screen)  

        for button in misc_buttons_list + color_buttons_list:
            button.draw(screen)

        lw_value_button.text=f"{line_thickness}"
        for button in lw_a_buttons_list:
            button.is_active = False
            button.draw(screen)

        alpha_percent = int(round(alpha * 100 / 255))
        alpha_value_button.text=f"{alpha_percent}%"
        for button in lw_a_buttons_list:
            button.is_active = False
            button.draw(screen)

        # Draw the current color
        current_color_button.active_color = current_color_button.inactive_color = current_color
        current_color_button.draw(screen)

        # Draw the button section texts on the screen
        font = pygame.font.SysFont('Arial', 18, bold=True)
        # Left side
        screen.blit(font.render("Tools"  , True, BLACK), (edge_padding, 50-25))
        screen.blit(font.render("Shapes" , True, BLACK), (edge_padding, 50-25+(button_h+button_padding)*3))
        # Right side
        # screen.blit(font.render("Color"  , True, BLACK), (screen_width - edge_padding - button_w, 50-25))
        screen.blit(font.render("Layers" , True, BLACK), (screen_width - edge_padding - button_w, 50-25))
        screen.blit(font.render("File"   , True, BLACK), (screen_width - edge_padding - button_w, 50-30+(button_h+button_padding)*6))

        # Display mouse coordinate at the bottom left of the screen
        mouse_pos = pygame.mouse.get_pos()
        mouse_coordinate_text = f"{mouse_pos[0]- x_canvas_border_width} , {mouse_pos[1]}"
        font = pygame.font.SysFont('Arial', 12)
        mouse_coor_surface = font.render(mouse_coordinate_text , True, BLACK)
        screen.blit(mouse_coor_surface, (15, screen_height-15))

        # Draw button tooltip on the screen
        for button in tool_buttons_list + misc_buttons_list + color_buttons_list + lw_a_buttons_list:
            button.draw_tooltip(screen)        
        current_color_button.draw_tooltip(screen)

        # --- Update the Display ---
        pygame.display.flip()

        # --- Frame Rate Control ---
        clock.tick(fps) # Limit frames per second to fps

    pygame.quit()



if __name__ == "__main__":
    # Define some colors
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    SILVER = (192, 192, 192)
    WHITE = (255, 255, 255)
    PINK = (255, 192, 203)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    INDIGO = (115, 0, 200)
    VIOLET = (127, 0, 255)
    PURPLE = (175, 0, 175)
    MAGENTA = (224, 51, 159)
    MAROON = (184, 18, 56)
    BROWN = (150, 75, 0)
    PEACH = (255, 229, 180)
    GOLD = (212, 175, 55)
    LIME = (191, 255, 55)
    FOREST = (1, 142, 32)
    AQUA = (0, 148, 148)
    CANVAS_BG = WHITE
    SCREEN_BG = GRAY
    TOOLTIP_BG = (255, 255, 200)
    TRANSPARENT_BG = (255, 254, 253)

    ## To open file dialogue
    # selected_file = load_file
    # if selected_file:
    #    print(f"Selected file: {selected_file}")
    # else:
    #    print("No file selected.")

    main()
