import pygame
from higame.core.component import Component
class SpringComponent(Component):
    def __init__(self, anchor_pos, rest_length, k, damping=0.1, gravity=0):
        super().__init__()
        # 弹簧
        self.anchor_pos = anchor_pos
        # 
        self.rest_length = rest_length
        # 弹簧系数
        self.k = k
        # 阻尼系数
        self.damping = damping
        # 
        self.mass = 1.0
        self.gravity = gravity # 增加重力感

    def update(self, dt):
        # 1. 计算位移向量 (从锚点指向实体)
        diff = self.entity.pos - self.anchor_pos
        current_length = diff.length()
        
        if current_length > 0:
            direction = diff.normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        # 2. 胡克定律: F = -k * x
        displacement = current_length - self.rest_length
        spring_force_mag = -self.k * displacement
        spring_force = direction * spring_force_mag

        # 3. 阻尼力: F = -c * v (消耗能量，停止抖动)
        damping_force = -self.damping * self.entity.vel

        # 4. 重力: F = m * g
        gravity_force = pygame.math.Vector2(0, self.gravity * self.mass)

        # 5. 合力与加速度: a = F / m
        total_force = spring_force + damping_force + gravity_force
        acceleration = total_force / self.mass

        # 6. 更新速度与位置 (半隐式欧拉法更稳定)
        self.entity.vel += acceleration * dt
        self.entity.pos += self.entity.vel * dt