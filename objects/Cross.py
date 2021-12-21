
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

class Crosshair:
    def __init__(self):
        self.position_array = [-1, 0,
                               1, 0,
                               0, -1,
                               0, 1]
        
    def set_verticies(self, shader):
        shader.set_position_attribute(self.position_array)
    
    def draw(self, shader):
        shader.set_position_attribute(self.position_array)
        glDrawArrays(GL_LINES, 0, 4)