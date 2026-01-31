import pygame
from higame.core.component import Component


class DrawCirlceComponent(Component):
    COMPONENT_TYPE = "draw_circle" 
    TAGS = ["render"] # Component 属于什么类别
    def __init__(self,pos_attr=None,radius=12, color=(255, 0, 0), width=0):
        super().__init__()
        self.pos_attr = pos_attr
        # 绘制属性
        self.radius = radius
        self.color = color
        self.width = width  # 0 为实心圆，>0 为空心圆线条宽度

    def draw(self, surface, camera=None):
        # 1. 获取实体的位置 (假设 entity 有 position 属性)
        # 如果有 Camera，需要减去相机偏移量来实现滚动效果
        
        if camera:
            # 应用相机偏移：屏幕坐标 = 世界坐标 - 相机坐标
            draw_pos = (int(self.pos.x  - camera.offset.x), int(self.pos.y  - camera.offset.y))

        else:
            draw_pos = (int(self.pos.x),int(self.pos.y))

        # 2. 使用 Pygame 绘制圆
        pygame.draw.circle(
            surface, 
            self.color, 
            draw_pos, 
            self.radius, 
            self.width
        )

    def update(self, dt):
        # 渲染组件的 update 通常保持为空，除非有动画逻辑（如闪烁）
        if self.pos_attr is None:
            self.pos = self.entity.pos
        else:
            if hasattr(self.entity, self.pos_attr):
                # pos = self.entity[self.name]
                self.pos = getattr(self.entity, self.pos_attr)
                print(f"{self.pos_attr}:{self.pos}")
            else:
                self.pos = self.entity.pos


import pygame
from higame.core.component import Component
import pygame

class DrawLineComponent(Component):
    COMPONENT_TYPE = "draw_line" 
    TAGS = ["render", "line"]

    def __init__(self, target_entity, color=(255, 0, 0), width=2):
        super().__init__()
        # 目标实体（终点）
        self.target_entity = target_entity
        self.color = color
        self.width = width
        # 起点和终点的实时位置缓存
        self.start_pos = pygame.Vector2(0, 0)
        self.end_pos = pygame.Vector2(0, 0)

    def update(self, dt):
        if hasattr(self.entity, 'pos') and self.entity.pos:
            # 尝试获取中心点，如果失败则回退到 top-left (x, y)
            center = getattr(self.entity.pos, 'center', (self.entity.pos[0], self.entity.pos[1]))
            self.start_pos = pygame.Vector2(center)
        
        if self.target_entity and hasattr(self.target_entity, 'pos') and self.target_entity.pos:
            target_center = getattr(self.target_entity.pos, 'center', (self.target_entity.pos[0], self.target_entity.pos[1]))
            self.end_pos = pygame.Vector2(target_center)

    def draw(self, surface, camera=None):
        """
        surface: 绘图平面 (通常是 screen 或 layer)
        camera: 摄像机对象，用于坐标转换
        """
        # 计算在屏幕上的实际绘制位置
        if camera:
            # 屏幕坐标 = 世界坐标 - 相机偏移
            render_start = self.start_pos - camera.offset
            render_end = self.end_pos - camera.offset
        else:
            render_start = self.start_pos
            render_end = self.end_pos

        # 执行绘制
        pygame.draw.line(
            surface, 
            self.color, 
            (int(render_start.x), int(render_start.y)), 
            (int(render_end.x), int(render_end.y)), 
            self.width
        )