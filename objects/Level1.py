
from math import pi
from objects.GameObjectBase import GameObject
import sys

if __name__ == "__main__":
    from Cube import Cube
else:
    from objects.Cube import Cube

class Level1(GameObject):
    """
        The Level1 gameobject
    """
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z)
        self.size = 20
        
        wall_color = (78/255, 233/255, 81/255)
        longwall = sys.path[0] + "\\textures\\longwall.png"
        longwallr = sys.path[0] + "\\textures\\longwall2.png"
        self.wall1 = Cube(0, 0.1, 10, (20, 1.5, 0.1), wall_color, texture_path=longwall)
        self.wall2 = Cube(0, 0.1, -10, (20, 1.5, 0.1), wall_color, texture_path=longwall)
        self.wall3 = Cube(10, 0.1, 0, (0.1, 1.5, 20), wall_color, texture_path=longwallr)
        self.wall4 = Cube(-10, 0.1, 0, (0.1, 1.5, 20), wall_color, texture_path=longwallr)

        # Fill the list with instances of Cube() that can then be drawn
        self.cubes = []

        self.cubes.append(self.wall1)
        self.cubes.append(self.wall2)
        self.cubes.append(self.wall3)
        self.cubes.append(self.wall4)

        self.destroy = False
        
    
    def collision(self, player_pos) -> GameObject:
        # Implement collision
        collision_walls = []
        for x in range(0, len(self.cubes)):
            c = self.cubes[x].collision(player_pos)
            if c is not None:
                collision_walls.append(c)
        if collision_walls == []:
            return None
        return collision_walls
    
    def draw(self, modelMatrix, shader, update_shader=False) -> None:
        # Implement the draw call
        for x in range(0, len(self.cubes)):
            c = self.cubes[x]
            c.draw(modelMatrix, shader, update_shader)

    def update(self, delta_time, game_objects):
        pass