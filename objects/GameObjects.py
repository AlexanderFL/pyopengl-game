from objects.GameObjectBase import GameObject
from typing import List

class GameObjects:
    """
        The 'GameObjects' class contains "almost" every GameObject within the scene
    """
    def __init__(self):
        self.game_objects = []
    
    def add_object(self, object) -> None:
        # Add an object to the scene
        self.game_objects.append(object)
    
    def remove_object(self, object) -> None:
        # Remove object from the scene
        self.game_objects.remove(object)
    
    def draw_objects(self, modelMatrix, shader, update_shader=False) -> None:
        # Draw all of the objects
        for object in self.game_objects:
            object.draw(modelMatrix, shader, update_shader)
    
    def update_objects(self, delta_time):
        # Update all objects in the scene
        for object in self.game_objects:
            object.update(delta_time, self)
            if object.destroy == True:
                self.remove_object(object)
        
    def check_collision(self, position) -> List[GameObject]:
        # Check if any object is colliding with the player
        collision_objects = []
        for object in self.game_objects:
            colliding_object = object.collision(position)
            if colliding_object != None:
                if type(colliding_object) == list:
                    for obj in colliding_object:
                        collision_objects.append(obj)
                else:
                    collision_objects.append(colliding_object)
        return collision_objects
