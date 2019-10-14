import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from text import Text
from image import Image
from high_scores import HighScores
import game_functions as gf


def run_game():
    """ Initialize pygame, settings and screen objects. """
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    """ Make play, back and high score buttons. """
    play_button = Button(screen, "Play", 800, 400)
    high_score_button = Button(screen, "High Score", 800, 500)
    back_button = Button(screen, "Back", 500, 850)

    """ Make start screen. """
    title1 = Text(screen, "SPACE", screen.get_rect().centerx, 85, 500, 100,
                  (255, 255, 255), 250)
    title2 = Text(screen, "INVADERS", screen.get_rect().centerx, 200, 500,
                  100, (255, 255, 255), 158)
    high_score_title1 = Text(screen, "PLAYER", 420, 30, 180,
                             70, (255, 255, 255), 100)
    high_score_title2 = Text(screen, "SCORE", 830, 30, 250,
                             70, (255, 255, 255), 100)

    """ Create a list for alien scores. """
    li_as = [Text(screen, "= {} PTS".format(x*10), 480, 320 + (x * 80), 220, 50, (255, 255, 255), 70) for x in range(3)]

    """ Create ufo score. """
    ufo_score = Text(screen, "= ?? PTS", 480, 560, 220, 50, (255, 255, 255), 70)

    """ Create a list for high scores. """
    li_hs = [Text(screen, "{}".format(x+1), 420, 100 + (x*55), 50, 50, (255, 255, 255), 65) for x in range(9)]

    """ Create a list for alien images. """
    li_ai = [Image(screen, 'images/a{}_c.png'.format(x+1), 230, 295 + (x * 80)) for x in range(3)]

    """ Create ufo and ship images. """
    ufo_img = Image(screen, 'images/ufo_4.png', 230, 565)
    ship_img = Image(screen, 'images/ship.png', 540, 764)

    """ Create an instance to store game stats and create a scoreboard. """
    high_scores = HighScores()
    stats = GameStats(ai_settings, high_scores)
    sb = Scoreboard(ai_settings, screen, stats)

    """ Make a group of bullets, a group for bunkers, a group of aliens, and a group for ufos. """
    bullets_ship = Group()
    bullets_alien = Group()

    bunker = Group()

    aliens = Group()
    alien_type = ['images/a1_a.png', 'images/a1_b.png', 'images/a1_c.png', 'images/a1_d.png', 'images/a1_e.png']
    ufo = Group()
    ufo_imgs = ['images/ufo_1.png', 'images/ufo_2.png', 'images/ufo_3.png', 'images/ufo_4.png', 'images/ufo_5.png']
    points = 10

    """ Create a fleet of aliens. """
    gf.create_fleet(ai_settings, screen, stats, alien_type, points, aliens,
                    ufo_imgs, ufo)

    """ Create the bunker. """
    gf.create_bunker(screen, bunker)

    """ Create the ship. """
    ship = Ship(ai_settings, screen)

    """ Load ship and alien sounds. """
    ship_shoot = pygame.mixer.Sound('sounds/laser.wav')
    ship_shoot.set_volume(0.05)
    alien_shoot = pygame.mixer.Sound('sounds/alien_shoot.wav')
    alien_shoot.set_volume(0.05)
    alien_exp = pygame.mixer.Sound('sounds/alien_death.wav')
    alien_exp.set_volume(0.05)
    ship_exp = pygame.mixer.Sound('sounds/player_death.wav')
    ship_exp.set_volume(0.05)
    ufo_sound = pygame.mixer.Sound('sounds/ufo.wav')
    ufo_sound.set_volume(0.01)
    ufo_sound_playing = False

    """ Load background music. """
    pygame.mixer.music.load('sounds/relaxing.mp3')
    pygame.mixer.music.set_volume(0.08)
    pygame.mixer.music.play(-1, 0.0)

    """ Set up 'intensity' drums. """
    original = pygame.mixer.Sound('sounds/original.wav')
    five_percent_faster = pygame.mixer.Sound('sounds/five_percent_faster.wav')
    ten_percent_faster = pygame.mixer.Sound('sounds/ten_percent_faster.wav')
    drum_channel = pygame.mixer.Channel(3)
    drum_channel.set_volume(0.05)

    """ Start the main loop for the game. """
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        high_score_button, back_button, ship, aliens, alien_type, points,
                        bullets_ship, bullets_alien, bunker, ufo_imgs, ufo, ship_shoot)

        if stats.game_active:
            ship.update()
            if ship.timer.finished is True:
                gf.ship_hit(ai_settings, stats, screen, sb,
                            ship, aliens, alien_type, points, bullets_alien,
                            bullets_ship, high_scores, bunker, ufo_imgs, ufo, ship_exp)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              alien_type, points, bullets_ship, bullets_alien,
                              high_scores, bunker, ufo_imgs, ufo, alien_shoot, alien_exp, ship_exp)
            gf.update_aliens(ai_settings, stats, screen, sb,  ship, aliens,
                             alien_type, points, bullets_alien, bullets_ship, high_scores,
                             bunker, ufo_imgs, ufo, ship_exp)

            """" Change music to indicate less enemies. """
            if not drum_channel.get_busy():
                if len(aliens) < 30:
                    drum_channel.play(original, 1)
                elif len(aliens) < 20:
                    drum_channel.stop()
                    drum_channel.set_volume(0.07)
                    drum_channel.play(five_percent_faster, 1)
                elif len(aliens) < 11:
                    drum_channel.stop()
                    drum_channel.set_volume(0.1)
                    drum_channel.play(ten_percent_faster, 1)
                elif len(aliens) == 0:
                    drum_channel.fadeout(5)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets_ship, bullets_alien, play_button, high_score_button, back_button, title1,
                         title2, li_as, ufo_score, li_ai, ship_img, ufo_img, high_score_title1, high_score_title2,
                         li_hs, high_scores, bunker, ufo, ufo_sound, ufo_sound_playing)


run_game()
