
from math import pi, cos, sin
from OpenGL.GL import *

class Crosshair:
    def __init__(self):

        self.samples = 21
        self.position_array = [0, 0]

        rad = 0.0025
        for i in range(0, self.samples):
            x = rad * cos(i * 2*pi / (self.samples - 1))
            y = rad * 1.8 * sin(i * 2*pi / (self.samples - 1))
            self.position_array.append(x)
            self.position_array.append(y)

    def draw(self):
        # Really tried to make this work with shader files but I kept getting very unexpected results
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.0, 0.0)
        for i in range(0, self.samples*2+1, 2):
            glVertex2f(self.position_array[i], self.position_array[i+1])
        glEnd()