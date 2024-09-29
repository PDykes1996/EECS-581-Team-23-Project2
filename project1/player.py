class Player:
    def __init__(self, player_id, difficulty=None):
        self.player_id = player_id
        #self.ships = None
        self.ships = []
        self.sunk_ships = []
        self.hits = [[None] * 10 for _ in range(10)]
        self.attack_grid = [[None for _ in range(10)] for _ in range(10)]
        self.special_used = False

        if difficulty is None:
            self.difficulty = None
            self.isAI = False
        else:
            self.difficulty = difficulty
            self.isAI = True