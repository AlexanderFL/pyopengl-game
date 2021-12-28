import json
import pygame
from pygame.locals import *
from common_game_maths.Point import Point
from common_game_maths.Vector import Vector
from .Camera import Camera
from CONSTANTS import *
from .Bullet import Bullet
from .GameObjectBase import GameObject

class Player(GameObject):
    def __init__(self, shader, position=Point(0,0,0), network = None) -> None:
        self.shader = shader
        self.prev_position = position
        self.position = position

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
    

    def update(self, delta_time, game_objects):
        self._mouse_controller(delta_time)
        self._keyboard_controller()

        self.move(delta_time)
        self.prev_position = self.position
        self.position = self.camera.viewMatrix.eye
        collision_objects = game_objects.check_collision(self.position)

        if collision_objects != []:
            pass
            #self.collide(collision_objects)
        
        if self.firing:
            self.firing = False
            direction_looking = self.camera.viewMatrix.get_matrix()
            direction_fire = Vector(direction_looking[2], -direction_looking[9], -direction_looking[0])
            bullet_pos = Point(self.position.x, -0.1, self.position.z)
            bullet_obj = Bullet(self.shader, bullet_pos, direction_fire)
            game_objects.add_object(bullet_obj)
            if self.network != None:
                self.network.send_on_next_update(bullet_obj)
        
        self.shader.use()
        self.shader.set_view_matrix(self.camera.viewMatrix.get_matrix())
        self.shader.set_eye_position(self.camera.viewMatrix.eye)
        
    def move(self, delta_time):
        self.change_vec += self.velocity * delta_time * self.speed
        self.camera.move_position(self.change_vec)
    
    def collide(self, collision_objects):
        for collision_object in collision_objects:
            teleport_back = self.position
            if collision_object.collision_side[0] == 1 or collision_object.collision_side[1] == 1:
                teleport_back.x = self.prev_position.x
            if collision_object.collision_side[2] == 1 or collision_object.collision_side[3] == 1:
                teleport_back.z = self.prev_position.z
            self.camera.set_position(teleport_back)

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