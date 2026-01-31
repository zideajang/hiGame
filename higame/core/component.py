from abc import ABC,abstractmethod
class Component(ABC):

    COMPONENT_TYPE = "base" 
    TAGS = [] # Component 属于什么类别
    def __init__(self):
        self.entity = None  # 持有 Entity 的引用
    @abstractmethod
    def update(self, dt):
        pass