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
    
    def mainLoop(self):
        running = True
        while running:
            screen.fill('gray')
            timer.tick(fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.flip()
        pygame.quit()
        
def initScreen():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Typing Test")
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    timer = pygame.timer.Clock()
    fps = 60

def main():
    initScreen()
    curr_game = Game()
    Game.mainLoop()
    
    


if __name__ == "__main__":
    main()
    