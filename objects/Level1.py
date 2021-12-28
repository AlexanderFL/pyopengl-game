
from math import pi

from objects.GameObjectBase import GameObject
import sys

if __name__ == "__main__":
    from Cube import TexturedCube
else:
    from objects.TexturedCube import TexturedCube
    from .SimpleCube import SimpleCube
    from maths.Material import Material
    from maths.Color import Color

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
        self.wall1 = TexturedCube(0, 0.2, 10, (20, 1.5, 0.1), wall_color, texture_path=longwall)
        self.wall2 = TexturedCube(0, 0.2, -10, (20, 1.5, 0.1), wall_color, texture_path=longwall)
        self.wall3 = TexturedCube(10, 0.2, 0, (0.1, 1.5, 20), wall_color, texture_path=longwallr)
        self.wall4 = TexturedCube(-10, 0.2, 0, (0.1, 1.5, 20), wall_color, texture_path=longwallr)
        
        obst_shiny = 1
        q1_diffuse = Color(244/255, 67/255, 54/255)
        q1_specular = Color(1.0, 67/255, 54/255)
        q1_mat = Material(q1_diffuse, q1_specular, obst_shiny)

        q2_diffuse = Color(76/255, 175/255, 80/255)
        q2_specular = Color(76/255, 1.0, 80/255)
        q2_mat = Material(q2_diffuse, q2_specular, obst_shiny)

        q3_diffuse = Color(33/255, 150/255, 243/255)
        q3_specular = Color(33/255, 150/255, 1.0)
        q3_mat = Material(q3_diffuse, q3_specular, obst_shiny)

        q4_diffuse = Color(1.0, 193/255, 7/255)
        q4_specular = Color(1.0, 193/255, 7/255)
        q4_mat = Material(q4_diffuse, q4_specular, obst_shiny)

        # Quadrant 1
        self.q1_cube_obsticle_1 = SimpleCube(6.5, 0.2, -8.5, q1_mat, (1, 1.5, 3))
        self.q1_cube_obsticle_2 = SimpleCube(2.5, 0.2, -3.5, q1_mat, (5, 1.5, 5))
        self.q1_cube_obsticle_3 = SimpleCube(8.5, 0.2, -2, q1_mat, (3, 1.5, 4))

        # Quadrant 2
        self.q2_cube_obsticle_1 = SimpleCube(-7, 0.2, -7, q2_mat, (2.0, 1.5, 2.0))
        self.q2_cube_obsticle_2 = SimpleCube(-3, 0.2, -9, q2_mat, (2.0, 1.5, 2.0))
        self.q2_cube_obsticle_3 = SimpleCube(-9, 0.2, -3, q2_mat, (2.0, 1.5, 2.0))
        self.q2_cube_obsticle_4 = SimpleCube(-2, 0.2, -3.5, q2_mat, (4, 1.5, 5))

        # Quadrant 3
        self.q3_cube_obsticle_1 = SimpleCube(-8, 0.2, 6.5, q3_mat, (4, 1.5, 1))
        self.q3_cube_obsticle_2 = SimpleCube(-2.5, 0.2, 3, q3_mat, (3, 1.5, 2))
        self.q3_cube_obsticle_3 = SimpleCube(-0.5, 0.2, 4.5, q3_mat, (1, 1.5, 5))

        # Quadrant 4
        self.q4_cube_obsticle_1 = SimpleCube(8.5, 0.2, 1.5, q4_mat, (3, 1.5, 3))
        self.q4_cube_obsticle_2 = SimpleCube(6, 0.2, 2.5, q4_mat, (2, 1.5, 1))
        self.q4_cube_obsticle_3 = SimpleCube(0.5, 0.2, 4.5, q4_mat, (1, 1.5, 5))
        self.q4_cube_obsticle_4 = SimpleCube(6.5, 0.2, 8.5, q4_mat, (1, 1.5, 3))

        # Fill the list with instances of Cube() that can then be drawn
        self.cubes = []

        self.cubes.append(self.wall1)
        self.cubes.append(self.wall2)
        self.cubes.append(self.wall3)
        self.cubes.append(self.wall4)

        self.cubes.append(self.q1_cube_obsticle_1)
        self.cubes.append(self.q1_cube_obsticle_2)
        self.cubes.append(self.q1_cube_obsticle_3)

        self.cubes.append(self.q2_cube_obsticle_1)
        self.cubes.append(self.q2_cube_obsticle_2)
        self.cubes.append(self.q2_cube_obsticle_3)
        self.cubes.append(self.q2_cube_obsticle_4)

        self.cubes.append(self.q3_cube_obsticle_1)
        self.cubes.append(self.q3_cube_obsticle_2)
        self.cubes.append(self.q3_cube_obsticle_3)

        self.cubes.append(self.q4_cube_obsticle_1)
        self.cubes.append(self.q4_cube_obsticle_2)
        self.cubes.append(self.q4_cube_obsticle_3)
        self.cubes.append(self.q4_cube_obsticle_4)

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