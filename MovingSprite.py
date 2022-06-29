import pyglet 
from pyglet.gl import *
from GameConstants import *
from math import copysign

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
        self.v_x = min([copysign(MAX_VEL, self.v_x), self.v_x + self.a_x \
            * 1/FRAME_RATE], key = abs)
        self.v_y = min([copysign(MAX_VEL, self.v_y), self.v_y + self.a_y \
            * 1/FRAME_RATE], key = abs)

    def update_pos(self):
        self.x += self.v_x * 1/FRAME_RATE
        self.y += self.v_y * 1/FRAME_RATE

    def update(self):
        self.update_pos()

    def inbounds(self):
        if not -self.width < self.x < SCREEN_WIDTH + self.width:
            return False
        if not -self.height < self.y < SCREEN_HEIGHT + self.height:
            return False
        return True

class Bullet(MovingSprite):

    def __init__(self, x=0, y=0, v_x = 0, v_y=BULLET_SPEED):
        super().__init__("Images/BulletCut.png", 2, x, y, v_x, v_y)
        self.remove = False