class GameStats:
    # Track statistics for Alien Invasion

    def __init__(self, ai_settings, hs):
        # initialize stats
        self.ai_settings = ai_settings
        self.score = None
        self.ships_left = None
        self.level = None
        self.reset_stats()

        # start alien invasion in an inactive state
        self.game_active = False
        self.main_menu = True
        self.high_score_menu = False

        # High score should never be reset
        self.high_score = hs.high_scores[0]

    def reset_stats(self):
        # initialize stats that can change during the game
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
