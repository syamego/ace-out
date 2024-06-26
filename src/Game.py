from random import random, uniform
from math import sqrt
from src.primitives.Heart import Heart
from src.primitives.Shield import Shield
from src.objects.Ship import Ship
from src.objects.EnemyA import EnemyA
from src.objects.EnemyB import EnemyB
from src.objects.Background import Background
from src.textures.Texture import Texture
from OpenGL.GL import *
from OpenGL.GLUT import *
from glm import vec3

class Game:
    def __init__(self):
        # Startup
        glClearColor(0, 0, 0, 1)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_TEXTURE_2D)
        Texture.texs.update({
            'ship': Texture('src/textures/ships/player_ship.png'),
            'bullet': Texture('src/textures/bullets/bullet.png'),
            'scenario': Texture('src/textures/bgs/space.png', GL_REPEAT),
        })
        
        # Internals
        self.FPS = 60
        self.front = False
        self.back = False
        self.left = False
        self.right = False

        self.windowH = 80
        self.windowW = 80
        self.sceneH = 20
        self.sceneW = 20

        # Status
        self.HP = 3
        self.upgrades = 0
        
        # Objects
        self.ship = Ship()
        self.projectiles = []
        self.enemies = []
        self.background = Background(Texture.texs['scenario'].texId, self.sceneW, self.sceneH)


    def keyboardSpecial(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.left = True
        elif key == GLUT_KEY_RIGHT:
            self.right = True

    def keyboardSpecialUp(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.left = False
        elif key == GLUT_KEY_RIGHT:
            self.right = False

    def reshape(self, w, h):
        self.windowW = w
        self.windowH = h
        self.sceneW = self.sceneH * w / h

        self.background.width = self.sceneW
        glViewport(0, 0, w, h)

    def timer(self, v):
        glutTimerFunc(int(1000 / self.FPS), self.timer, 0)
        
        # Spawn enemies
        if random() < 0.005:
            posX = uniform(-self.sceneW/2+1.15, self.sceneW/2-1.15)
            if random() < 0.45:
                self.enemies.append(EnemyA(posX))
            else:
                self.enemies.append(EnemyB(posX))
        
        # Update positions
        self.ship.updatePosition(self)

        for projectil in self.projectiles:
            projectil.updatePosition()
            if (projectil.position.y > self.sceneH/2) or (projectil.position.y < -self.sceneH/2):
                self.projectiles.remove(projectil)
        
        for enemy in self.enemies:
            enemy.updatePosition()
            if enemy.position.y < -self.sceneH/2-2 or abs(enemy.position.x) > self.sceneW/2+2:
                self.enemies.remove(enemy)
        self.background.updatePosition()

        # Firing
        self.ship.fireGauge -= 1
        self.ship.fire(self)
        for enemy in self.enemies:
            enemy.fireGauge -= 1
            enemy.fire(self)
        
        # Collision detection
        for projectile in self.projectiles:
            if not projectile.isEnemy:
                for enemy in self.enemies:
                    d = sqrt((projectile.position.x-enemy.position.x)**2 + (projectile.position.y-enemy.position.y)**2)
                    if d <= 0.9:
                        self.upgrades = min(self.upgrades+1, 10)
                        self.enemies.remove(enemy)
                        self.projectiles.remove(projectile)
                        break
            else:
                d = sqrt((projectile.position.x-self.ship.position.x)**2 + (projectile.position.y-self.ship.position.y)**2)
                if d < 0.5:
                    self.projectiles.remove(projectile)
                    if self.upgrades > 0:
                        self.upgrades -= 1
                    else:
                        self.HP -= 1
                        if self.HP == 0:
                            glutLeaveMainLoop()

        glutPostRedisplay()

    def run(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.sceneW / 2, self.sceneW / 2, -self.sceneH / 2, self.sceneH / 2, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Apply upgrades
        self.ship.fireGaugeFull = 100-self.upgrades*5
        self.ship.velocity = (0.2+0.03*self.upgrades)*vec3(1, 0, 0)

        # Drawings
        self.background.draw()
        for projectile in self.projectiles:
            projectile.draw()

        self.ship.draw()
        for enemy in self.enemies:
            enemy.draw()
        
        for i in range(self.HP):
            Heart(
                vec3(-self.sceneW/2+1.15+i*0.6, self.sceneH/2-1.15, 1),
                vec3(0.5, 0.5, 1),
                (1, 0, 1)
            ).draw()
        for i in range(self.upgrades):
            Shield(
                vec3(self.sceneW/2-1.15-i*0.6, self.sceneH/2-1.15, 1),
                vec3(0.5, 0.5, 1),
                (0, 1, 1)
            ).draw()
        
        glutSwapBuffers()
