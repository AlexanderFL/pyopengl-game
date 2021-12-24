from shaders.Shaders import Shaders
from OpenGL.GL import *
from math import *

import sys


class Shader3D(Shaders):
    def __init__(self):
        # Compiling and linking the shader files
        vert_shader = sys.path[0] + "\\shaders\\simple3D.vert"
        frag_shader = sys.path[0] + "\\shaders\\simple3D.frag"
        super().__init__(vert_shader, frag_shader)

        # Getting the shader variable locations
        self.positionLoc    = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        self.normalLoc      = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
        self.uvLoc          = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.eyePosLoc              = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.lightPosLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDifLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.matDifLoc              = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")
        self.matSpecLoc             = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.matShinyLoc            = glGetUniformLocation(self.renderingProgramID, "u_material_shininess")
        self.diffuseTexLoc          = glGetUniformLocation(self.renderingProgramID, "u_tex01")

        self.modelMatrixLoc         = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc          = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc    = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
    
    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, a_normal):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, a_normal)
    
    def set_uv_attribute(self, uv):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, uv)

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)
    
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)
    
    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_specular(self, r, g, b):
        glUniform4f(self.lightSpecLoc, r, g, b, 1.0)
    
    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.lightDifLoc, r, g, b, 1.0)
    
    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.matDifLoc, r, g, b, 1.0)
    
    def set_material_specular(self, r, g, b):
        glUniform4f(self.matSpecLoc, r, g, b, 1.0)
    
    def set_material_shininess(self, shiny):
        glUniform1f(self.matShinyLoc, shiny)
    
    def set_diffuse_texture(self, tex):
        glUniform1f(self.diffuseTexLoc, tex)
    
    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    """
    Texture testing
    """
    def set_diffuse_texture(self, diffuseTexture):
        pass

    def set_specular_texture(self, specularTexture):
        pass
