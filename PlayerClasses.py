from pyglet.window import key
from MovingSprite import *

class Player():

    def __init__(self, image):
        self.ship_sprite = Ship(image)
        self.bullets = []
        self.hp = PLAYER_HP

    def update(self):

        if self.ship_sprite.key_handler[key.SPACE]:
            if not self.ship_sprite.bullet_cooldown > 0:
                self.ship_sprite.bullet_cooldown = BULLET_COOLDOWN
                new_bullet = Bullet(self.ship_sprite.x + \
                    self.ship_sprite.width / 2, self.ship_sprite.y \
                    + self.ship_sprite.height)
                new_bullet.x -= new_bullet.width / 2
                self.bullets.append(new_bullet)
        
        self.ship_sprite.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.inbounds()\
            and not bullet.remove]
        for bullet in self.bullets:
            bullet.update()

    def on_draw(self):
        self.ship_sprite.draw()
        for bullet in self.bullets:
            bullet.draw()

class Ship(MovingSprite):

    def __init__(self, image):

        MovingSprite.__init__(self, image, MAG_FACTOR, 250 - 22, 25)

        self.a_x = 0
        self.a_y = 0
        self.bullet_cooldown = 0

        self.key_handler = key.KeyStateHandler()
        
    def update_accel(self):
        if self.a_x != 0:
            self.a_x = self.a_x / 2
        if self.a_y != 0:
            self.a_y = self.a_y / 2       

    def update(self):
        self.bullet_cooldown -= 1
        self.update_vel()
        self.update_accel()
        if self.key_handler[key.RIGHT]:
            self.a_x = MAX_ACCEL
        if self.key_handler[key.LEFT]:
            self.a_x = -MAX_ACCEL
        if self.key_handler[key.UP]:
            self.a_y = MAX_ACCEL
        if self.key_handler[key.DOWN]:
            self.a_y = -MAX_ACCEL

        self.update_pos()
