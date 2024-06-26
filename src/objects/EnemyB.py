from random import uniform
from src.primitives.Eneagon import Eneagon
from src.objects.Projectile import Projectile
from glm import vec3, normalize

class EnemyB(Eneagon):
    def __init__(self, x):
        super().__init__(
            vec3(x, 8, 0), # Position
            vec3(1.5, 1.5, 1), # Scale
            (1, 0, 0), # Color
            6 # N_sides
        )
        self.velocity = 0.05*normalize(vec3(uniform(-1, 1), -1, 0))
        self.scale_delta = 0.01
        self.fireGauge = 0
        self.fireGaugeFull = 200
        
    def updatePosition(self):
        self.scale.x += self.scale_delta
        self.scale.y += self.scale_delta
        if self.scale.x >= 2 or self.scale.x <= 0.9:
            self.scale_delta *= -1
        self.position += self.velocity
        
    def fire(self, game):
        if self.fireGauge <= 0:
            game.projectiles.append(
                Projectile(self.position.x, self.position.y, True)
            )
            self.fireGauge = self.fireGaugeFull