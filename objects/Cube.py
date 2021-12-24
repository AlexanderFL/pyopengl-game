from OpenGL.GL import *
from OpenGL.GLU import *

from shaders.SimpleShaders import Shader3D
import numpy

class CubeObject:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,

                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,

                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,

                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]

        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]
    
    def set_vertecies(self, shader:Shader3D):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader, update_shader=False, texture=False):
        if update_shader:
            shader.set_position_attribute(self.position_array)
            shader.set_normal_attribute(self.normal_array)
        
        if texture != None:
            pass

        draw_method = GL_TRIANGLE_FAN 
        glDrawArrays(draw_method, 0, 4)
        glDrawArrays(draw_method, 4, 4)
        glDrawArrays(draw_method, 8, 4)
        glDrawArrays(draw_method, 12, 4)
        glDrawArrays(draw_method, 16, 4)
        glDrawArrays(draw_method, 20, 4)
        