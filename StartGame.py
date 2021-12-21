from CONSTANTS import *

import pygame
from pygame.locals import *
from time import time

from OpenGL.GL import *
from OpenGL.GLU import *
from game_objects.Maze import Maze

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

        self.modelMatrix    = ModelMatrix()
        self.maze = Maze(-10, 0, -10)

        self.shader.set_light_position(Point(5, 10, 5))
        self.shader.set_light_diffuse(0.9, 0.9, 0.9)
        self.shader.set_light_specular(0.89, 0.89, 0.89)
        self.shader.set_material_specular(0.89, 0.89, 0.89)
        self.shader.set_material_shininess(25)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.angle += pi * delta_time * 0.01

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
    
        # Game objects that should be in the scene
        self.game_objects = GameObjects()
        self.game_objects.add_object(self.floor)
        self.game_objects.add_object(self.cube1)
        self.game_objects.add_object(self.maze)
        self.game_objects.draw_objects(self.modelMatrix, self.shader, True)

    def display(self):
        glClearColor(66/255, 135/255, 245/255, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_CLAMP)
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Update player the camera
        self.player.display()

        # Draw all objects within game_objects
        self.game_objects.draw_objects(self.modelMatrix, self.shader, True)
        
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