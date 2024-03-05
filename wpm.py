import time
import pygame

WIDTH = 800
HEIGHT = 600

class word:
    def __init__(self, _livingTime, _speed):
        self.livingTime = _livingTime
        self.speed = _speed

class Game:
    def __init__(self):
        pass
    
    def resetGame(self):
        pass
    
    def startGame(self):
        pass
    
    def mainLoop(self, screen, timer, fps, background):
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)

        
        running = True
        while running:
            screen.blit(background, (0, 0))
            timer.tick(fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            
        pygame.mixer.music.stop()
        pygame.quit()
        
def initScreen():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Typing Test")
    background = pygame.image.load("space.webp").convert()
    return screen, pygame.time.Clock(), 60, background



def main():
    screen, timer, fps, background = initScreen()
    curr_game = Game()
    curr_game.mainLoop(screen, timer, fps, background)
    
    
if __name__ == "__main__":
    main()
    