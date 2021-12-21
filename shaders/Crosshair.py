from OpenGL.GL import *

import sys

class ShaderCrosshair:
    def __init__(self):
        vert_shader = self.compile_shader(GL_VERTEX_SHADER, "crosshair.vert")
        frag_shader = self.compile_shader(GL_FRAGMENT_SHADER, "crosshair.frag")

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc    = glGetAttribLocation(self.renderingProgramID, "u_crosshair_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.projectionMatrixLoc   = glGetAttribLocation(self.renderingProgramID, "u_projection_matrix")

    def compile_shader(self, SHADER_TYPE, file_name):
        shader = glCreateShader(SHADER_TYPE)
        shader_file = open(sys.path[0] + "\\shaders\\" + file_name)
        glShaderSource(shader, shader_file.read())
        shader_file.close()
        glCompileShader(shader)
        result = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if (result != 1):
            print("Couldn't compile shader\nShader compilation log:\n" + str(glGetShaderInfoLog(shader)))
        else:
            print("Compiled shader " + shader_file.name)
        return shader
    
    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 2, GL_FLOAT, False, 0, vertex_array)
    
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)