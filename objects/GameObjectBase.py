from __future__ import annotations

class GameObject:
    """
        'GameObject' is a base class that each game object should inherit from,
        it contains common functions and variables that each game object MUST have
    """
    def __init__(self, x, y, z) -> None:
        self.set_position(x, y, z)
    
    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def update(self, delta_time) -> None:
        raise NotImplementedError("update is not implemented")
    
    def collision(self, player_pos) -> GameObject:
        # Implement the collision
        raise NotImplementedError("collision is not implemented")
    
    def draw(self) -> GameObject:
        # Implement the draw call
        raise NotImplementedError("draw is not implemented")
