import pygame


class Image:
    # a class to represents aliens on a start screen

    def __init__(self, screen, alien_type, rectx, recty):
        self.screen = screen

        # load the alien image and set its rect attribute
        self.image = None
        self.alien_types(alien_type)
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = rectx
        self.rect.y = recty

    def alien_types(self, alien_type):
        # chooses image for alien based on string passed
        self.image = pygame.image.load(alien_type)

    def blitme(self):
        # draw the alien at its current position
        self.screen.blit(self.image, self.rect)
