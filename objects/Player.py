import json
import pygame
from pygame.locals import *
from maths.Material import Material
from maths.Point import Point
from maths.Vector import Vector

from .Camera import Camera
from CONSTANTS import *
from .Bullet import Bullet
from .GameObjectBase import GameObject

from random import randint

class Player(GameObject):
    def __init__(self, shader, position=Point(0,0,0), network = None) -> None:
        super().__init__(shader, position, Vector(0,0,0), Vector(0,0,0), Material())
        
        self.prev_position = position

        self.change_vec = Vector(position.x, position.y, position.z)
        self.velocity = Vector(0, 0, 0)

        self.camera = Camera(shader, position)
        self.first_mouse = True
        self.pitch = 0
        self.yaw = 0

        self.mouse_x = SCREEN_WIDTH / 2
        self.mouse_y = SCREEN_HEIGHT / 2

        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.sprint_key_down = False

        self.sensitivity = 20
        self.speed = 2

        self.firing = False
        self.network = network

        self.dead = False
        self.death_positions = {"position": Point(15, 5, 0), "lookat": Point(0, 1, 0)}

        # Bullets that the player shoots, so that he doesn't collide with his own bullets at the start
        self.owned_bullets = []

        # Respawn logic variables
        self.respawn_point_picked = False
        self.respawn_points = [Point(9, 0, 9), Point(-9, 0, -9), Point(-9, 0, 9), Point(9, 0, -9)]
        # Bezier points that the respawn will use, last one updates if user dies
        self.defined_bezier_points = [Point(15, 5, 0), Point(0, 10, 0), Point(9, 0, 9)]
        self.time = 0
    
    """
    Bezier formula for 3 points
    """
    def bezier(self):
        p1 = self.defined_bezier_points[0] * ((1-self.time) * (1-self.time))
        p2 = self.defined_bezier_points[1] * (2 * (1 - self.time) * self.time)
        p3 = self.defined_bezier_points[2] * (self.time * self.time)
        return p1 + p2 + p3

    
    """
    Shoot functions, spawns a bullet in the direction that the player is looking and gives it
    momentum to propell it out in that direction.
    
    Requires the main GameObjects class to add it into the scene 
    """
    def shoot(self, game_objects):
        self.firing = False
        direction_looking = self.camera.viewMatrix.get_matrix()
        direction_fire = Vector(direction_looking[2], -direction_looking[9], -direction_looking[0])
        bullet_pos = Point(self.position.x, -0.1, self.position.z)
        bullet_obj = Bullet(self.shader, bullet_pos, direction_fire)
        game_objects.add_object(bullet_obj)
        self.owned_bullets.append(bullet_obj)
        if self.network != None:
            self.network.send_on_next_update(bullet_obj)

    """
    Function to fire every update
    """
    def update(self, delta_time, game_objects):
        if self.dead:
            # If the player is dead, animate him respawning at a random position
            if self.respawn_point_picked == False:
                rand = randint(0, 3)
                self.defined_bezier_points[2] = self.respawn_points[rand]
                self.respawn_point_picked = True
            
            # Increment 'time' for the bezier path
            self.time += (delta_time / 4)
            if self.time >= 1:
                self.dead = False
                self.time = 1
            bezier_motion_pos = self.bezier()
            
            if self.time < 1:
                # Update the camera and shader matricies
                self.camera.set_position(bezier_motion_pos)
                self.camera.look_at(self.death_positions["lookat"])
                self.shader.use()
                self.shader.set_view_matrix(self.camera.viewMatrix.get_matrix())
                self.shader.set_eye_position(self.camera.viewMatrix.eye)
            else:
                # Last code to execude before player is alive again, resets lots of numbers
                self.shader.use()
                self.position = self.defined_bezier_points[2]
                self.prev_position = self.position
                self.camera = Camera(self.shader, self.defined_bezier_points[2])
                self.change_vec = Vector(self.position.x, self.position.y, self.position.z)
                self.respawn_point_picked = False
                self.time = 0
                self.first_mouse = True
        else:
            # Player is alive and can play normally
            self._mouse_controller(delta_time)
            self._keyboard_controller()

            self.move(delta_time)
            self.prev_position = self.position
            self.position = self.camera.viewMatrix.eye
            collision_objects = game_objects.check_collision(self)

            if collision_objects != []:
                self.collide(collision_objects)
                pass
            
            if self.firing:
                self.shoot(game_objects)
            
            for bullet in self.owned_bullets:
                if bullet.destroy == True:
                    self.owned_bullets.remove(bullet)
            
            self.shader.use()
            self.shader.set_view_matrix(self.camera.viewMatrix.get_matrix())
            self.shader.set_eye_position(self.camera.viewMatrix.eye)
    
    """
    Move function of the player, should fire every update
    """
    def move(self, delta_time):
        self.change_vec += self.velocity * delta_time * self.speed
        self.camera.move_position(self.change_vec)

    """
    Function that defines what should happen if the user is colliding with an object
    """
    def collide(self, collision_objects):
        for collision_object in collision_objects:
            if type(collision_object) == Bullet:
                if collision_object not in self.owned_bullets:
                    self.dead = True
            else:
                teleport_back = self.position
                if collision_object.collision_side[0] == 1 or collision_object.collision_side[1] == 1:
                    teleport_back.x = self.prev_position.x
                if collision_object.collision_side[2] == 1 or collision_object.collision_side[3] == 1:
                    teleport_back.z = self.prev_position.z
                self.camera.set_eye_position(teleport_back)

    """
    event_loop() should be fired for every pygame event, registers movement and firing
    """
    def event_loop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.firing = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                self.W_key_down = True
            if event.key == K_s:
                self.S_key_down = True
            if event.key == K_d:
                self.D_key_down = True
            if event.key == K_a:
                self.A_key_down = True
            if event.key == K_LSHIFT:
                self.sprint_key_down = True
        elif event.type == pygame.KEYUP:
            if event.key == K_w:
                self.W_key_down = False
            if event.key == K_s:
                self.S_key_down = False
            if event.key == K_d:
                self.D_key_down = False
            if event.key == K_a:
                self.A_key_down = False
            if event.key == K_LSHIFT:
                self.sprint_key_down = False

    """
    Function that handles what should happen if the user is pressing a key
    """
    def _keyboard_controller(self):

        if self.W_key_down:
            self.velocity.x = -1
        if self.S_key_down:
            self.velocity.x = 1
        if self.A_key_down:
            self.velocity.z = -1
        if self.D_key_down:
            self.velocity.z = 1
        if self.sprint_key_down:
            # TODO: Reduce speed, is fast for testing
            self.speed = 6
        else:
            self.speed = 2

        if (not self.W_key_down and not self.S_key_down):
            self.velocity.x = 0
        if (not self.D_key_down and not self.A_key_down):
            self.velocity.z = 0

    """
    Function that that moves the camera with the mouse and makes sure it stays within some range
    """
    def _mouse_controller(self, delta_time):
        if pygame.mouse.get_focused():
            pygame.mouse.set_pos((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            x_diff = (mouse_x - self.mouse_x) * self.sensitivity * delta_time
            y_diff = (mouse_y - self.mouse_y) * self.sensitivity * delta_time

            last_pitch = self.pitch
            last_yaw = self.yaw

            self.yaw += x_diff
            self.pitch += y_diff

            # Limit the camera's vertical range
            if self.pitch <= -89:
                self.pitch = -89
            if self.pitch >= 89:
                self.pitch = 89

            if self.yaw >= 360:
                self.yaw = 0
            if self.yaw <= -360:
                self.yaw = 0
            
            self.camera.pitch(self.pitch - last_pitch)
            self.camera.turn(last_yaw - self.yaw)

            if self.first_mouse:
                pygame.mouse.set_pos(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                self.camera.look(self.camera.position, Vector(0, 1, 0), Vector(0, 1, 0))
                self.pitch = 0
                self.yaw = 0
                self.first_mouse = False
    
    def get_dict(self):
        player_dict = {
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z
            }
        }
        return player_dict