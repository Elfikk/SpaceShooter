#Preset waves for the game handler.

from GameConstants import FRAME_RATE, SCREEN_HEIGHT, SCREEN_WIDTH, SWEEPER_SPEED
from Enemies import RoundShip, Sweeper, ZigZagger

class Wave():

    def __init__(self, sequence = [], cooldowns = [], initial_wait = 0):

        self.duration = sum(cooldowns) + 5 * FRAME_RATE
        self.sequence = sequence
        self.cooldowns = cooldowns
        self.current_cooldown = initial_wait

    def series_add(self, other, mid_break = 5 * FRAME_RATE):
        #Combine two wave objects into a linear sequence of the two.
        if mid_break:
            new_wave = Wave(self.sequence + [] + other.sequence, self.cooldowns \
                        + [mid_break] + other.cooldowns)
        else:
            new_wave = Wave(self.sequence + other.sequence, self.cooldowns \
                        + other.cooldowns)
        return new_wave

    def __add__(self, other):
        return self.series_add(other)

    # def parallel_add(self, other, offset = 0):
    #     #Combines two waves into one with the enemy sequence combined together
    #     #into one.

    #     offset_seq = 

    def tick(self):

        self.current_cooldown -= 1
        if self.current_cooldown <= 0:
            try:
                self.current_cooldown = self.cooldowns[0]
                self.cooldowns = self.cooldowns[1:]
                next_enemies = self.sequence[0]
                self.sequence = self.sequence[1:]
                return next_enemies
            except IndexError:
                if len(self.cooldowns) == 0 and len(self.sequence) == 1:
                    self.current_cooldown = 5 * FRAME_RATE
                    next_enemies = self.sequence[0]
                    self.sequence = self.sequence[1:]
                    return next_enemies
                if len(self.cooldowns) == len(self.sequence):
                    raise Exception("Wave tick has overrun its break.")

        return []

def sweep_wave_horizontal(sweepers = 5, left_to_right = True):
    #Left to Right on the first ship by default, 

    density = SCREEN_HEIGHT // (sweepers + 1)

    if left_to_right:
        sequence = [Sweeper(0, y, SWEEPER_SPEED, 0) for y in range(0, \
            sweepers * density, density)]
    else:
        sequence = [Sweeper(SCREEN_WIDTH, y, -SWEEPER_SPEED, 0) for y \
            in range(0, sweepers * density, density)]
    cooldowns = [1] * (sweepers - 1)

    return Wave(sequence, cooldowns)

def sweep_wave_vertical(sweepers = 5, top_to_bottom = True):

    density = SCREEN_WIDTH // (sweepers + 1)

    if top_to_bottom:
        sequence = [Sweeper(x, 0, 0, -SWEEPER_SPEED) for x in range(0, \
            sweepers * density, density)]
    else:
        sequence = [Sweeper(x, SCREEN_HEIGHT, 0, SWEEPER_SPEED) for x in\
            range(0, sweepers * density, density)]
    cooldowns = [1] * (sweepers - 1)

    return Wave(sequence, cooldowns)

if __name__ == "__main__":

    # a = Wave(["1", "2", "3"], [1,2])
    # for i in range(100):
    #     next_ting = a.tick()
    #     print(next_ting, a.current_cooldown, a.cooldowns, a.sequence)

    seq = sweep_wave_horizontal(5, False)
    print(seq)