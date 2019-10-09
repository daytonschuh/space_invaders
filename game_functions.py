import sys
import pygame.font
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from bunker import Bunker
from ufo import Ufo
import random


def check_keydown_events(event, ai_settings, screen, ship, bullets_ship, ship_shoot):
    # respond to keypresses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet_ship(ai_settings, screen, ship, bullets_ship, ship_shoot)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # respond to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, high_score_button, back_button,
                 ship, aliens, alien_type, points, bullets_ship, bullets_alien,
                 bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_shoot):
    # respond to keypresses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets_ship, ship_shoot)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              high_score_button, back_button, ship, aliens, alien_type,
                              points, bullets_ship, bullets_alien, mouse_x, mouse_y, bunker1,
                              bunker2, bunker3, ufo_imgs, ufo_group)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      high_score_button, back_button, ship, aliens, alien_type, points, bullets_ship,
                      bullets_alien, mouse_x, mouse_y, bunker1, bunker2, bunker3,
                      ufo_imgs, ufo_group):
    # start a new game when the player clicks Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    button_clicked2 = high_score_button.rect.collidepoint(mouse_x, mouse_y)
    button_clicked3 = back_button.rect.collidepoint(mouse_x, mouse_y)

    if (button_clicked or button_clicked2 or button_clicked3) and not stats.game_active:
        # reset the game settings
        ai_settings.initialize_dynamic_settings()

        # reset the game statistics
        stats.reset_stats()
        if button_clicked:
            stats.game_active = True
            stats.main_menu = False
            stats.high_score_menu = False
            # hide the mouse cursor
            pygame.mouse.set_visible(False)

        if button_clicked2:
            stats.high_score_menu = True
            stats.main_menu = False

        if button_clicked3:
            stats.high_score_menu = False
            stats.main_menu = True

        # reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the list of aliens, bullets, bunkers
        aliens.empty()
        ufo_group.empty()
        bullets_ship.empty()
        bullets_alien.empty()
        bunker1.empty()
        bunker2.empty()
        bunker3.empty()

        # create a new fleet, center the ship, rebuild bunkers
        create_fleet(ai_settings, screen, stats, alien_type, points, aliens,
                     ufo_imgs, ufo_group)
        ship.center_ship()
        ship.initialize()
        create_bunker(screen, 1, bunker1)
        create_bunker(screen, 2, bunker2)
        create_bunker(screen, 3, bunker3)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets_ship, bullets_alien,
                  play_button, high_score_button, back_button, title1, title2, alien_1_score,
                  alien_2_score, alien_3_score, ufo_score, alien_1_img,
                  alien_2_img, alien_3_img, ship_img, ufo_img, high_score_title1,
                  high_score_title2, hs1, hs2, hs3, hs4, hs5, hs6, hs7,
                  hs8, hs9, hs10, high_scores, bunker1, bunker2, bunker3, ufo_group,
                  ufo_sound, playing):

    # update images on screen and flip the new screen
    for ufo in ufo_group:
        if ufo.rect.right > 0 and ufo.rect.left < 1200 and \
                ship.explode is False and ufo.explode is False:
            if playing is False:
                ufo_sound.play(loops=-1)
                playing = True
        else:
            ufo_sound.stop()
            playing = False

    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # redraw all bullets behind ship and aliens
    for bullet in bullets_ship.sprites():
        bullet.draw_bullet()
    for bullet in bullets_alien.sprites():
        bullet.draw_bullet()

    bunker1.draw(screen)
    bunker2.draw(screen)
    bunker3.draw(screen)

    ship.blitme()
    aliens.draw(screen)
    ufo_group.draw(screen)

    # draw the score info
    sb.show_score()

    # draw the main menu and scoreboard if the game is inactive
    if not stats.game_active:
        if stats.main_menu:
            screen.fill(ai_settings.bg_color)
            pygame.draw.rect(screen, (255, 255, 255), (25, 25, 1150, 850), 5)
            title1.draw_text()
            title2.draw_text()
            alien_1_score.draw_text()
            alien_2_score.draw_text()
            alien_3_score.draw_text()
            alien_1_img.blitme()
            alien_2_img.blitme()
            alien_3_img.blitme()
            ship_img.blitme()
            ufo_img.blitme()
            ufo_score.draw_text()
            play_button.draw_button()
            high_score_button.draw_button()
        elif stats.high_score_menu:
            screen.fill(ai_settings.bg_color)
            pygame.draw.rect(screen, (255, 255, 255), (25, 25, 1150, 850), 5)
            high_score_title1.draw_text()
            high_score_title2.draw_text()
            hs1.draw_text()
            hs2.draw_text()
            hs3.draw_text()
            hs4.draw_text()
            hs5.draw_text()
            hs6.draw_text()
            hs7.draw_text()
            hs8.draw_text()
            hs9.draw_text()
            hs10.draw_text()
            high_score_screen(high_scores, 0, screen, 100)
            high_score_screen(high_scores, 1, screen, 155)
            high_score_screen(high_scores, 2, screen, 210)
            high_score_screen(high_scores, 3, screen, 265)
            high_score_screen(high_scores, 4, screen, 320)
            high_score_screen(high_scores, 5, screen, 375)
            high_score_screen(high_scores, 6, screen, 430)
            high_score_screen(high_scores, 7, screen, 485)
            high_score_screen(high_scores, 8, screen, 540)
            high_score_screen(high_scores, 9, screen, 595)
            back_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def high_score_screen(hs, num, screen, recty):
    # turn the high score into a rendered image
    font = pygame.font.SysFont(None, 48)
    score = int(hs.high_scores[num])
    score_str = "{:,}".format(score)
    score_image = font.render(score_str, True, (255, 255, 255), (0, 0, 0))

    # center the high score at the top of the screen
    score_rect = score_image.get_rect()
    score_rect.centerx = screen.get_rect().centerx + 235
    score_rect.top = recty
    screen.blit(score_image, score_rect)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                   alien_type, points, bullets_ship, bullets_alien, high_scores,
                   bunker1, bunker2, bunker3, ufo_imgs, ufo_group, alien_shoot,
                   alien_exp, ship_exp):
    # update position of bullets and get rid of old bullets
    # update bullet positions
    bullets_ship.update(ship)
    bullets_alien.update(ship)

    for alien in aliens:
        alien_bullet_interval(ai_settings, screen, alien, bullets_alien, stats,
                              alien_shoot, ship)

    # get rid of bullets that have disappeared
    for bullet in bullets_ship.copy():
        if bullet.rect.bottom <= 0:
            bullets_ship.remove(bullet)
    for bullet in bullets_alien.copy():
        if bullet.rect.top >= 800:
            bullets_alien.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  alien_type, points, aliens, bullets_ship,
                                  ufo_imgs, ufo_group, bunker1, bunker2, bunker3,
                                  alien_exp)
    check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship,
                                 alien_type, points, aliens, bullets_alien,
                                 bullets_ship, high_scores, bunker1, bunker2, bunker3,
                                 ufo_imgs, ufo_group, ship_exp)
    check_bullet_bullet_collisions(bullets_alien, bullets_ship)
    check_bullet_bunker_collisions(bullets_alien, bullets_ship, bunker1, bunker2, bunker3)
    check_alien_bunker_collisions(aliens, bunker1, bunker2, bunker3)
    check_bullet_ufo_collisions(stats, sb, ai_settings, bullets_ship, ufo_group,
                                alien_exp)


