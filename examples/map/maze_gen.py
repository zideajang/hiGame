import sys
import pygame


from higame.generator.maze import Maze
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS= 60
class MazeGen:
    def __init__(self,name,w,h):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        # 
        self.map = Maze(w=800,h=1000,grid_size=20)
        self.map.generate()
    def run(self):
        dt = self.clock.tick(FPS) / 1000.0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WHITE)
            self.map.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = MazeGen("maze",w=800,h=1000)
    game.run()