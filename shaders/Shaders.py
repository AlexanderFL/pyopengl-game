from OpenGL.GL import *
import sys

class Shaders:
    def __init__(self, vertex_shader, fragment_shader) -> None:
        cvert_shader = self.compile_shader(GL_VERTEX_SHADER, vertex_shader)
        cfrag_shader = self.compile_shader(GL_FRAGMENT_SHADER, fragment_shader)
        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, cvert_shader)
        glAttachShader(self.renderingProgramID, cfrag_shader)
        glLinkProgram(self.renderingProgramID)
    
    def compile_shader(self, SHADER_TYPE, file_name):
        shader = glCreateShader(SHADER_TYPE)
        shader_file = open(file_name)
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