def check_bullet_bullet_collisions(bullets_alien, bullets_ship):
    # respond to bullet bullet collisions
    # remove any bullets that have collided
    pygame.sprite.groupcollide(bullets_alien, bullets_ship, True, True)


def check_alien_bunker_collisions(aliens, bunker1, bunker2, bunker3):
    # respond to alien bunker collisions
    # remove any bunker that have collided
    pygame.sprite.groupcollide(aliens, bunker1, False, True)
    pygame.sprite.groupcollide(aliens, bunker2, False, True)
    pygame.sprite.groupcollide(aliens, bunker3, False, True)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  alien_type, points, aliens, bullets,
                                  ufo_imgs, ufo_group, bunker1, bunker2, bunker3,
                                  alien_exp):
    # respond to bullet alien collisions
    # remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for x in aliens:
                if x.explode is False:
                    pygame.mixer.Channel(2).play(alien_exp)
                    stats.score = int(round(stats.score + x.point_value))
                    sb.prep_score()
                    ai_settings.increase_speed_temp()
                    x.explode = True
                    x.timer.frames = ['images/ex_1.png', 'images/ex_2.png', 'images/ex_3.png', 'images/ex_4.png',
                                      'images/ex_5.png', 'images/ex_6.png', 'images/ex_7.png']
                    x.timer.reset()
                    x.timer.frameindex = 0
                    x.timer.lastframe = 4
                    x.timer.wait = 75
                    x.timer.looponce = True
            check_high_score(stats, sb)

    if len(aliens) == 0:
        # if the enemy fleet is destroyed, start a new level
        bullets.empty()
        ufo_group.empty()
        bunker1.empty()
        bunker2.empty()
        bunker3.empty()

        ai_settings.ufo_counter = 0
        ai_settings.ufo_limit = random.randint(2000, 4000)
        ai_settings.ufo_exp_count = 0
        ai_settings.ufo_exp_limit = 100

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, stats, alien_type, points, aliens,
                     ufo_imgs, ufo_group)
        create_bunker(screen, 1, bunker1)
        create_bunker(screen, 2, bunker2)
        create_bunker(screen, 3, bunker3)
        ai_settings.increase_speed()
        ai_settings.randomize_bullet_rate(stats)


