import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("H_S Museum")
icon = pygame.image.load("mu.png")
pygame.display.set_icon(icon)

bg_1 = (78, 58, 145)
green = (100, 159, 113)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)

font = pygame.font.SysFont("arial", 36)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = green
        self.hover_color = (150, 150, 150)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.action()

class TextInputBox:
    def __init__(self, x, y, width, height, placeholder):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = white
        self.placeholder = placeholder
        self.text = ""
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect, 2)

        if self.active:
            pygame.draw.rect(screen, gray, self.rect)
        else:
            pygame.draw.rect(screen, white, self.rect)

        if not self.text:
            placeholder_surface = font.render(self.placeholder, True, black)
            screen.blit(placeholder_surface, (self.rect.x + 5, self.rect.y + 5))
        else:
            text_surface = font.render(self.text, True, black)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode

class Validator:
    def __init__(self):
        pass

    @staticmethod
    def validate_name(name):
        if any(char.isdigit() or not char.isalnum() for char in name):
            raise ValueError("Name cannot contain numbers or symbols!")

    @staticmethod
    def validate_code(code):
        if not code or any(not char.isalnum() or char in ['!', '@', '#', '$', '%', '^', '&', '*'] for char in code):
            raise ValueError("Code cannot be empty, contain numbers, or symbols!")
        
def draw_text(text, font, color, x, y):
    img = font.render(text, True, black)
    screen.blit(img, (x, y))

validator = Validator()

error_message = ""

def main():
    global error_message

    global name_input, code_input
    submit_button = Button(900, 700, 200, 50, "Submit", submit_action)
    cancel_button = Button(100, 700, 200, 50, "Cancel", cancel_action)

    name_input = TextInputBox(500, 100, 300, 50, "Enter your name")
    code_input = TextInputBox(500, 200, 300, 50, "Enter your code")

    running = True
    while running:
        screen.fill(bg_1)
        draw_text("     Name    :", font, black, 250, 100)
        draw_text("Personal Code:", font, black, 250, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            submit_button.click()
            cancel_button.click()

            name_input.handle_event(event)
            code_input.handle_event(event)

        name_input.draw(screen)
        code_input.draw(screen)
        submit_button.draw(screen)
        cancel_button.draw(screen)

        if error_message:
            error_surface = font.render(error_message, True, red)
            screen.blit(error_surface, (200, 500))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def submit_action():
    global error_message

    try:
        validator.validate_name(name_input.text)
        validator.validate_code(code_input.text)
        error_message = ""
        print(f"Name: {name_input.text}")
        print(f"Code: {code_input.text}")
    except ValueError as e:
        error_message = str(e)

def cancel_action():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
