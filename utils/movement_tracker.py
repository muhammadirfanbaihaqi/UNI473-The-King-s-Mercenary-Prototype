import time
import math

class MovementTracker:
    def __init__(self, persistence_time=180, max_distance=30):
        self.last_position = None
        self.last_movement_time = time.time()
        self.persistence_time = persistence_time
        self.max_distance = max_distance

    def update(self, new_position):
        now = time.time()

        if self.last_position is None:
            self.last_position = new_position
            self.last_movement_time = now
            return False

        dist = math.dist(new_position, self.last_position)
        if dist > self.max_distance:
            self.last_movement_time = now
            self.last_position = new_position
            return False
        else:
            if now - self.last_movement_time >= self.persistence_time:
                return True
            return False
