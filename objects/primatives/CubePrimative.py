from OpenGL.GL import *
from OpenGL.GLU import *

from shaders.Shaders import Shader3D
import numpy

class CubePrimative:
    def __init__(self):
        cube_array = [
            #position           normals             uv
            -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,     0.0, 0.0,
            -0.5, 0.5, -0.5,    0.0, 0.0, -1.0,     0.0, 1.0,
            0.5, 0.5, -0.5,     0.0, 0.0, -1.0,     1.0, 1.0,
            0.5, -0.5, -0.5,    0.0, 0.0, -1.0,     1.0, 0.0,

            -0.5, -0.5, 0.5,    0.0, 0.0, 1.0,      0.0, 0.0,
            -0.5, 0.5, 0.5,     0.0, 0.0, 1.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      0.0, 0.0, 1.0,      1.0, 1.0,
            0.5, -0.5, 0.5,     0.0, 0.0, 1.0,      1.0, 0.0,

            -0.5, -0.5, -0.5,   0.0, -1.0, 0.0,     0.0, 0.0,
            0.5, -0.5, -0.5,    0.0, -1.0, 0.0,     0.0, 1.0,
            0.5, -0.5, 0.5,     0.0, -1.0, 0.0,     1.0, 1.0,
            -0.5, -0.5, 0.5,    0.0, -1.0, 0.0,     1.0, 1.0,

            -0.5, 0.5, -0.5,    0.0, 1.0, 0.0,      0.0, 0.0,
            0.5, 0.5, -0.5,     0.0, 1.0, 0.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      0.0, 1.0, 0.0,      1.0, 1.0,
            -0.5, 0.5, 0.5,     0.0, 1.0, 0.0,      1.0, 0.0,

            -0.5, -0.5, -0.5,   -1.0, 0.0, 0.0,     0.0, 0.0,
            -0.5, -0.5, 0.5,    -1.0, 0.0, 0.0,     0.0, 1.0,
            -0.5, 0.5, 0.5,     -1.0, 0.0, 0.0,     1.0, 1.0,
            -0.5, 0.5, -0.5,    -1.0, 0.0, 0.0,     1.0, 0.0,

            0.5, -0.5, -0.5,    1.0, 0.0, 0.0,      0.0, 0.0,
            0.5, -0.5, 0.5,     1.0, 0.0, 0.0,      0.0, 1.0,
            0.5, 0.5, 0.5,      1.0, 0.0, 0.0,      1.0, 1.0,
            0.5, 0.5, -0.5,     1.0, 0.0, 0.0,      1.0, 0.0
        ]
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(cube_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Draw fuction for a primitive cube object
    def draw(self, shader):
        shader.set_attrib_buffers_tex(self.vertex_buffer_id)

        for i in range(0, 6):
            glDrawArrays(GL_TRIANGLE_FAN, i * 4, 4)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
