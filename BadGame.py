import pyglet 
from pyglet.window import key
from pyglet.gl import *
from math import copysign
from GameConstants import *

glEnable(GL_TEXTURE_2D)

class MyWindow(pyglet.window.Window):

    def __init__(self, handler):
        super(MyWindow, self).__init__(width = SCREEN_WIDTH,\
            height = SCREEN_HEIGHT)
        self.push_handlers(handler.player.ship_sprite.key_handler)
        self.handler = handler

    def update(self, _):
        self.handler.update()

    def on_draw(self):
        self.clear()
        self.handler.on_draw()

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

    def inbounds(self):
        if not -self.width < self.x < SCREEN_WIDTH + self.width:
            return False
        if not -self.height < self.y < SCREEN_HEIGHT + self.height:
            return False
        return True

class Bullet(MovingSprite):

    def __init__(self, x=0, y=0, v_x = 0, v_y=BULLET_SPEED):
        super().__init__("Images/BulletCut.png", 3, x, y, v_x, v_y)
        self.remove = False

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

class EnemyShip(MovingSprite):
    
    def __init__(self, image, mag = 1, x = 0, y = 0, v_x = 0, v_y = 0):

        MovingSprite.__init__(self, image, mag, x, y, v_x, v_y)

        self.hp = 1

class RoundShip(EnemyShip):

    def __init__(self, x = 0, y = 0, v_x = 0, v_y = 0, x_rot = 0, y_rot = 0, speed = 0):
        EnemyShip.__init__(self, ROUND_SHIP_DIR, 2, x, y, v_x, v_y)
        self.x_rot = x_rot 
        self.y_rot = y_rot
        self.speed_sq = speed**2

    def update_accel(self):
        dist_squared = (self.x - self.x_rot)**2 + (self.y - self.y_rot)**2
        accel_mag = self.speed_sq / dist_squared 
        self.a_x = accel_mag * (self.x_rot - self.x)
        self.a_y = accel_mag * (self.y_rot - self.y)

    def update_vel(self):
        self.v_x += self.a_x * 1/FRAME_RATE
        self.v_y += self.a_y * 1/FRAME_RATE

    def update(self):
        self.update_accel()
        self.update_vel()
        self.update_pos()

class GameHandler():

    def __init__(self):
        
        self.player = Player(SHIP_DIR)
        self.enemy_ships = []
        self.player_bullets = []
        self.enemy_bullets = []

    def check_all_collisions(self):
        self.enemy_ships = [ship for ship in self.enemy_ships if ship.hp != 0]
        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if not \
            bullet.remove]
        self.player_ships_check()
        self.bullet_player_check()
        self.bullet_ships_check()

    def check_collision(self, sprite1, sprite2):
        dist_sq = (sprite1.x - sprite2.x)**2 + (sprite1.y - sprite2.y)**2
        threshold = max(sprite1.width**2 + sprite2.height**2, sprite1.height**2\
            + sprite2.width**2)
        if dist_sq <= threshold:
            return True
        return False

    def player_ships_check(self):
        for ship in self.enemy_ships:
            if self.check_collision(self.player.ship_sprite, ship):
                self.player.hp -= 1
                ship.hp -= 1
        
    def bullet_player_check(self):
        for bullet in self.enemy_bullets:
            if self.check_collision(self.player.ship_sprite, bullet):
                self.player.hp -= 1
                bullet.remove = True
                
    def bullet_ships_check(self):
        for bullet in self.enemy_bullets:
            for ship in self.enemy_ships:
                if self.check_collision(ship, bullet):
                    self.ship.hp -= 1
                    bullet.remove = True
        
        for bullet in self.player_bullets:
            for ship in self.enemy_ships:
                if self.check_collision(ship, bullet):
                    ship.hp -= 1
                    bullet.remove = True
        
    def update(self):
        self.check_all_collisions()
        for bullet in self.enemy_bullets:
            bullet.update()
        for ship in self.enemy_ships:
            ship.update()
        self.player.update()
        self.player_bullets = self.player.bullets

    def on_draw(self):
        self.player.on_draw()
        for ship in self.enemy_ships:
            ship.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()

if __name__ == "__main__":  

    handler = GameHandler()
    window = MyWindow(handler)
    handler.enemy_ships.append(RoundShip(250, 600, 0, -450, 600, 600, 450))
    pyglet.clock.schedule_interval(window.update, 1/240)
    pyglet.app.run()




