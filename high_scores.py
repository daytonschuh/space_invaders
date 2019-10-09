class HighScores:

    def __init__(self):
        self.high_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.read_scores()
        self.save_scores()

    def save_scores(self):
        self.sort()
        file = open("high_scores.txt", "w")
        for x in self.high_scores:
            file.write(str(x) + "\n")
        file.close()

    def update_scores(self, stats):
        for x in self.high_scores:
            if stats.score > x:
                self.high_scores[9] = stats.score
                break

    def sort(self):
        for x in range(10):
            for y in range(9):
                if self.high_scores[y] < self.high_scores[y + 1]:
                    self.high_scores[y], self.high_scores[y + 1] = \
                        self.high_scores[y + 1], self.high_scores[y]

    def read_scores(self):
        file = open("high_scores.txt", "r")
        for x in range(10):
            self.high_scores[x] = int(file.readline())
        file.close()

    def read_players(self):
        """file = open("player_names.txt", "r")
        for x in range(10):
            self.player_names[x] = file.readline()
        file.close()"""
        pass
