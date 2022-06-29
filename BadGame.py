import pyglet 
from pyglet.window import key
from pyglet.gl import *
from GameConstants import *
from Enemies import RoundShip, ZigZagger, Sweeper
from GameController import GameHandler

#The biggest OOP mess Ive ever written...

glEnable(GL_TEXTURE_2D)

class MyWindow(pyglet.window.Window):

    def __init__(self, handler):
        super(MyWindow, self).__init__(width = SCREEN_WIDTH,\
            height = SCREEN_HEIGHT)
        self.push_handlers(handler.player.ship_sprite.key_handler) #Cursed
        self.handler = handler
        self.player_hp_label = pyglet.text.Label("HP: " + str(handler.player.hp), \
            font_name='Times New Roman', font_size=12, x=10, y=10)

    def update(self, _):
        self.handler.update()
        self.player_hp_label.text = "HP: " + str(handler.player.hp)

    def on_draw(self):
        self.clear()
        self.handler.on_draw()
        self.player_hp_label.draw()

if __name__ == "__main__":  

    handler = GameHandler()
    window = MyWindow(handler)
    handler.enemy_ships.append(RoundShip(250, 600, 0, -10, 600, 350, 10))
    # handler.enemy_ships.append(Sweeper(0, 600, 100, 0))
    pyglet.clock.schedule_interval(window.update, 1/FRAME_RATE)
    pyglet.app.run()




