import re
import sys
import pygame


from higame.core.entity import Entity
from higame.render.base import DrawCirlceComponent,DrawLineComponent
from higame.component.spring import SpringComponent
RENDER_COMP_PATTERN = re.compile(r'^draw_.*')
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS= 60

class SpringDemo:
    def __init__(self,name,w,h):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        
        # 创建一个 Entity
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()

        circle_initial_pos = (w//2,280)
        anchor_initial_pos = (w//2,16)


        anchor = Entity("anchor",anchor_initial_pos[0],
                        anchor_initial_pos[1],[
            self.active_sprites,
            self.visible_sprites])
        
        anchor.add_component(DrawCirlceComponent(
            radius=16,
            color=(255,0,255)),"draw_circle")
        

        circle = Entity("point",circle_initial_pos[0],
                        circle_initial_pos[1],[
            self.active_sprites,
            self.visible_sprites])
        
        anchor.add_component(DrawLineComponent(
            circle
        ),"draw_line")
        
        
        circle.add_component(DrawCirlceComponent(
            radius=32,
            color=(255,255,0)),"draw_circle2")
        
        circle.add_component(SpringComponent(
            anchor_pos=pygame.math.Vector2(w//2,0),
            rest_length=200,k=0.75,damping=0.05))
        

        circle.vel = pygame.math.Vector2(0,50)


        # 绘制先
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        


    def run(self):
        dt = self.clock.tick(FPS) / 1000.0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)
            for sprite in self.active_sprites:
                sprite.update(dt)
            
            for sprite in self.visible_sprites:
                if hasattr(sprite,"image") and sprite.rect:
                    self.screen.blit(sprite.image, sprite.rect.center)
                if hasattr(sprite,"components"):
                    for comp_name, component in sprite.components.items():
                        if RENDER_COMP_PATTERN.match(comp_name):
                            # 执行具有 draw 方法的组件
                            if hasattr(component, 'draw'):
                                component.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = SpringDemo("maze",w=600,h=400)
    game.run()