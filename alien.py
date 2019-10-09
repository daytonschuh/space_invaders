import pygame
from pygame.sprite import Sprite
from timer import Timer


class Alien(Sprite):
    # a class to represent a single alien in the fleet

    def __init__(self, ai_settings, screen, alien_type, points):
        # initialize the alien and set its start position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the alien image and set its rect attribute
        self.image = None
        self.timer = Timer(alien_type, wait=150)
        self.alien_types(self.timer.imagerect())
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

        # explode or not
        self.explode = False

        # points value
        self.point_value = points

    def alien_types(self, alien_type):
        # chooses image for alien based on string passed
        self.image = pygame.image.load(alien_type)

    def blitme(self):
        # draw the alien at its current position
        self.screen.blit(self.image, self.rect)

    def update(self, ship):
        # move the alien right or left
        if self.explode is False and ship.explode is False:
            self.x += (self.ai_settings.curr_alien_speed_factor *
                       self.ai_settings.fleet_direction)
            self.rect.x = self.x
        if ship.explode is False:
            self.image = pygame.image.load(self.timer.imagerect())

    def check_edges(self):
        # return true if alien is at the edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
