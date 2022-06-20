import pyglet 
from pyglet.window import key
from pyglet.gl import *
from math import copysign
glEnable(GL_TEXTURE_2D)

class MyWindow(pyglet.window.Window):

    def __init__(self, image):
        super(MyWindow, self).__init__()

        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)

        self.ship_sprite = Ship(image)

    def on_draw(self):
        self.clear()
        self.ship_sprite.draw()

    def update(self, _):
        self.ship_sprite.update_vel()
        self.ship_sprite.update_accel()
        if self.key_handler[key.RIGHT]:
            self.ship_sprite.a_x = 300
        if self.key_handler[key.LEFT]:
            self.ship_sprite.a_x = -300
        if self.key_handler[key.UP]:
            self.ship_sprite.a_y = 300
        if self.key_handler[key.DOWN]:
            self.ship_sprite.a_y = -300
        self.ship_sprite.update_pos()

class Ship(pyglet.sprite.Sprite):

    def __init__(self, image):

    
        ship_image_base = pyglet.image.load(image)
        ship_image = ship_image_base.get_texture()

        #OpenGL magic to allow resizing without blurring
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 

        ship_image.width = 45
        ship_image.height = 60

        pyglet.sprite.Sprite.__init__(self, ship_image)

        self.x = 300
        self.y = 300

        self.v_x = 0
        self.v_y = 0

        self.a_x = 0
        self.a_y = 0

    def update_accel(self):
        if self.a_x != 0:
            self.a_x = self.a_x / 2
        if self.a_y != 0:
            self.a_y = self.a_y / 2       

    def update_vel(self):
        self.v_x = min([copysign(75, self.v_x), self.v_x + self.a_x * 1/60], key = abs)
        self.v_y = min([copysign(75, self.v_y), self.v_y + self.a_y * 1/60], key = abs)

    def update_pos(self):
        self.x += self.v_x * 1/60
        self.y += self.v_y * 1/60

if __name__ == "__main__":  

    window = MyWindow("Images/ShipCut.png")
    pyglet.clock.schedule_interval(window.update, 1/60)
    pyglet.app.run()




