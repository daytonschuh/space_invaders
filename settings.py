import random


class Settings:
    # A class to store all settings for Alien Invasion

    def __init__(self):
        # initialize the game's  static settings

        # screen settings
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (0, 0, 0)

        # ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (130, 130, 130)
        self.bullets_allowed = 3

        # alien settings
        self.base_alien_speed_factor = None
        self.curr_alien_speed_factor = None
        self.fleet_drop_speed = 10

        # how quickly the game speeds up
        self.speedup_scale = 1.1
        self.temp_speedup_scale = 1.005

        # how quickly the alien point values increase
        self.score_scale = 1.5

        self.fleet_direction = None
        self.alien_points = None
        self.initialize_dynamic_settings()

        # interval bullets will shoot
        self.alien_bullet_counter = None
        self.alien_bullet_rate = None
        self.alien_bullet_rate_increase = .95

        # interval ufo appears
        self.ufo_counter = None
        self.ufo_limit = None
        self.ufo_exp_count = None
        self.ufo_exp_limit = None

    def initialize_dynamic_settings(self):
        # initialize settings that change throughout the game
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.base_alien_speed_factor = .65
        self.curr_alien_speed_factor = self.base_alien_speed_factor
        self.alien_bullet_rate = random.randint(1000, 30001)
        self.alien_bullet_counter = 0
        self.ufo_counter = 0
        self.ufo_exp_count = 0
        self.ufo_exp_limit = 100
        self.ufo_limit = random.randint(2000, 4000)

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        # increase speed settings and alien point values
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.base_alien_speed_factor *= self.speedup_scale
        self.curr_alien_speed_factor = self.base_alien_speed_factor

    def increase_speed_temp(self):
        # temporarily increase the speed of aliens as they are destroyed
        self.curr_alien_speed_factor *= self.temp_speedup_scale

    def randomize_bullet_rate(self, stats):
        self.alien_bullet_rate = random.randint(5000, 10000) \
                                 * self.alien_bullet_rate_increase**stats.level