def check_bullet_ship_collisions(ai_settings, screen, stats, sb, ship,
                                 alien_type, points, aliens, bullets_alien,
                                 bullets_ship, high_scores, bunker1, bunker2, bunker3,
                                 ufo_imgs, ufo_group, ship_exp):
    # respond to bullet ship collisions
    # remove any bullets that have collided
    collisions = pygame.sprite.spritecollide(ship, bullets_alien, True)

    if collisions:
        ship_hit(ai_settings, stats, screen, sb, ship, aliens,
                 alien_type, points, bullets_alien, bullets_ship, high_scores,
                 bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp)


def check_bullet_ufo_collisions(stats, sb, ai_settings, bullets_ship, ufo_group,
                                alien_exp):
    # respond to bullet ufo collisions
    # remove any bullets and ufo that have collided
    for ufo in ufo_group:
        if ufo.explode is False:
            collision = pygame.sprite.groupcollide(bullets_ship, ufo_group, True, False)
            if collision:
                for ufo_group in collision.values():
                    for x in ufo_group:
                        pygame.mixer.Channel(2).play(alien_exp)
                        stats.score = int(round(stats.score + x.point_value))
                        sb.prep_score()
                        ufo.explode = True
                        rounded_points = int(round(ufo.point_value, -1))
                        points_str = str(rounded_points)
                        font = pygame.font.SysFont(None, 48)
                        points_img = font.render(points_str, True, (255, 255, 255),
                                                 ai_settings.bg_color)
                        ufo.image = points_img


def check_bullet_bunker_collisions(bullets_alien, bullets_ship, bunker1, bunker2, bunker3):
    # respond to bullet bunker collisions
    # remove any bullets and damage bunker that have collided
    collisions1 = pygame.sprite.groupcollide(bunker1, bullets_alien, False, True)
    collisions2 = pygame.sprite.groupcollide(bunker2, bullets_alien, False, True)
    collisions3 = pygame.sprite.groupcollide(bunker3, bullets_alien, False, True)

    collisions4 = pygame.sprite.groupcollide(bunker1, bullets_ship, False, True)
    collisions5 = pygame.sprite.groupcollide(bunker2, bullets_ship, False, True)
    collisions6 = pygame.sprite.groupcollide(bunker3, bullets_ship, False, True)

    for pieces in collisions1:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker1.remove(pieces)
    for pieces in collisions2:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker2.remove(pieces)
    for pieces in collisions3:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker3.remove(pieces)

    for pieces in collisions4:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker1.remove(pieces)
    for pieces in collisions5:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker2.remove(pieces)
    for pieces in collisions6:
        if pieces.hits == 0:
            pieces.update()
            pieces.hits = 1
        elif pieces.hits == 1:
            bunker3.remove(pieces)


def fire_bullet_ship(ai_settings, screen, ship, bullets, ship_shoot):
    # fire a bullet if limit is not reached yet
    # create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        pygame.mixer.Channel(0).play(ship_shoot)
        new_bullet = Bullet(ai_settings, screen, ship, "ship")
        bullets.add(new_bullet)


def fire_bullet_alien(ai_settings, screen, alien, bullets, alien_shoot):
    # fire bullet from alien
    # create a new bullet and add it to the bullet group
    pygame.mixer.Channel(1).play(alien_shoot)
    new_bullet = Bullet(ai_settings, screen, alien, "alien")
    bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    # determine the number of aliens that fit in a row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, alien_type, points, aliens, alien_number,
                 row_number):
    # create an alien and place it in the row
    alien = Alien(ai_settings, screen, alien_type, points)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + alien.rect.height * row_number - 100
    aliens.add(alien)


def create_ufo(ai_settings, screen, ufo_imgs, points, ufo_group):
    ufo = Ufo(ai_settings, screen, ufo_imgs, points)
    ufo_width = ufo.rect.width
    ufo.x = 0 - ufo_width
    ufo.rect.x = ufo.x
    ufo.rect.y = 40
    ufo_group.add(ufo)


