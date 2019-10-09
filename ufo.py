import pygame
from pygame.sprite import Sprite
from timer import Timer


class Ufo(Sprite):
    # a class to represent the ufo in the fleet

    def __init__(self, ai_settings, screen, alien_type, points):
        # initialize the ufo and set its start position
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ufo image and set its rect attribute
        self.image = None
        self.timer = Timer(alien_type, wait=150)
        self.alien_types(self.timer.imagerect())
        self.rect = self.image.get_rect()

        # start each new ufo near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the ufo's exact position
        self.x = float(self.rect.x)

        # points value
        self.point_value = points

        # exploded or not
        self.explode = False

    def alien_types(self, alien_type):
        # chooses image for ufo based on string passed
        self.image = pygame.image.load(alien_type)

    def blitme(self):
        # draw the ufo at its current position
        self.screen.blit(self.image, self.rect)

    def update(self, ship):
        # move the ufo right
        if self.explode is False and ship.explode is False:
            self.x += self.ai_settings.curr_alien_speed_factor * 1.5
            self.rect.x = self.x
        if ship.explode is False:
            self.image = pygame.image.load(self.timer.imagerect())

    def check_edges(self):
        # return true if ufo passed the edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.left >= screen_rect.right:
            return True

    def increase_points(self, settings):
        self.point_value = int(self.point_value * settings.score_scale)
