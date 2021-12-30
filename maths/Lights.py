
# Trying to follow a similar lighting model described here
# https://learnopengl.com/Lighting/Basic-Lighting

class LightSource:
    def __init__(self, direction, diffuse, specular, ambient) -> None:
        # Vector
        self.direction = direction
        # Colors
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
    
    def set_light_in_shader(self, shader, index):
        shader.set_light_position(self.direction, index)
        shader.set_light_diffuse(self.diffuse, index)
        shader.set_light_specular(self.specular, index)
        shader.set_light_ambient(self.ambient, index)
