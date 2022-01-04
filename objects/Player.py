import json, pygame
from typing import List
from pygame.locals import *
from random import randint

from maths.Material import Material
from maths.Point import Point
from maths.Vector import Vector
from .GameObjectBase import GameObject
from .GameObjects import GameObjects
from .Camera import Camera
from .Bullet import Bullet
from CONSTANTS import *


class Player(GameObject):
    """
    'Player' is a big class that handles all of the player interaction with the game,
    movement, shooting, looking around and collision logic
    """
    def __init__(self, shader, position=Point(0,0,0)) -> None:
        super().__init__(shader, position, Vector(0,0,0), Vector(0,0,0), Material())

        # Camera object
        self.camera = Camera(shader, position)

        # Mouse position and variables
        self.mouse_x = G_SCREEN_WIDTH / 2
        self.mouse_y = G_SCREEN_HEIGHT / 2
        self.first_mouse = True
        self.pitch = 0
        self.yaw = 0

        # Keyboard variables
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.sprint_key_down = False
        self.sensitivity = 20
        self.speed = 2
        self.firing = False
        self.velocity = Vector(0, 0, 0)
        self.prev_position = position
        self.change_vec = Vector(position.x, position.y, position.z)

        # Will recieve from the server on connection
        self.network_uid = None

        # Bullets that the player shoots, so that he doesn't collide with his own bullets at the start
        self.owned_bullets = []

        # Respawn logic variables
        self.dead = False
        self.respawn_point_picked = False
        self.respawn_points = [Point(9, 0, 9), Point(-9, 0, -9), Point(-9, 0, 9), Point(9, 0, -9)]
        # Bezier points that the respawn will use, last one updates if user dies
        self.defined_bezier_points = [Point(15, 5, 0), Point(0, 10, 0), Point(9, 0, 9)]
        self.time = 0
    
    def bezier(self):
        """
        bezier() is the bezier formula for 3 points. Maybe it doesn't belong in the player
        class but whatever
        """
        p1 = self.defined_bezier_points[0] * ((1-self.time) * (1-self.time))
        p2 = self.defined_bezier_points[1] * (2 * (1 - self.time) * self.time)
        p3 = self.defined_bezier_points[2] * (self.time * self.time)
        return p1 + p2 + p3

    
    def shoot(self, game_objects):
        """
        shoot() spawns a bullet in the direction that the player is looking and gives it
        momentum to propell it out in that direction.
        
        @param 'game_objects' - the object that handles all of the game objects
        """
        self.firing = False
        direction_looking = self.camera.viewMatrix.get_matrix()
        direction_fire = Vector(direction_looking[2], -direction_looking[9], -direction_looking[0])
        bullet_pos = Point(self.position.x, -0.1, self.position.z)
        bullet_obj = Bullet(self.shader, bullet_pos, direction_fire)
        game_objects.add_object(bullet_obj)
        self.owned_bullets.append(bullet_obj)

    def update(self, delta_time, game_objects : GameObjects):
        """
        update() is, well... executed every update

        @param 'delta_time' - time difference between the previous and current frame
        @param 'game_objects' - the object that handles all of the game objects
        """
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
                self.camera.look_at(Point(0, 1, 0))
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
                # yaw has to be set before player respawns for correct network information
                if self.position.x == -9 and self.position.z == -9:
                    self.yaw = 45
                elif self.position.x == 9 and self.position.z == -9:
                    self.yaw = 315
                elif self.position.x == -9 and self.position.z == 9:
                    self.yaw = 135
                elif self.position.x == 9 and self.position.z == 9:
                    self.yaw = 225
        else:
            # Player is alive, can move and play normally
            self.rotation.y = -self.yaw
            self.move(delta_time)
            self.prev_position = self.position
            self.position = self.camera.viewMatrix.eye

            self._mouse_controller(delta_time)
            self._keyboard_controller()

            # Check all game objects for collisions
            collision_objects = game_objects.check_collision(self)

            if collision_objects != []:
                self.collide(collision_objects)
            
            # Shooting logic
            if self.firing:
                self.shoot(game_objects)
            
            for bullet in self.owned_bullets:
                if bullet.destroy == True:
                    self.owned_bullets.remove(bullet)
            
            # Set shader variables for correct lighting
            self.shader.use()
            self.shader.set_view_matrix(self.camera.viewMatrix.get_matrix())
            self.shader.set_eye_position(self.camera.viewMatrix.eye)
    
    def move(self, delta_time):
        """
        move() moves the player around, what more do you want?

        @param 'delta_time' - time difference between the previous and current frame
        """
        self.change_vec += self.velocity * delta_time * self.speed
        self.camera.move_position(self.change_vec)

    def collide(self, collision_objects : List[GameObject]):
        """
        collide() defines what should happen if the user is colliding with an object

        @param 'collision_objects' - List of objects that the user is currently colliding with
        """
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

    def event_loop(self, event):
        """
        event_loop() should be fired for every pygame event, registers movement and firing

        @param 'event' - the event object from pygame
        """
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
        """
        _keyboard_controller() handles what should happen if the user is pressing a key
        """

        if self.W_key_down:
            self.velocity.x = -1
        if self.S_key_down:
            self.velocity.x = 1
        if self.A_key_down:
            self.velocity.z = -1
        if self.D_key_down:
            self.velocity.z = 1
        if self.sprint_key_down:
            self.speed = 6
        else:
            self.speed = 2

        if (not self.W_key_down and not self.S_key_down):
            self.velocity.x = 0
        if (not self.D_key_down and not self.A_key_down):
            self.velocity.z = 0

    def _mouse_controller(self, delta_time):
        """
        _mouse_controller() moves the camera with the mouse and makes sure it stays within some range

        @param 'delta_time' - time difference between the previous and current frame
        """
        if pygame.mouse.get_focused():
            # Keeps the mouse stuck in the center of the screen
            pygame.mouse.set_pos((G_SCREEN_WIDTH/2, G_SCREEN_HEIGHT/2))

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

            if self.yaw > 360:
                self.yaw = 0
            if self.yaw < 0:
                self.yaw = 360
            
            # Tell the camera to pitch and turn
            self.camera.pitch(self.pitch - last_pitch)
            self.camera.turn(last_yaw - self.yaw)

            if self.first_mouse:
                # Setting some initial variables if the user is entering the screen for the first time
                pygame.mouse.set_pos(G_SCREEN_WIDTH/2, G_SCREEN_HEIGHT/2)
                self.camera.look(self.camera.position, Vector(0, 1, 0), Vector(0, 1, 0))
                self.pitch = 0
                self.first_mouse = False

                if self.position.x == -9 and self.position.z == -9:
                    self.yaw = 45
                elif self.position.x == 9 and self.position.z == -9:
                    self.yaw = 135
                elif self.position.x == -9 and self.position.z == 9:
                    self.yaw = 315
                elif self.position.x == 9 and self.position.z == 9:
                    self.yaw = 225
    
    def serialize(self):
        """
        serialize() puts the player in a short dict with information that can be
        sent over the network.
        """
        bullet_list = []
        for bullet in self.owned_bullets:
            bullet_list.append(bullet.to_dict())
        player_dict = {
            "uid": self.network_uid,
            "data": {
                "position": {
                    "x": self.position.x,
                    "y": self.position.y,
                    "z": self.position.z
                },
                "rotation": {
                    "x": self.rotation.x,
                    "y": self.rotation.y,
                    "z": self.rotation.z,
                },
                "dead": self.dead,
                "bullets": bullet_list,
            }
        }
        return json.dumps(player_dict)