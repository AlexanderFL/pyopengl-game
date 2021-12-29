
# Trying to follow a similar lighting model described here
# https://learnopengl.com/Lighting/Basic-Lighting

class DirectionalLight:
    def __init__(self, direction, diffuse, specular, ambient) -> None:
        # Vector
        self.direction = direction
        # Colors
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
    
    def set_light_in_shader(self, shader):
        shader.set_light_position(self.direction)
        shader.set_light_diffuse(self.diffuse)
        shader.set_light_specular(self.specular)

class PointLight:
    def __init__(self, position, constant, linear, quadratic, ambient, diffuse, specular) -> None:
        # Vector
        self.position = position
        # Floats
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        # Colors
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
    
    def set_lights_in_shader(self, shader, index):
        pass