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
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Typing Test")
        self.background = pygame.image.load("space.webp").convert()

    def load_word_list(self, filename):
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return words

    def falling_words_animation(self, words, fps):
        clock = pygame.time.Clock()
        word_objects = []

        drop_interval = 1000  # 3 sec
        last_drop_time = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if current_time - last_drop_time > drop_interval:
                x = random.randint(50, WIDTH - 50)
                y = 0
                word_objects.append(Word(random.choice(words), x, y, random.randint(2, 5)))
                last_drop_time = current_time

            for word in word_objects:
                word.update()

                if word.y > HEIGHT:
                    word_objects.remove(word)  # Remove the word when it reaches the bottom

            self.screen.blit(self.background, (0, 0))
            font = pygame.font.Font(None, 36)

            for word in word_objects:
                text = font.render(word.text, True, (255, 255, 255))
                self.screen.blit(text, (word.x - text.get_width() // 2, word.y - text.get_height() // 2))

            pygame.display.flip()
            clock.tick(fps)

    def run_game(self):
        word_list = self.load_word_list("words.txt")  # Update the filename to "words.txt"
        self.falling_words_animation(word_list, 60)

        pygame.quit()

def main():
    curr_game = Game()
    curr_game.run_game()

if __name__ == "__main__":
    main()
