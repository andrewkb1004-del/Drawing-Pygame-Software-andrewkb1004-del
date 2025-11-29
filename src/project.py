import pygame
from pygame._sdl2.video import Window
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

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
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.set_colorkey(background_color)
        self.surface.fill(background_color)
        self.eye_button = None
        self.layer_button = None

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
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
            self.text_color = BLACK
        self.action = action
        self.tooltip = tooltip_text
        self.is_active = False
        self.tool = tool
        self.use_active_on_hover = True # When True, display active image/color when mouse hovers over button.  Otherwise, which image/color to display depends on self.is_active

        # Setup Font
        self.font = pygame.font.SysFont('Arial', 12)

    def draw(self, screen):
        """Draws the button on the screen, changing color on hover."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state based on hover
        if (self.use_active_on_hover and self.rect.collidepoint(mouse_pos)) or self.is_active:
            current_image = self.active_image
            current_color = self.active_color
        else:
            current_image = self.inactive_image
            current_color = self.inactive_color
            
        # Draw the button
        if current_image is not None:
            screen.blit(current_image, (self.x, self.y))
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

def add_layer(instance):
    """Function to add a layer."""
    global current_layer
    global layer_label_cnt
    if len(layers_list) < 10:
        layerN = layers_list[len(layers_list)-1]
        layerN_eye_button = layerN.eye_button
        button_x = layerN_eye_button.x
        button_y = layerN_eye_button.y
        button_w = layerN_eye_button.width
        button_h = layerN_eye_button.height
        new_layer = Layer(
            x=layerN.x,
            y=layerN.y,
            width=layerN.width,
            height=layerN.height,
            background_color=layerN.bg_color
        )

        eye_button = Button(
            x=button_x, y=button_y+button_h, width=button_w, height=button_h,
            inactive_image=os.path.join("assets", "layer_hidden.png"), active_image=os.path.join("assets", "layer_shown.png"),
            border_color=BLACK,
        )
        eye_button.use_active_on_hover = False
        layer_button = Button(
            x=button_x+button_w, y=button_y+button_h, width=button_w, height=button_h,
            inactive_color=SCREEN_BG, active_color=SILVER,
            border_color=BLACK,
            text=f"{layer_label_cnt}",
            tooltip_text="Set as current layer",
            action=set_current_layer
        )
        layer_label_cnt += 1

        if new_layer.is_visible:
            eye_button.is_active = True
        new_layer.eye_button=eye_button
        new_layer.layer_button=layer_button

        layer_buttons_list.extend([eye_button, layer_button])
        layers_list.append(new_layer)
        current_layer_history.append(current_layer)
        current_layer = new_layer

def delete_layer(instance):
    """Function to delete a layer."""
    global current_layer

    if len(layers_list) > 1:
        # Remove the current_layer associated buttons from the buttons list
        layer_buttons_list.remove(current_layer.eye_button)
        layer_buttons_list.remove(current_layer.layer_button)

        # Remove all occurences of current_layer from history
        # Iterate in reverse to avoid skipping elements
        for i in range(len(current_layer_history) - 1, -1, -1):
            if current_layer_history[i] == current_layer:
                del current_layer_history[i]

        # Remove current_layer from the layers list
        layers_list.remove(current_layer)

        # Assign previous current_layer to current_layer
        try:
            current_layer = current_layer_history.pop()
        except:
            current_layer = layers_list[0]

def move_layer_up(instance):
    """Function to move layer up to make it more visible."""
    global current_layer
    if len(layers_list) > 1:
        current_idx = layers_list.index(current_layer)
        layers_list.insert(current_idx+1, layers_list.pop(current_idx))

def move_layer_down(instance):
    """Function to move layer up to make it more visible."""
    global current_layer
    if len(layers_list) > 1:
        current_idx = layers_list.index(current_layer)
        layers_list.insert(current_idx-1, layers_list.pop(current_idx))

def set_current_layer(instance):
    """ Function to set current layer """
    global current_layer
    #print(f"Current layer is {current_layer.layer_button.text}")
    for layer in layers_list:
        if layer.layer_button == instance:
            current_layer = layer
            break
    #print(f"Current layer is changed to {current_layer.layer_button.text}")

def open_file_dialog(filetypes=None):
    global window

    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    if filetypes is None:
        filetypes = pygame_supported_filetypes

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=filetypes,
    )
    root.destroy()
    window.focus()
    return file_path

def save_file_dialog(title="Save file as", filetypes=None):
    global window

    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Save file dialog
    if filetypes is None:
        filetypes = pygame_supported_filetypes
    file_path = filedialog.asksaveasfilename(
        title=title,
        defaultextension=".tiff",  # Default extension
        filetypes=filetypes,
    )
    root.destroy()
    window.focus()
    return file_path

def load_from_multipage_tif(file_path):
    #print("load from multipage-tiff")

    global layers_list
    global layer_label_cnt
    global layer_buttons_list
    global current_layer_history
    global current_layer

    layer0 = layers_list[0]
    layer0_eye_button = layer0.eye_button
    layer0_x = layer0.x
    layer0_y = layer0.y
    layer0_w = layer0.width
    layer0_h = layer0.height
    layer0_bg = layer0.bg_color
    button_x = layer0_eye_button.x
    button_y = layer0_eye_button.y
    button_w = layer0_eye_button.width
    button_h = layer0_eye_button.height

    layers_list = []
    layer_label_cnt = 1
    layer_buttons_list = []
    current_layer_history = []

    # Load the tiff pages into the pil_images array
    with Image.open(file_path) as img:
        try:
            page = 0
            while True:
                pil_page = img.convert("RGBA")  # Convert each page to RGBA to preserve alpha if present
                pil_img = pil_page.copy()
                size = pil_img.size  # (width, height)
                raw = pil_img.tobytes("raw", "RGBA")
                surf = pygame.image.fromstring(raw, size, "RGBA").convert_alpha()  # Create a pygame surface with per-pixel alpha
                pil_img.close()

                new_layer = Layer(
                    x=layer0_x,
                    y=layer0_y,
                    width=layer0_w,
                    height=layer0_h,
                    background_color=layer0_bg
                )
                new_layer.surface.blit(surf, (0,0))

                eye_button = Button(
                    x=button_x, y=button_y, width=button_w, height=button_h,
                    inactive_image=os.path.join("assets", "layer_hidden.png"), active_image=os.path.join("assets", "layer_shown.png"),
                    border_color=BLACK,
                )
                eye_button.use_active_on_hover = False
                layer_button = Button(
                    x=button_x+button_w, y=button_y, width=button_w, height=button_h,
                    inactive_color=SCREEN_BG, active_color=SILVER,
                    border_color=BLACK,
                    text=f"{layer_label_cnt}",
                    tooltip_text="Set as current layer",
                    action=set_current_layer
                )
                layer_label_cnt += 1
                button_y += button_h

                if new_layer.is_visible:
                    eye_button.is_active = True
                new_layer.eye_button=eye_button
                new_layer.layer_button=layer_button

                layer_buttons_list.extend([eye_button, layer_button])
                layers_list.append(new_layer)

                page += 1
                img.seek(page)  # Move to next page in the tiff file
        except EOFError:
            # no more pages
            pass

        current_layer = layers_list[len(layers_list) - 1]


def load_file(instance):
    file_path = open_file_dialog()
    #print(f"File to load is {file_path}")

    global layers_list
    global layer_buttons_list
    global current_layer
    global layer_label_cnt
    global current_layer_history

    if file_path != "":
        response = messagebox.askokcancel(title="Confirmation", message="You will loose current progress. Do you want to proceed?")
        if not response:
            return False

        if os.access(file_path, os.R_OK):
            base, ext = os.path.splitext(file_path)
            if ext.lower() == ".tiff":
                #print("saving to multipage-tif")
                load_from_multipage_tif(file_path)
                return True
            else:
                try:
                    # Load the image into the 1st layer and then remove the other layers
                    image = pygame.image.load(file_path).convert_alpha()
                    layers_list[0].clear()
                    layers_list[0].surface.blit(image, (0,0))
                    layers_list[0].layer_button.text = "1"
                    layer_label_cnt = 2  # When we create a new layer, this is the name of it.
                    current_layer = layers_list[0]
                    layers_list = [layers_list[0]]  # Keep only the 1st layer.  Remove the rest.
                    layer_buttons_list = [layers_list[0].eye_button, layers_list[0].layer_button] # Keep only the buttons associated with the 1st layer
                    current_layer_history = [] # Reset the current_layer history
                    return True
                except:
                    messagebox.showerror(title="Error", message=f"Couldn't load from {file_path}.")
        else:
            messagebox.showerror(title="Error", message=f"{file_path} is not readable.")
    return False

def save_to_multipage_tif(file_path):
    #print("saving to multipage-tif")
    pil_images = []
    for layer in layers_list:
        size = layer.surface.get_size()
        has_alpha = layer.surface.get_flags() & pygame.SRCALPHA
        if has_alpha:
            # Get raw RGBA bytes from the surface
            raw_str = pygame.image.tostring(layer.surface, "RGBA", False)
            pil_img = Image.frombytes("RGBA", size, raw_str)
        else:
            # No alpha: get RGB bytes
            raw_str = pygame.image.tostring(layer.surface, "RGB", False)
            pil_img = Image.frombytes("RGB", size, raw_str).convert("RGBA")
        pil_images.append(pil_img)

    first, rest = pil_images[0], pil_images[1:]
    save_kwargs = {"format": "TIFF", "save_all": True, "append_images": rest}
    save_kwargs["compression"] = "tiff_deflate"

    first.save(file_path, **save_kwargs)
    # Close PIL images
    for im in pil_images:
        im.close()
    return True

def save_file(instance):
    file_path = save_file_dialog(title="Save file as (Hint: Save to TIFF to preserve layers)")
    #print(f"File to save is {file_path}")

    if file_path != "":
        base, ext = os.path.splitext(file_path)
        if ext.lower() == ".tiff":
            save_to_multipage_tif(file_path)
            return True
        else:
            tmp_surface = pygame.Surface((layers_list[0].width, layers_list[0].height), pygame.SRCALPHA)
            for layer in layers_list:
                if layer.is_visible:
                    tmp_surface.blit(layer.surface, (0,0))
            try:
                pygame.image.save(tmp_surface, file_path)
                return True
            except:
                messagebox.showerror(title="Error", message=f"Couldn't save to {file_path}")
    return False

def import_file(instance):
    global current_layer

    # pygame can't import tiff file that it creates.  Removing it from the supported filetype list.
    mod_filetypes = []
    for x in pygame_supported_filetypes:
        if x != ("TIFF files", "*.tiff"):
            mod_filetypes.append(x)
            
    file_path = open_file_dialog(filetypes=mod_filetypes)
    #print(f"File to import is {file_path}")

    if file_path != "":
        if os.access(file_path, os.R_OK):
            try:
                image = pygame.image.load(file_path).convert_alpha()
                current_layer.surface.blit(image, (0,0))
                return True
            except:
                messagebox.showerror(title="Error", message=f"Couldn't import from {file_path}")
        else:
            messagebox.showerror(title="Error", message=f"{file_path} is not readable.")
    return False

def export_file(instance):
    global current_layer

    # pygame can't import tiff file that it creates.  Removing it from the supported filetype list.
    mod_filetypes = []
    for x in pygame_supported_filetypes:
        if x != ("TIFF files", "*.tiff"):
            mod_filetypes.append(x)
            
    file_path = save_file_dialog(filetypes=mod_filetypes)
    #print(f"File to export is {file_path}")

    if file_path != "":
        try:
            pygame.image.save(current_layer.surface, file_path)
            return True
        except:
            messagebox.showerror(title="Error", message=f"Couldn't export to {file_path}.")
    return False

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

    button_y = button_y + (button_h + button_padding)*5
    quit_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "quit_inactive.png"), active_image=os.path.join("assets", "quit_active.png"),
        tool="quit",
        tooltip_text="Quit Program",
        action=quit_program # Pass the function reference
    )

    tool_buttons_list.extend([pen_button, eraser_button, square_button, rect_button, circle_button, oval_button, triangle_button, quit_button])    

def create_right_buttons(edge_padding, button_padding, button_w, button_h, screen_width):
    # --- Create right side buttons ---
    button_x = screen_width - edge_padding - button_w
    button_y = 50

    button_y = button_y + (button_h + button_padding)*8
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
        tooltip_text="Import image into current layer",
        action=import_file # Pass the function reference
    )

    button_y = button_y + button_h + button_padding
    export_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "export.png"), active_image=os.path.join("assets", "export.png"),
        tool="export",
        tooltip_text="Export current layer to image",
        action=export_file # Pass the function reference
    )

    misc_buttons_list.extend([save_button, load_button, import_button, export_button])

def create_layer_buttons(edge_padding, button_padding, button_w, button_h, screen_width, layers_list):
    # --- Create right side buttons ---
    button_x = screen_width - edge_padding - button_w - 25
    button_y = 50

    add_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "add_layer_inactive.png"), active_image=os.path.join("assets", "add_layer_active.png"),
        border_color=BLACK,
        tooltip_text="Add layer",
        action=add_layer
    )
    delete_button = Button(
        x=button_x+button_w, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "delete_layer_inactive.png"), active_image=os.path.join("assets", "delete_layer_active.png"),
        border_color=BLACK,
        tooltip_text="Remove layer",
        action=delete_layer
    )

    button_y = button_y + (button_h + button_padding)
    up_button = Button(
        x=button_x, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "up_arrow_inactive.png"), active_image=os.path.join("assets", "up_arrow_active.png"),
        border_color=BLACK,
        tooltip_text="Move layer up",
        action=move_layer_up
    )
    down_button = Button(
        x=button_x+button_w, y=button_y, width=button_w, height=button_h,
        inactive_image=os.path.join("assets", "down_arrow_inactive.png"), active_image=os.path.join("assets", "down_arrow_active.png"),
        border_color=BLACK,
        tooltip_text="Move layer up",
        action=move_layer_down
    )
    layer_func_buttons_list.extend([add_button, delete_button, up_button, down_button])

    button_y = button_y + (button_h + button_padding)

    global layer_button_start_info
    layer_button_start_info = (button_x, button_y, button_w, button_h)
    global layer_label_cnt
    layer_label_cnt = 1
    for layer in layers_list:
        eye_button = Button(
            x=button_x, y=button_y, width=button_w, height=button_h,
            inactive_image=os.path.join("assets", "layer_hidden.png"), active_image=os.path.join("assets", "layer_shown.png"),
            border_color=BLACK,
        )
        eye_button.use_active_on_hover = False

        layer_button = Button(
            x=button_x+button_w, y=button_y, width=button_w, height=button_h,
            inactive_color=SCREEN_BG, active_color=SILVER,
            border_color=BLACK,
            text=f"{layer_label_cnt}",
            tooltip_text="Set as current layer",
            action=set_current_layer
        )
        
        if layer.is_visible:
            eye_button.is_active = True

        layer.eye_button=eye_button
        layer.layer_button=layer_button
        layer_buttons_list.extend([eye_button, layer_button])

        layer_label_cnt = layer_label_cnt + 1
        button_y = button_y + button_h


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
        "Sky"    : SKY,
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

    lw_a_buttons_list.extend([lw_label_button, lw_minus_button, lw_value_button, lw_plus_button, 
                              alpha_label_button, alpha_minus_button, alpha_value_button, alpha_plus_button])


def draw_shape(active_tool, layer, draw_color, start_pos, current_pos, shape_width):
    tmp_surface = pygame.Surface((layer.get_width(), layer.get_height()), pygame.SRCALPHA)
    if active_tool == "square":
        pygame.draw.rect(tmp_surface, draw_color, get_square(start_pos, current_pos), shape_width)
    elif active_tool == "rect":
        pygame.draw.rect(tmp_surface, draw_color, get_rect(start_pos, current_pos), shape_width)
    elif active_tool == "circle":
        x, y , radius = get_circle(start_pos, current_pos)
        pygame.draw.circle(tmp_surface, draw_color, (x, y), radius, shape_width)
    elif active_tool == "oval":
        pygame.draw.ellipse(tmp_surface, draw_color, get_rect(start_pos, current_pos), shape_width)
    elif active_tool == "triangle":
        pygame.draw.polygon(tmp_surface, draw_color, get_triangle(start_pos, current_pos), shape_width)
    layer.blit(tmp_surface, (0, 0))

def is_pos_in_canvas(pos, canvas_rect):
    if canvas_rect.collidepoint(pos):
        return True
    else:
        return False


### Main program ######
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
SKY = (0, 186, 255)
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

# Get the Pygame window object
window = Window.from_display_module()

pygame_supported_filetypes = [("TIFF files", "*.tiff"), ("BMP files", "*.bmp"), ("GIF files", "*.gif"), ("JPEG files", "*.jpg"), ("PNG Files", "*.png"), ("All Files", "*.*")]

line_thickness = 2 # Initial brush size
alpha = 255
current_color = BLACK # Default drawing color
fps = 60
edge_padding = 15
button_padding = 10
button_w = 50
button_h = 50
x_canvas_border_width = edge_padding + button_w + edge_padding

tool_buttons_list = []
create_left_buttons(edge_padding, button_padding, button_w, button_h)

misc_buttons_list = []
create_right_buttons(edge_padding, button_padding, button_w, button_h, screen_width)

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

layer_buttons_list = []
layer_func_buttons_list = []
create_layer_buttons(edge_padding, button_padding, button_w//2*1.3, button_h//2*1.3, screen_width, layers_list)

active_tool = "None"
running = True
start_pos = None # Use for square, rect, circle, oval, and triangle
mouse_button_down = False # Flag to check if the mouse button is held down
last_pos = None # To store the last mouse position for continuous lines
clock = pygame.time.Clock() # To control the frame rate
start_pos = None # Use for square, rect, circle, oval, and triangle
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
                            draw_shape(active_tool, current_layer.surface, draw_color+(alpha,), start_pos, current_pos, shape_width)
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
                    draw_shape(active_tool, current_layer.surface, draw_color+(alpha,), start_pos, current_pos, shape_width)
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
                            tmp_surface = pygame.Surface((current_layer.surface.get_width(), current_layer.surface.get_height()), pygame.SRCALPHA)
                            pygame.draw.line(tmp_surface, draw_color+(alpha,), last_pos, current_pos, line_thickness)
                            current_layer.surface.blit(tmp_surface, (0, 0))
                        last_pos = current_pos # Update last_pos for the next segment
            
            # Follow the mouse movement and draw the shape and tmp_layer
            elif active_tool in ["square", "rect", "circle", "oval", "triangle"] and start_pos is not None:
                tmp_layer.clear()
                tmp_layer.surface.blit(current_layer.surface, (0,0))
                current_pos = (event.pos[0] - x_canvas_border_width, event.pos[1])
                if draw_color != eraser_color:
                    tmp_draw_color = draw_color
                    tmp_shape_width = shape_width
                else:
                    tmp_draw_color = BLACK
                    tmp_shape_width = 1
                draw_shape(active_tool, tmp_layer.surface, tmp_draw_color+(alpha,), start_pos, current_pos, tmp_shape_width)

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

            # Cancel drawing operation
            elif event.key == pygame.K_ESCAPE:
                start_pos = None
                tmp_layer.clear()

            # Change line thickness
            elif event.key == pygame.K_LEFTBRACKET: # [ key
                line_thickness = max(1, line_thickness - 1) # Decrease, min 1
                if shape_width != 0:
                    shape_width = line_thickness
            elif event.key == pygame.K_RIGHTBRACKET: # ] key
                line_thickness = min(50, line_thickness + 1) # Increase, max 50
                if shape_width != 0:
                    shape_width = line_thickness

        # Handling event for the buttons
        for button in tool_buttons_list + misc_buttons_list + layer_buttons_list + layer_func_buttons_list + color_buttons_list + lw_a_buttons_list:
            button.handle_event(event)

    # Draw layers
    for layer in layers_list:
        # keep layer.is_current and layer.layer_button.is_active in sync with current_layer
        if layer == current_layer:
            layer.is_current = True
            layer.layer_button.is_active = True
            layer.layer_button.text_color = RED
        else:
            layer.is_current = False
            layer.layer_button.is_active = False
            layer.layer_button.text_color = BLACK

        # keep layer.is_visible in sync with layer.eye_button.is_active, just in case the button status was changed by the event loop 
        if layer.eye_button.is_active:
            layer.is_visible = True
            layer.draw(screen)
        else:
            layer.is_visible = False

    tmp_layer.draw(screen)

    x, y, w, h = layer_button_start_info
    for i in range(len(layers_list) - 1, -1, -1):
        layer = layers_list[i]
        # Set the buttons position according to the layer order in layers_list.  Do this in reverse order so that we start with the buttons for last drawn layer 
        layer.eye_button.x = x
        layer.eye_button.y = y
        layer.eye_button.rect = pygame.Rect(x, y, w, h)
        layer.layer_button.x = x+w
        layer.layer_button.y = y
        layer.layer_button.rect = pygame.Rect(x+w, y, w, h)
        y = y + h

    # Draw the buttons onto the on screen
    for button in tool_buttons_list:
        # keep tool button.is_active in sync with active_tool
        if button.tool != active_tool:
            button.is_active = False
        button.draw(screen)  

    for button in misc_buttons_list + layer_buttons_list + color_buttons_list:
        button.draw(screen)

    lw_value_button.text=f"{line_thickness}"
    for button in lw_a_buttons_list + layer_func_buttons_list:
        button.is_active = False
        button.draw(screen)

    alpha_percent = int(round(alpha * 100 / 255))
    alpha_value_button.text=f"{alpha_percent}%"
    for button in lw_a_buttons_list:
        button.is_active = False
        button.draw(screen)

    # Draw the current color
    current_color_button.active_color = current_color_button.inactive_color = current_color+(alpha,)
    current_color_button.draw(screen)

    # Draw the button section texts on the screen
    font = pygame.font.SysFont('Arial', 18, bold=True)
    # Left side
    screen.blit(font.render("Tools"  , True, BLACK), (edge_padding, 50-25))
    screen.blit(font.render("Shapes" , True, BLACK), (edge_padding, 50-25+(button_h+button_padding)*3))
    screen.blit(font.render("Exit" , True, BLACK), (edge_padding, 50-25+(button_h+button_padding)*11.9))
    # Right side
    screen.blit(font.render("Layers" , True, BLACK), (screen_width - edge_padding - button_w, 50-25))
    screen.blit(font.render("File"   , True, BLACK), (screen_width - edge_padding - button_w, 50-30+(button_h+button_padding)*8))

    # Display mouse coordinate at the bottom left of the screen
    mouse_pos = pygame.mouse.get_pos()
    mouse_coordinate_text = f"{mouse_pos[0]- x_canvas_border_width} , {mouse_pos[1]}"
    font = pygame.font.SysFont('Arial', 12)
    mouse_coor_surface = font.render(mouse_coordinate_text , True, BLACK)
    screen.blit(mouse_coor_surface, (15, screen_height-15))

    # Draw button tooltip on the screen
    for button in tool_buttons_list + misc_buttons_list + layer_buttons_list + layer_func_buttons_list + color_buttons_list + lw_a_buttons_list:
        button.draw_tooltip(screen)        
    current_color_button.draw_tooltip(screen)

    # --- Update the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(fps) # Limit frames per second to fps

pygame.quit()
