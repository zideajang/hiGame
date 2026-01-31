from abc import ABC,abstractmethod
class Map(ABC):
    def __init__(self,w:int,h:int):
        self._width = w
        self._height = h
        self

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @abstractmethod
    def draw(self):
        pass
    

    