def create_fleet(ai_settings, screen, stats, alien_type, points, aliens,
                 ufo_imgs, ufo_group):
    # create a full fleet of aliens
    # create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen, alien_type, points)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = 6

    # create ufo
    if stats.level > 1:
        points = random.randint(50, 100) * ai_settings.score_scale ** (stats.level - 1)
    else:
        points = random.randint(50, 100)
    create_ufo(ai_settings, screen, ufo_imgs, points, ufo_group)

    # create the fleet of aliens
    for row_number in range(number_rows):
        if row_number is 0 or row_number is 1:
            alien_type = ['images/a1_a.png', 'images/a1_b.png', 'images/a1_c.png', 'images/a1_d.png', 'images/a1_e.png']
            if stats.level > 1:
                points = 10 * ai_settings.score_scale**(stats.level - 1)
            else:
                points = 10
        elif row_number is 2 or row_number is 3:
            alien_type = ['images/a2_a.png', 'images/a2_b.png', 'images/a2_c.png', 'images/a2_d.png', 'images/a2_e.png']
            if stats.level > 1:
                points = 20 * ai_settings.score_scale ** (stats.level - 1)
            else:
                points = 20
        elif row_number is 4 or row_number is 5:
            alien_type = ['images/a3_a.png', 'images/a3_b.png', 'images/a3_c.png', 'images/a3_d.png', 'images/a3_e.png']
            if stats.level > 1:
                points = 40 * ai_settings.score_scale ** (stats.level - 1)
            else:
                points = 40
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, alien_type, points, aliens, alien_number,
                         row_number)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens,
             alien_type, points, bullets_alien, bullets_ship, high_scores,
             bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp):
    # respond to ship being hit by alien
    if ship.explode is False:
        pygame.mixer.Channel(3).play(ship_exp)
        ship.explode = True
        ship.timer.frames = ship.explode_frames
        ship.timer.reset()
        ship.timer.frameindex = 0
        ship.timer.lastframe = 8
        ship.timer.looponce = True
    if ship.timer.finished is True:
        if stats.ships_left > 0:
            # decrement ships_left
            stats.ships_left -= 1

            # update scoreboard
            sb.prep_ships()

            # empty the list of aliens and bullets
            aliens.empty()
            ufo_group.empty()
            bullets_alien.empty()
            bullets_ship.empty()
            bunker1.empty()
            bunker2.empty()
            bunker3.empty()

            ai_settings.ufo_counter = 0
            ai_settings.ufo_limit = random.randint(2000, 4000)

            # create a new fleet and center the ship
            create_fleet(ai_settings, screen, stats, alien_type, points, aliens,
                         ufo_imgs, ufo_group)
            ship.center_ship()
            ship.initialize()
            create_bunker(screen, 1, bunker1)
            create_bunker(screen, 2, bunker2)
            create_bunker(screen, 3, bunker3)

            # reset curr speed
            ai_settings.curr_alien_speed_factor = ai_settings.base_alien_speed_factor

            # pause
            sleep(0.5)
        else:
            stats.game_active = False
            stats.main_menu = True
            high_scores.update_scores(stats)
            high_scores.save_scores()
            pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens,
                  alien_type, points, bullets_aliens, bullets_ship, high_scores,
                  bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp):
    # check if the fleet is at an edge and
    # update the positions of all in the fleet
    check_fleet_edges(ai_settings, aliens, ufo_group)
    aliens.update(ship)
    for alien in aliens:
        if alien.timer.finished is True:
            aliens.remove(alien)
    if ship.explode is False:
        ai_settings.ufo_counter += 1
    for ufo in ufo_group:
        if (ai_settings.ufo_counter > ai_settings.ufo_limit) and ufo.explode is False:
            ufo_group.update(ship)
        elif (ai_settings.ufo_counter > ai_settings.ufo_limit) and ufo.explode is True:
            ufo.blitme()
            ai_settings.ufo_exp_count += 1

        if ai_settings.ufo_exp_count > ai_settings.ufo_exp_limit:
            ufo_group.remove(ufo)

    # look for alien ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens,
                 alien_type, points, bullets_aliens, bullets_ship,
                 high_scores, bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp)

    # look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
                        alien_type, points, bullets_aliens, bullets_ship, high_scores,
                        bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp)


def check_fleet_edges(ai_settings, aliens, ufo_group):
    # respond appropriately if any aliens have reached the edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
    for ufo in ufo_group.sprites():
        if ufo.check_edges():
            ai_settings.ufo_counter = 0
            ai_settings.ufo_limit = random.randint(2000, 4000)
            ufo.x = 0 - ufo.rect.width
            ufo.rect.x = ufo.x


