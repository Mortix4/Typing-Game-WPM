import pygame
import random
import os

WIDTH = 1000
HEIGHT = 600
total_words_typed = 0

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
        self.background = pygame.image.load(os.path.join("assets", "pictures", "space.webp")).convert()
        pygame.mixer.music.load(os.path.join("assets", "sounds", "background_music.mp3"))
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
        original_restart_icon = pygame.image.load(os.path.join("assets", "pictures", "restart_icon.png"))
        self.restart_icon = pygame.transform.scale(original_restart_icon, (30, 30))

        original_difficulty_icons = {
            "easy": pygame.image.load(os.path.join("assets", "pictures", "easy_icon.png")),
            "medium": pygame.image.load(os.path.join("assets", "pictures", "medium_icon.png")),
            "hard": pygame.image.load(os.path.join("assets", "pictures", "hard_icon.png"))
        }
        self.difficulty_icons = {key: pygame.transform.scale(img, (30, 30)) for key, img in original_difficulty_icons.items()}

        # Initial state
        self.state = "start"
        self.difficulty = None
        self.initial_timer = 60 * 60  # second * 60 = minute
        self.timer = self.initial_timer  # Timer attribute now initialized with initial_timer value

        # Words and user input tracking
        self.word_objects = []
        self.user_input = ""
        self.correct_words = 0
        self.total_words = 0

    def display_score(self):
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()

        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)

        score_text = font_large.render(f"WPM: {wpm} | Accuracy: {accuracy}%", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        try_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if try_again_button.collidepoint(mouse_pos):
                        # Reset timer, metrics, and return to the start screen
                        self.timer = self.initial_timer
                        self.correct_words = 0
                        self.total_words = 0
                        self.state = "start"
                        return

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(score_text, score_rect)

            pygame.draw.rect(self.screen, (0, 128, 255), try_again_button)
            try_again_text = font_small.render("Try Again", True, (255, 255, 255))
            try_again_rect = try_again_text.get_rect(center=try_again_button.center)
            self.screen.blit(try_again_text, try_again_rect)

            pygame.display.flip()

    def load_word_list(self, filename):
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return words
    
    def handle_user_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.check_user_input()
                self.user_input = ""
            else:
                self.user_input += event.unicode.lower()
    
    def check_user_input(self):
        global total_words_typed  # Reference the global variable
        for word in self.word_objects:
            if self.user_input == word.text.lower():
                # Remove the word if it matches user input
                self.word_objects.remove(word)
                self.correct_words += 1
                self.total_words += 1
                total_words_typed += 1
                break
            
    def calculate_wpm(self):
        global total_words_typed
        return total_words_typed


    def calculate_accuracy(self):
        if self.total_words == 0:
            return 0
        return int((self.correct_words / self.total_words) * 100)
            
    def falling_words_animation(self, words, fps):
        global total_words_typed  # Reference the global variable
        total_words_typed = 0
        clock = pygame.time.Clock()

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
                        # Reset the state to "start" and timer to initial value
                        self.state = "start"
                        self.timer = self.initial_timer
                        return
                elif self.state == "game":
                    self.handle_user_input(event)

            if current_time - last_drop_time > drop_interval:
                x = random.randint(50, WIDTH - 50)
                y = 0
                speed = self.get_difficulty_speed()
                self.word_objects.append(Word(random.choice(words), x, y, speed))
                last_drop_time = current_time

            for word in self.word_objects:
                word.update()

                if word.y > HEIGHT:
                    # Remove the word if it reaches the bottom without being typed
                    self.word_objects.remove(word)
                    self.total_words += 1

            self.screen.blit(self.background, (0, 0))
            font = pygame.font.Font(None, 36)

            for word in self.word_objects:
                text = font.render(word.text, True, (255, 255, 255))
                if word.text.lower().startswith(self.user_input):
                    # Highlight the matching part in green
                    highlight_color = (0, 255, 0)
                    text_input = font.render(self.user_input, True, highlight_color)
                    text_remainder = font.render(word.text[len(self.user_input):], True, (255, 255, 255))
                    self.screen.blit(text_input, (word.x - text.get_width() // 2, word.y - text.get_height() // 2))
                    self.screen.blit(text_remainder, (word.x + text_input.get_width() - text.get_width() // 2, word.y - text.get_height() // 2))
                else:
                    self.screen.blit(text, (word.x - text.get_width() // 2, word.y - text.get_height() // 2))

            # Draw the restart button image
            self.screen.blit(self.restart_icon, self.restart_button.topleft)

            # Draw timer at the top left
            timer_text = font.render(f"Time: {self.timer // 60:02d}:{self.timer % 60:02d}", True, (255, 255, 255))
            self.screen.blit(timer_text, (10, 10))

            pygame.display.flip()
            clock.tick(fps)
            self.timer -= 1

            if self.timer < 0:
                self.timer = 0
                self.display_score()
                self.state = "start"
                return

    def start_screen(self):
        font = pygame.font.Font(None, 48)
        start_text = font.render("Press Start to Play", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 180))

        difficulty_text = font.render("Select Difficulty:", True, (255, 255, 255))
        difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))

        timer_text = font.render(f"Time: {self.timer // 60:02d}:{self.timer % 60:02d}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topleft=(10, 10))

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
            self.screen.blit(timer_text, timer_rect)

            pygame.draw.rect(self.screen, (0, 128, 255), self.start_button)
            button_text = font.render("Start", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=self.start_button.center)
            self.screen.blit(button_text, button_rect)

            for key, button in self.difficulty_buttons.items():
                border_color = (255, 0, 0) if key == self.difficulty else (0, 128, 255)
                pygame.draw.rect(self.screen, border_color, button, 3)  # Draw a border around the difficulty button
                self.screen.blit(self.difficulty_icons[key], button.topleft)

            pygame.display.flip()

    def get_difficulty_speed(self):
        if self.difficulty == "easy":
            return random.randint(1, 3)
        elif self.difficulty == "medium":
            return random.randint(2, 5)
        elif self.difficulty == "hard":
            return random.randint(4, 7)
        else:
            return random.randint(1, 3)

    def run_game(self):
        pygame.mixer.music.play(-1)  # Start playing the background music
    
        while True:
            if self.state == "start":
                self.start_screen()  # Show the starting screen
            elif self.state == "game":
                if self.difficulty is not None:
                    word_list = self.load_word_list(os.path.join("assets", "words.txt"))
                    self.word_objects = []  # Reset the word_objects list
                    self.falling_words_animation(word_list, 60)
                else:
                    # If difficulty is not selected, go back to the starting screen
                    self.state = "start"


def main():
    curr_game = Game()
    curr_game.run_game()

if __name__ == "__main__":
    main()
