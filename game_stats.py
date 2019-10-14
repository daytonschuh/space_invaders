class GameStats:
    """ Track statistics for Space Invaders. """

    def __init__(self, ai_settings, hs):
        """ Initialize stats. """
        self.ai_settings = ai_settings
        self.score = None
        self.ships_left = None
        self.level = None
        self.reset_stats()

        """ Start Space Invaders at main menu. """
        self.game_active = False
        self.main_menu = True
        self.high_score_menu = False

        """ High score should never be reset. """
        self.high_score = hs.high_scores[0]

    def reset_stats(self):
        """ Reset stats that change during the game. """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
