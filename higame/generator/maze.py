import random
from typing import List
import pygame
from higame.core.map import Map
BLUE = (0, 120, 255)
import random
from typing import List
import pygame

# 

class Maze:
    def __init__(self, w: int, h: int, 
                 grid_size: int, 
                 num_rooms: int = 10, 
                 min_cell_size: int = 2, 
                 margin: int = 30):
        
        # 
        self.width, self.height = w, h
        self.grid_size = grid_size
        self.num_rooms = num_rooms
        self.min_cell_dim = min_cell_size * self.grid_size
        
        self.cells: List[Cell] = []
        self.halls: List[Hall] = []
        # 初始化时候创建 Root 
        self.root = Cell(margin, margin, w - margin, h - margin)

    def generate(self):
        """ 完整的生成流程 """
        # 1. 递归分割
        self.divide()
        
        # 2. 刷新叶子节点列表
        self.cells = []
        self.root.get_leaves(self.cells)
        # cells
        
        # 3. 在收缩前寻找邻居 (此时边界是完美贴合的)
        self.find_neighbors()
        
        self.shrink()
        # 5. 最后收缩区域变成房间
        # 4. 生成走廊 (基于原始边界计算连接点)

        self.root.snap_to_grid(self.grid_size)

        self.add_halls()
        

    def divide(self):
        rooms = 1
        while rooms < self.num_rooms:
            if self.root.divide(self.min_cell_dim):
                rooms += 1

    def find_neighbors(self):
        for c in self.cells:
            c.h_neighbors, c.v_neighbors = [], []
            for o in self.cells:
                if c is o: continue
                # 水平相邻检测
                if c.x2 == o.x1 and max(c.y1, o.y1) < min(c.y2, o.y2):
                    c.h_neighbors.append(o)
                # 垂直相邻检测
                if c.y2 == o.y1 and max(c.x1, o.x1) < min(c.x2, o.x2):
                    c.v_neighbors.append(o)

    def add_halls(self):
        self.halls = []
        for c in self.cells:
            # 水平走廊
            for n in c.h_neighbors:
                overlap_y_start = max(c.y1, n.y1)
                overlap_y_end = min(c.y2, n.y2)
                if (overlap_y_end - overlap_y_start) > self.grid_size:
                    y = random.uniform(overlap_y_start, overlap_y_end - self.grid_size)
                    self.halls.append(Hall(c.x2 , y, n.x1 , y + self.grid_size)) # 稍微重叠确保无缝

            # 垂直走廊
            for n in c.v_neighbors:
                overlap_x_start = max(c.x1, n.x1)
                overlap_x_end = min(c.x2, n.x2)
                if (overlap_x_end - overlap_x_start) > self.grid_size:
                    x = random.uniform(overlap_x_start, overlap_x_end - self.grid_size)
                    self.halls.append(Hall(x, c.y2 , x + self.grid_size, n.y1 + 2))

    def shrink(self):
        self.root.shrink(self.min_cell_dim)

    def draw(self, screen):
        # 先画走廊 (底层)
        for hall in self.halls:
            hall.draw(screen)
        # 后画房间 (顶层)
        self.root.draw(screen,self.grid_size)

class Cell:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.left = self.right = None
        self.h_neighbors, self.v_neighbors = [], []

    def get_leaves(self, cells_list):
        if self.left is None:
            cells_list.append(self)
        else:
            self.left.get_leaves(cells_list)
            self.right.get_leaves(cells_list)

    def snap_to_grid(self, grid_size):
        if self.left:
            self.left.snap_to_grid(grid_size)
            self.right.snap_to_grid(grid_size)
        else:
            # 四舍五入到最近的网格线
            self.x1 = round(self.x1 / grid_size) * grid_size
            self.y1 = round(self.y1 / grid_size) * grid_size
            self.x2 = round(self.x2 / grid_size) * grid_size
            self.y2 = round(self.y2 / grid_size) * grid_size
            
            # 确保对齐后房间依然有最小尺寸 (防止消失)
            if self.x2 <= self.x1: self.x2 = self.x1 + grid_size
            if self.y2 <= self.y1: self.y2 = self.y1 + grid_size
    
    def divide(self, min_dim):
        w, h = self.x2 - self.x1, self.y2 - self.y1
        if w < min_dim  and h < min_dim : return False
        
        if self.left: # 递归向下尝试分割
            if random.random() < 0.5:
                return self.left.divide(min_dim) 
            else:
                return self.right.divide(min_dim)

        # 决定切割方向
        split_horizontally = random.choice([True, False]) if abs(w-h) < 10 else (w < h)
        
        if not split_horizontally: # 垂直切割
            mid = self.x1 + random.uniform(0.3, 0.6) * w
            self.left = Cell(self.x1, self.y1, mid, self.y2)
            self.right = Cell(mid, self.y1, self.x2, self.y2)
        else: # 水平切割
            mid = self.y1 + random.uniform(0.3, 0.6) * h
            self.left = Cell(self.x1, self.y1, self.x2, mid)
            self.right = Cell(self.x1, mid, self.x2, self.y2)
        return True

    def shrink(self, min_dim):
        if self.left:
            self.left.shrink(min_dim)
            self.right.shrink(min_dim)
        else:
            w, h = self.x2 - self.x1, self.y2 - self.y1
            new_w = max(w * random.uniform(0.25, 0.9), min_dim)
            new_h = max(h * random.uniform(0.25, 0.9), min_dim)
            self.x1 += (w - new_w) / 2
            self.x2 -= (w - new_w) / 2
            self.y1 += (h - new_h) / 2
            self.y2 -= (h - new_h) / 2

    def draw(self, screen, grid_size):
        if self.left:
            self.left.draw(screen, grid_size)
            self.right.draw(screen, grid_size)
        else:
            # 1. 绘制房间背景
            rect = (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
            pygame.draw.rect(screen, (20, 20, 40), rect) # 深色背景

            # 2. 绘制内部网格线
            grid_color = (40, 40, 80) # 微亮的网格线颜色
            
            # 绘制垂直线
            for x in range(int(self.x1), int(self.x2) + 1, grid_size):
                pygame.draw.line(screen, grid_color, (x, self.y1), (x, self.y2))
            
            # 绘制水平线
            for y in range(int(self.y1), int(self.y2) + 1, grid_size):
                pygame.draw.line(screen, grid_color, (self.x1, y), (self.x2, y))

            # 3. 绘制房间外边框 (蓝色)
            pygame.draw.rect(screen, (0, 120, 255), rect, 1)

class Hall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))