from MovingSprite import *
from math import sqrt, atan2, cos, sin, pi

class EnemyShip(MovingSprite):
    
    def __init__(self, image, mag = 1, x = 0, y = 0, v_x = 0, v_y = 0):

        MovingSprite.__init__(self, image, mag, x, y, v_x, v_y)

        self.hp = 1
        self.cooldown = ENEMY_SHOT_COOLDOWN
        self.speed = sqrt(self.v_x**2 + self.v_y**2)

    def targeted_shot(self, player_x, player_y):
        
        phi = atan2(player_y - self.y, player_x - self.x)
        new_bullet = Bullet(self.x, self.y, ENEMY_BULLET_SPEED * cos(phi), \
                            ENEMY_BULLET_SPEED * sin(phi))
        for i in range(30):
            new_bullet.update()
        return new_bullet

    def velocity_shot(self):
        #Returns a bullet whose velocity is in the same direction as the 
        #ship's. Resolved using similar triangles.
        similarity_factor = ENEMY_BULLET_SPEED / self.speed
        new_bullet = Bullet(self.x + self.width * copysign(1, self.v_x), \
            self.y + self.height * copysign(1, self.v_y), similarity_factor * \
            self.v_x, similarity_factor * self.v_y)
        return new_bullet

    def shoot_tick(self, player_x, player_y):
        self.cooldown -= 1
        if not self.cooldown:
            self.cooldown = ENEMY_SHOT_COOLDOWN
            return [self.velocity_shot()]
        return []

    def shoot_tick_targeted(self, player_x, player_y):
        self.cooldown -= 1
        if not self.cooldown:
            self.cooldown = ENEMY_SHOT_COOLDOWN
            return [self.targeted_shot(player_x, player_y)]
        return []

class RoundShip(EnemyShip):

    #Enemy ship which rotates at constant speed at about some point. Target
    #off screen will allow curving in ship.

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

    def shoot_tick(self, player_x, player_y):
        return self.shoot_tick_targeted(player_x, player_y)

class Sweeper(EnemyShip):

    #Enemy ship which moves in a straight line at constant velocity.

    def __init__(self, x = 0, y = 0, v_x = 0, v_y = 0):
        EnemyShip.__init__(self, SWEEPER_SHIP_DIR, 5, x, y, v_x, v_y)

        self.rotation = - atan2(v_x, v_y) * 180 / pi

class ZigZagger(EnemyShip):

    def __init__(self, x=0, y=0, v_x=0, v_y=0, vertical = True):
        #Vertical - if true, the ship keeps its vertical velocity and has 
        #changes to its x-vel instead.
        EnemyShip.__init__(self, ZIGZAGGER_SHIP_DIR, 2, x, y, v_x, v_y)

        self.direction_cooldown = ZIGZAGGER_COOlDOWN
        self.vertical = vertical

    def update_vel(self):
        self.direction_cooldown -= 1
        # self.rotation += 180 / ZIGZAGGER_COOlDOWN
        if self.direction_cooldown < 1:
            if self.vertical:
                self.v_x = - self.v_x
            else:
                self.v_y = - self.v_y
            self.direction_cooldown = ZIGZAGGER_COOlDOWN

    def update(self):
        self.update_vel()
        self.update_pos()     