import time, pygame as p, sys, math

class Notification:
    def __init__(self, status: str, user):
        # Initialize pygame and set the screen size
        p.init()
        w, h = 400, 200
        self.screen = p.display.set_mode((w, h), p.SRCALPHA)#.convert_alpha()
        p.display.set_caption("Notification Status")  # Imposta il nome della finestra
        self.clock = p.time.Clock()  # Clock per il controllo del framerate
        self.running = False # If the status is True, create a green circle and set it as the icon
        
        if status == "online":
            self.circle_color = "green"
            self.icon_color = "green"
        elif status == "offline":
            self.circle_color = "red"
            self.icon_color = "red"
        elif status == "indisponible":
            self.circle_color = "blue"
            self.icon_color = "blue"
            
        self.circle = Circle(self.screen, self.circle_color, "left", "squ")
        self.circle_icon = Circle(self.screen, self.icon_color, "posicon", "cir")
        self.set_icon(self.circle_icon.draw_circle(type="icon"))
        
        #Text
        self.text = f"{user} Now is {status}!"  # Set the text to display
        self.text_color = (255, 255, 255)  # Set the color of the text

    def set_icon(self, icon_surface: p.Surface):
        # Set the icon of the display to the provided surface
        if icon_surface:
            p.display.set_icon(icon_surface)


    def close_window(self):
        p.quit()  # Chiude la finestra pygame

    def show_notification(self, duration, text):
        self.running = True
        start_time = p.time.get_ticks()  # Tempo di inizio della visualizzazione
        font = p.font.SysFont(None, 36)  # Set the font and size
        text_surface = font.render(text, True, self.text_color)  # Render the text
        text_rect = text_surface.get_rect(center=(230, 100))  # Get the rectangle of the text surface
        while self.running:
            self.clock.tick(15)  # Imposta il framerate a 15 FPS

            # Calcola il tempo trascorso dalla visualizzazione
            elapsed_time = p.time.get_ticks() - start_time

            # Aggiorna la finestra pygame
            # self.screen.fill((80, 80, 80))# Sfondo bianco
            self.circle.draw_circle()  # Disegna il cerchio
            self.screen.blit(text_surface, text_rect)  # Draw the text on the screen

            # Gestione della chiusura della finestra dopo la durata specificata
            if elapsed_time >= duration * 1000:
                self.running = False

            # Gestione degli eventi
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False

            # Aggiorna la finestra
            p.display.flip()

        p.quit()  # Chiude la finestra pygame





class Circle:
    def __init__(self, screen: p.Surface, color: str, pos: str, shape: str) -> None:
        # Initialize the Circle object with screen, color, position, and shape
        self.color = color
        self.pos = pos
        self.shape = shape
        self.screen = screen

    def draw_circle(self, type: str = None):
        # Define colors and positions for drawing the circle
        colors = {
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)
        }

        position = {
            "center": (200, 100),
            "left": (75, 100),
            "right": (325, 100),
            "topcenter": (200, 25),
            "downcenter": (200, 175),
            "topleft": (75, 25),
            "downleft": (75, 175),
            "topright": (325, 25),
            "downright": (325, 175),
            "posicon": (25,25)
        }

        # Define radius values for different shapes of circles
        r = 25
        square_radius = r / math.sqrt(2)  # Square: half the length of the side
        middle_radius = (r + square_radius) / 2  # Between square and circle: average of the two radii
        circle_radius = r  # Circle: the radius remains unchanged
        shape_r = {"squ": square_radius, "mid": middle_radius, "cir": circle_radius}

        # Draw circle icon
        if type == "icon":
            icon_surface = p.Surface((r * 2, r * 2), p.SRCALPHA)  # Create a surface with transparent background for the icon
            icon_surface.fill((0, 0, 0, 0))  # Fill the icon surface with transparent background
            p.draw.circle(icon_surface, colors[self.color], position[self.pos], shape_r[self.shape])  # Draw the circle on the icon surface
            return icon_surface  # Return the icon surface

        # Draw circle
        if type is None:
            return p.draw.circle(self.screen, colors[self.color], position[self.pos], shape_r[self.shape])

