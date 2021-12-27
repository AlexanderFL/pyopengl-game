from common_game_maths.Vector import Vector
from maths.Matricies import ViewMatrix
from maths.Matricies import ProjectionMatrix
from common_game_maths.Point import Point
from CONSTANTS import *

class Camera:
    def __init__(self, shader, position = Point(0, 0, 0)):
        self.viewMatrix = ViewMatrix()
        self.shader = shader
        self.position = position

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(3.14159/2, SCREEN_WIDTH/SCREEN_HEIGHT, 0.001, 100)
        shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.viewMatrix.look(position, Point(0, 1, 0), Vector(0, 1, 0))

    def pitch(self, angle):
        self.viewMatrix.pitch(angle, True)
    
    def turn(self, angle):
        self.viewMatrix.turn(angle, True)
    
    def look(self, position, center, up):
        self.viewMatrix.look(position, center, up)
    
    def move_position(self, move_vec):
        change = move_vec - self.position
        self.viewMatrix.move_forward(change.x)
        self.viewMatrix.move_sideways(change.z)
        self.position = move_vec

    def set_position(self, position):
        self.viewMatrix.eye = position