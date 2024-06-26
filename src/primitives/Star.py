from math import pi as PI, sin, cos, radians
from OpenGL.GL import *
from src.primitives.Primitive import Primitive

class Star(Primitive):
    def __init__(self, position, scale, color, n_corners):
        super().__init__(position, scale, color)
        self.n_corners = n_corners
    
    def draw(self):
        glPushMatrix()
        super().draw()
        theta = 0.0
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0.0, 0.0)        
        for i in range(0, self.n_corners+1):
            glVertex2f(cos(theta), sin(theta))
            theta += 2.0*PI/self.n_corners
            glVertex2f(cos(theta)/2.0, sin(theta)/2.0)
            theta += 2.0*PI/self.n_corners
        glEnd()
        glPopMatrix()