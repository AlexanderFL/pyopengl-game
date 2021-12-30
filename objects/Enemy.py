from objects.GameObjectBase import GameObject
from maths.Point import Point

class Enemy(GameObject):
    def __init__(self, shader, position=Point(0,0,0)) -> None:
        self.shader = shader
        self.position = position