import pygame
import random

WIDTH = 1000
HEIGHT = 600

class Word:
    def __init__(self, text, x, y, speed):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.y += self.speed

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Typing Test")
        self.background = pygame.image.load("space.webp").convert()
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.set_volume(0.5)

        # Define the Start, Restart, and Difficulty buttons
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50)
        self.difficulty_buttons = {
            "easy": pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 30, 100, 50),
            "medium": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50),
            "hard": pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 + 30, 100, 50)
        }
        self.restart_button = pygame.Rect(WIDTH - 60, 10, 30, 30)

        # Load the restart and difficulty buttons' images and resize them
        original_restart_icon = pygame.image.load("restart_icon.png")
        self.restart_icon = pygame.transform.scale(original_restart_icon, (30, 30))

        original_difficulty_icons = {
            "easy": pygame.image.load("easy_icon.png"),
            "medium": pygame.image.load("medium_icon.png"),
            "hard": pygame.image.load("hard_icon.png")
        }
        self.difficulty_icons = {key: pygame.transform.scale(img, (30, 30)) for key, img in original_difficulty_icons.items()}

        # Initial state
        self.state = "start"
        self.difficulty = None

    def load_word_list(self, filename):
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return words

    def falling_words_animation(self, words, fps):
        clock = pygame.time.Clock()
        word_objects = []

        drop_interval = 1000
        last_drop_time = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.restart_button.collidepoint(mouse_pos):
                        # Reset the state to "start"
                        self.state = "start"
                        return

            if current_time - last_drop_time > drop_interval:
                x = random.randint(50, WIDTH - 50)
                y = 0
                speed = self.get_difficulty_speed()
                word_objects.append(Word(random.choice(words), x, y, speed))
                last_drop_time = current_time

            for word in word_objects:
                word.update()

                if word.y > HEIGHT:
                    word_objects.remove(word)

            self.screen.blit(self.background, (0, 0))
            font = pygame.font.Font(None, 36)

            for word in word_objects:
                text = font.render(word.text, True, (255, 255, 255))
                self.screen.blit(text, (word.x - text.get_width() // 2, word.y - text.get_height() // 2))

            # Draw the restart button image
            self.screen.blit(self.restart_icon, self.restart_button.topleft)

            pygame.display.flip()
            clock.tick(fps)

    def start_screen(self):
        font = pygame.font.Font(None, 48)
        start_text = font.render("Press Start to Play", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 180))

        difficulty_text = font.render("Select Difficulty:", True, (255, 255, 255))
        difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.collidepoint(mouse_pos):
                        # Change the state to "game"
                        self.state = "game"
                        return
                    elif any(button.collidepoint(mouse_pos) for button in self.difficulty_buttons.values()):
                        # Set the selected difficulty
                        for key, button in self.difficulty_buttons.items():
                            if button.collidepoint(mouse_pos):
                                self.difficulty = key

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(start_text, start_rect)
            self.screen.blit(difficulty_text, difficulty_rect)

            pygame.draw.rect(self.screen, (0, 128, 255), self.start_button)
            button_text = font.render("Start", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=self.start_button.center)
            self.screen.blit(button_text, button_rect)

            for key, button in self.difficulty_buttons.items():
                pygame.draw.rect(self.screen, (0, 128, 255), button)
                self.screen.blit(self.difficulty_icons[key], button.topleft)

            pygame.display.flip()

    def get_difficulty_speed(self):
        if self.difficulty == "easy":
            return random.randint(1, 4)
        elif self.difficulty == "medium":
            return random.randint(3, 7)
        elif self.difficulty == "hard":
            return random.randint(4, 9)
        else:
            return random.randint(1, 5)

    def run_game(self):
        pygame.mixer.music.play(-1)  # Start playing the background music

        while True:
            if self.state == "start":
                self.start_screen()  # Show the starting screen
            elif self.state == "game":
                if self.difficulty is not None:
                    word_list = self.load_word_list("words.txt")
                    self.falling_words_animation(word_list, 60)
                else:
                    # If difficulty is not selected, go back to the starting screen
                    self.state = "start"

def main():
    curr_game = Game()
    curr_game.run_game()

if __name__ == "__main__":
    main()
