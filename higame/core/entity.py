from typing import Dict

import uuid
import pygame
from higame.core.component import Component
class Entity(pygame.sprite.Sprite):
    def __init__(self,
                 name,x:int,y:int,
                 groups,max_speed:int = 2):
        super().__init__(groups)
        self.id = uuid.uuid4().hex  # 唯一标识符
        self.name:str = name
        self.parent = None
        
        self._pos:pygame.math.Vector2 = pygame.math.Vector2(x, y)

        # 速度大小
        self.max_speed = max_speed
         # 速度方向向量(单位向量)
        self.direction:pygame.math.Vector2 = pygame.math.Vector2(0, 0)

        self.vel:pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.acc:pygame.math.Vector2 = pygame.math.Vector2(0,0)

        self.components:Dict[str,Component] = {} # 存储组件的字典: {ComponentType: ComponentInstance}
        self.is_active:bool = True

        self._groups = groups
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self,new_pos):
        self._pos = new_pos

    @property
    def pos_y(self):
        return self._pos.y
    
    @property
    def pos_x(self):
        return self._pos.x
    

        
    def add_component(self, component,component_name=None):
        """添加组件并建立双向链接"""
        if component_name:
            self.components[component_name] = component
        else:
            self.components[component.__class__.__name__] = component
            
        component.entity = self
        return self # 链式调用支持

    def has_component(self, component_name: str) -> bool:
        """判断实体是否包含指定名称的组件"""
        return component_name in self.components
    def get_component(self, component_type):
        """获取指定类型的组件"""
        return self.components.get(component_type)

    def update(self, dt):
        """更新所有组件"""
        for component in self.components.values():
            component.update(dt)


    