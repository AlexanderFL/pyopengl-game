from OpenGL import GL
from CONSTANTS import *

import pygame
from pygame.locals import *
from time import time

from OpenGL.GL import *
from OpenGL.GLU import *
from game_objects.Level1 import Level1

from shaders.Shaders import Shader3D
from shaders.Crosshair import ShaderCrosshair
from maths.Matricies import *

from game_objects.GameObjects import GameObjects
from game_objects.Floor import Floor
from game_objects.Player import Player
from game_objects.Cube import Cube
from objects.Cross import Crosshair

from game_objects.Bullet import Bullet
from networking.Networking import Networking
import asyncio
import sys

from game_objects.ObjLoader import load_obj_file

class StartGame:
    def __init__(self):
        self.is_networking = False

        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.mouse.set_visible(False)

        if self.is_networking:
            self.server = Networking('127.0.0.1', 7532)
            if self.server.connect() == -1:
                self.is_networking = False
        
        self.shader = Shader3D()
        self.shader.use()

        self.crosshair = Crosshair()
        self.crosshairshader = ShaderCrosshair()

        self.modelMatrix    = ModelMatrix()
        self.maze = Level1(-10, 0, -10)

        self.shader.set_light_position(Point(5, 0, 4))
        self.shader.set_light_diffuse(0.9, 0.89, 0.74)
        self.shader.set_light_specular(0.89, 0.89, 0.89)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0
        self.radius = 3
        self.light_x = self.radius
        self.light_z = self.radius

        self.fr_ticker = 0
        self.fr_sum = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        self.game_objects.update_objects(delta_time)
        self.player.update(delta_time, self.game_objects)
        
        if self.is_networking:
            self.server.send_on_next_update(self.player)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.server.update())

    def initializeGameObjects(self):
        self.floor = Floor(0, -0.5, 0)
        crate_texture = sys.path[0] + "\\game_objects\\textures\\Crate.png"
        self.cube1 = Cube(0, 0.5, 0, (2, 2, 2), texture_path=crate_texture)
        if self.is_networking:
            self.player = Player(self.shader, Point(8, 0, 0), self.server)
        else:
            self.player = Player(self.shader, Point(8, 0, 0), None)
        
        obj_file_path = sys.path[0] + "\\models"
        obj_file_name = "simple_box.obj"
        self.cube_obj = load_obj_file(obj_file_path, obj_file_name)
        print(self.cube_obj.mesh_materials)
    
        # Game objects that should be in the scene
        self.game_objects = GameObjects()
        self.game_objects.add_object(self.floor)
        self.game_objects.add_object(self.cube1)
        self.game_objects.add_object(self.maze)

    def display(self):
        self.player.camera.projection_matrix.set_perspective(3.14159/2, SCREEN_WIDTH/SCREEN_HEIGHT, 0.001, 100)
        glClearColor(66/255, 135/255, 245/255, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_CLAMP)
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Update player the camera
        self.shader.use()
        self.player.display()

        # Draw all objects within game_objects
        self.game_objects.draw_objects(self.modelMatrix, self.shader, True)

        self.shader.set_eye_position(self.player.camera.viewMatrix.eye)
        
        self.modelMatrix.push_matrix()
        self.modelMatrix.load_identity()
        self.modelMatrix.add_translation(5, 0.15, 0)
        self.modelMatrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.modelMatrix.matrix)
        self.cube_obj.draw(self.shader)
        self.modelMatrix.pop_matrix()

        self.crosshairshader.use()
        self.player.camera.projection_matrix.set_orthographic(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, 0.01, 10)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.crosshair.draw()
        
        pygame.display.flip()

    def loop(self):
        exiting = False
        self.initializeGameObjects()
        
        while not exiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITTING")
                    self.server.send("disconnect")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("ESCAPING")
                        exiting = True
                self.player.event_loop(event)

            self.update()
            self.display()
        
        # End of game loop
        pygame.quit()
    
    def start(self):
        if self.is_networking:
            if self.server.connected:
                self.loop()
        else:
            self.loop()

if __name__ == "__main__":
    s = StartGame()
    s.start()