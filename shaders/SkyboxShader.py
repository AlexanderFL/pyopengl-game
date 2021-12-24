from shaders.Shaders import Shaders
from OpenGL.GL import *
import sys
import numpy

class SkyboxShader(Shaders):
    def __init__(self) -> None:
        vert_shader = sys.path[0] + "\\shaders\\skybox.vert"
        frag_shader = sys.path[0] + "\\shaders\\skybox.frag"
        super().__init__(vert_shader, frag_shader)
        
        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "aPos")
        glEnableVertexAttribArray(self.positionLoc)
    
    #def set_position_attribute(self, array):
    #    glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, array)

    def set_skybox(self, i):
        glUniform1i(glGetUniformLocation(self.renderingProgramID, "skybox"), i)
    
    def set_view_attribute(self, view):
        glUniformMatrix4fv(glGetUniformLocation(self.renderingProgramID, "view"), 1, GL_FALSE, view)
    
    def set_projection_attribute(self, projection):
        glUniformMatrix4fv(glGetUniformLocation(self.renderingProgramID, "projection"), 1, GL_FALSE, projection)