def change_fleet_direction(ai_settings, aliens):
    # drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
                        alien_type, points, bullets_alien, bullets_ship, high_scores,
                        bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp):
    # check if any aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens,
                     alien_type, points, bullets_alien, bullets_ship, high_scores,
                     bunker1, bunker2, bunker3, ufo_imgs, ufo_group, ship_exp)
            break


def check_high_score(stats, sb):
    # check to see if theres a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def alien_bullet_interval(ai_settings, screen, alien, bullets, stats, alien_shoot, ship):
    if ship.explode is False:
        ai_settings.alien_bullet_counter += 1
    if ai_settings.alien_bullet_counter > ai_settings.alien_bullet_rate:
        fire_bullet_alien(ai_settings, screen, alien, bullets, alien_shoot)
        ai_settings.alien_bullet_counter = 0
        ai_settings.randomize_bullet_rate(stats)


def create_bunker(screen, position, bunker):
    bunk_foot_left = None
    bunk_left = None
    bunk_up_left = None
    bunk_up = None
    bunk_down = None
    bunk_up_right = None
    bunk_right = None
    bunk_foot_right = None
    if position == 1:
        bunk_foot_left = Bunker(screen, ['images/bottom_left.png', 'images/bottom_left_break.png'],
                                720, 140)
        bunk_left = Bunker(screen, ['images/left.png', 'images/left_break.png'],
                           680, 140)
        bunk_up_left = Bunker(screen, ['images/top_left.png', 'images/top_left_break.png'],
                              640, 140)
        bunk_up = Bunker(screen, ['images/top.png', 'images/top_break.png'],
                         640, 180)
        bunk_down = Bunker(screen, ['images/bottom.png', 'images/bottom_break.png'],
                           680, 180)
        bunk_up_right = Bunker(screen, ['images/top_right.png', 'images/top_right_break.png'],
                               640, 220)
        bunk_right = Bunker(screen, ['images/right.png', 'images/right_break.png'],
                            680, 220)
        bunk_foot_right = Bunker(screen, ['images/bottom_right.png', 'images/bottom_right_break.png'],
                                 720, 220)
    elif position == 2:
        bunk_foot_left = Bunker(screen, ['images/bottom_left.png', 'images/bottom_left_break.png'],
                                720, 540)
        bunk_left = Bunker(screen, ['images/left.png', 'images/left_break.png'],
                           680, 540)
        bunk_up_left = Bunker(screen, ['images/top_left.png', 'images/top_left_break.png'],
                              640, 540)
        bunk_up = Bunker(screen, ['images/top.png', 'images/top_break.png'],
                         640, 580)
        bunk_down = Bunker(screen, ['images/bottom.png', 'images/bottom_break.png'],
                           680, 580)
        bunk_up_right = Bunker(screen, ['images/top_right.png', 'images/top_right_break.png'],
                               640, 620)
        bunk_right = Bunker(screen, ['images/right.png', 'images/right_break.png'],
                            680, 620)
        bunk_foot_right = Bunker(screen, ['images/bottom_right.png', 'images/bottom_right_break.png'],
                                 720, 620)
    elif position == 3:
        bunk_foot_left = Bunker(screen, ['images/bottom_left.png', 'images/bottom_left_break.png'],
                                720, 940)
        bunk_left = Bunker(screen, ['images/left.png', 'images/left_break.png'],
                           680, 940)
        bunk_up_left = Bunker(screen, ['images/top_left.png', 'images/top_left_break.png'],
                              640, 940)
        bunk_up = Bunker(screen, ['images/top.png', 'images/top_break.png'],
                         640, 980)
        bunk_down = Bunker(screen, ['images/bottom.png', 'images/bottom_break.png'],
                           680, 980)
        bunk_up_right = Bunker(screen, ['images/top_right.png', 'images/top_right_break.png'],
                               640, 1020)
        bunk_right = Bunker(screen, ['images/right.png', 'images/right_break.png'],
                            680, 1020)
        bunk_foot_right = Bunker(screen, ['images/bottom_right.png', 'images/bottom_right_break.png'],
                                 720, 1020)
    bunker.add(bunk_foot_left)
    bunker.add(bunk_left)
    bunker.add(bunk_up_left)
    bunker.add(bunk_up)
    bunker.add(bunk_down)
    bunker.add(bunk_up_right)
    bunker.add(bunk_right)
    bunker.add(bunk_foot_right)
