from PlayerClasses import Player
from GameConstants import *

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
                    ship.hp -= 1
                    bullet.remove = True
        
        for bullet in self.player_bullets:
            for ship in self.enemy_ships:
                if self.check_collision(ship, bullet):
                    ship.hp -= 1
                    bullet.remove = True
        
    def update(self):
        self.check_all_collisions()
        for ship in self.enemy_ships:
            ship.update()
            new_bullet = ship.shoot_tick(self.player.ship_sprite.x, self.player.ship_sprite.y)
            self.enemy_bullets += new_bullet
        for bullet in self.enemy_bullets:
            bullet.update()

        self.player.update()
        self.player_bullets = self.player.bullets

    def on_draw(self):
        self.player.on_draw()
        for ship in self.enemy_ships:
            ship.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()