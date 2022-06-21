from turtle import width
import pyglet 
from pyglet.window import key
from pyglet.gl import *
from math import copysign
from GameConstants import *

glEnable(GL_TEXTURE_2D)

class MyWindow(pyglet.window.Window):

    def __init__(self, player):
        super(MyWindow, self).__init__(width = SCREEN_WIDTH,\
            height = SCREEN_HEIGHT)
        self.push_handlers(player.ship_sprite.key_handler)
        self.player = player

    def update(self, _):
        self.player.update()

    def on_draw(self):
        self.clear()
        self.player.on_draw()

class Player():

    def __init__(self, image):
        self.ship_sprite = Ship(image)
        self.bullets = []
        self.hp = 10

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
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.inbounds()]

    def on_draw(self):
        self.ship_sprite.draw()
        for bullet in self.bullets:
            bullet.draw()

class MovingSprite(pyglet.sprite.Sprite):

    def __init__(self, image, mag = 1, x = 0, y = 0, v_x = 0, v_y = 0):

        image_base = pyglet.image.load(image)
        image_texture = image_base.get_texture()
        if mag != 1:
            #OpenGL magic to allow resizing without blurring
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
            image_texture.width = image_texture.width * mag
            image_texture.height = image_texture.height * mag
        
        pyglet.sprite.Sprite.__init__(self, image_texture, x, y)

        self.v_x = v_x
        self.v_y = v_y

    def update_vel(self):
        self.v_x = min([copysign(MAX_VEL, self.v_x), self.v_x + self.a_x * 1/FRAME_RATE], key = abs)
        self.v_y = min([copysign(MAX_VEL, self.v_y), self.v_y + self.a_y * 1/FRAME_RATE], key = abs)

    def update_pos(self):
        self.x += self.v_x * 1/FRAME_RATE
        self.y += self.v_y * 1/FRAME_RATE

    def inbounds(self):
        if not -self.width < self.x < SCREEN_WIDTH + self.width:
            return False
        if not -self.height < self.y < SCREEN_HEIGHT + self.height:
            return False
        return True

class Bullet(MovingSprite):

    def __init__(self, x=0, y=0, v_x = 0, v_y=BULLET_SPEED):
        super().__init__("Images/BulletCut.png", 3, x, y, v_x, v_y)

    def update(self):
        self.update_pos()

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


if __name__ == "__main__":  

    player = Player("Images/ShipCut.png")
    window = MyWindow(player)
    pyglet.clock.schedule_interval(window.update, 1/240)
    pyglet.app.run()




