


class GameState:
    """
    Base class for game states in Balatro, used for Monte Carlo Tree Search (MCTS).
    """
    def __init__(self, state_type, parent=None):
        self.state_type = state_type  # Type of state, e.g., "Play" or "Buy"
        self.parent = parent  # Parent state (used for backpropagation in MCTS)
        self.children = []  # List of child states
        self.visits = 0  # Number of times this state has been visited
        self.value = 0.0  # Cumulative value for MCTS backpropagation

    def is_terminal(self):
        """
        Returns True if this is a terminal state (e.g., game over).
        Should be overridden by child classes if necessary.
        """
        raise NotImplementedError

    def get_actions(self):
        """
        Returns a list of possible actions from this state.
        Should be implemented by child classes.
        """
        raise NotImplementedError

    def simulate(self):
        """
        Simulates this state to produce a score/reward.
        Should be implemented by child classes.
        """
        raise NotImplementedError

    def __repr__(self):
        return f"<GameState type={self.state_type} visits={self.visits} value={self.value}>"



class PlayState(GameState):
    """
    Represents the state of the game during the 'Play' phase in Balatro.
    """
    def __init__(self, hand, chips, multiplier, required_score, current_score, rounds_remaining, jokers, active_buffs):
        self.hand = hand  # List of cards in the current hand
        self.chips = chips  # Number of chips accumulated
        self.multiplier = multiplier  # Current multiplier applied to chips
        self.required_score = required_score  # Target score to pass the round
        self.current_score = current_score  # Current score achieved in this round
        self.rounds_remaining = rounds_remaining  # How many rounds are left before failure
        self.jokers = jokers  # List of active Joker cards
        self.active_buffs = active_buffs  # Any temporary buffs or effects active during the play phase

        # Optional attributes
        self.is_boss_round = False  # Whether the current round is a boss round
        self.played_hands = []  # A log of poker hands played (e.g., "Full House", "Flush")
        self.bonus_cards_used = 0  # Number of bonus cards (like Tarot or Planet cards) played
        self.score_multiplier_history = []  # History of multipliers applied

    def is_terminal(self):
        # Terminal if player cannot meet required score or no rounds remain
        return self.current_score >= self.required_score or self.rounds_remaining <= 0

    def get_actions(self):
        # Return possible poker hands to play as actions
        return ["Pair", "Flush", "Full House", "Straight"]  # Example actions

    def simulate(self):
        # Simulate scoring based on a random action (basic implementation)
        import random
        action = random.choice(self.get_actions())
        reward = self.multiplier * 10  # Example simulation logic
        return reward



class BuyState(GameState):
    """
    Represents the state of the game during the 'Buy' phase in Balatro.
    """
    def __init__(self, shop_items, money, jokers_owned, rerolls_remaining, shop_level):
        self.shop_items = shop_items  # List of items available in the shop
        self.money = money  # Amount of money available to spend
        self.jokers_owned = jokers_owned  # List of Joker cards owned
        self.rerolls_remaining = rerolls_remaining  # Number of shop rerolls left
        self.shop_level = shop_level  # Current level of the shop

        # Optional attributes
        self.bonus_discount = 0  # Discount percentage applied to shop items
        self.items_purchased = []  # Log of items purchased in this phase
        self.free_reroll_used = False  # Whether the player has used a free reroll

    def is_terminal(self):
        # Terminal if no money remains or all items are purchased
        return self.money <= 0 or not self.shop_items

    def get_actions(self):
        # Return a list of items that can be purchased as actions
        return [item["name"] for item in self.shop_items if item["cost"] <= self.money]

    def simulate(self):
        # Simulate a purchase by randomly selecting an affordable item
        import random
        affordable_items = [item for item in self.shop_items if item["cost"] <= self.money]
        if not affordable_items:
            return 0  # No reward if no purchase is possible
        chosen_item = random.choice(affordable_items)
        return chosen_item["cost"] / 10  # Example reward logic