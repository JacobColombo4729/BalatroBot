import random

class Effect:
    """
    Represents an effect that can be applied to the game or player.
    """
    def __init__(self, effect_type, value=None):
        """
        Initialize an effect.
        
        :param effect_type: Type of effect (e.g., 'increase_chips', 'swap_cards').
        :param value: The value associated with the effect (e.g., the amount of chips to increase).
        """
        self.effect_type = effect_type
        self.value = value

    # I might need to apply effects in a MCTS simulation phase
    def apply(self, player):
        """
        Apply the effect to a player.
        
        :param player: The player to whom the effect is applied.
        """
        if self.effect_type == 'increase_chips' and self.value is not None:
            player.chips += self.value
            print(f"{self.value} chips added!")
        elif self.effect_type == 'double_bet':
            player.double_bet = True
            print("Bet will be doubled!")
        elif self.effect_type == 'swap_cards':
            # Example of a swap effect (just a placeholder)
            print("Cards swapped!")
        else:
            print(f"Unknown effect: {self.effect_type}")



class Card:
    """
    Base class for a card in the Balatro deck.
    """
    def __init__(self, name, suit, chip_value, effects=None):
        self.name = name
        self.suit = suit
        self.chip_value = chip_value
        self.effects = effects if effects else []

    def apply_effects(self, player):
        """
        Apply the card's effects to a player.
        
        :param player: The player to whom the effect is applied.
        """
        for effect in self.effects:
            effect.apply(player)

    def __repr__(self):
        return f"{self.name} of {self.suit} ({self.chip_value} chips)"


class BalatroDeck:
    """
    Represents a type of deck in Balatro, altering game rules and deck composition.
    """
    def __init__(self, name, description, num_cards, joker_slots, consumable_slots, special_rules=None):
        """
        Initialize a DeckType instance.

        :param name: Name of the deck type.
        :param description: Brief description of the deck's traits.
        :param num_cards: Total number of cards in the deck.
        :param joker_slots: Number of available joker slots.
        :param consumable_slots: Number of slots for consumables (tarot, planet, spectral cards).
        :param special_rules: A dictionary of special modifiers or effects.
        """
        self.name = name
        self.description = description
        self.num_cards = num_cards
        self.joker_slots = joker_slots
        self.consumable_slots = consumable_slots
        self.special_rules = special_rules or {}  # Default to an empty dictionary
    
    def apply_special_rules(self, game_state):
        """
        Apply the deck's special rules to the game state.
        
        :param game_state: The current game state to modify.
        """
        for rule, value in self.special_rules.items():
            if rule == "bonus_chips":
                game_state.chips += value
                print(f"{self.name}: +{value} bonus chips applied!")
            elif rule == "extra_multiplier":
                game_state.base_multiplier += value
                print(f"{self.name}: Base multiplier increased by {value}x!")
            elif rule == "reroll_bonus":
                game_state.rerolls_remaining += value
                print(f"{self.name}: +{value} additional rerolls!")
            else:
                print(f"{self.name}: Unknown rule '{rule}' - No action taken.")
    
    def __repr__(self):
        return (f"<DeckType: {self.name} | Cards: {self.num_cards} | Joker Slots: {self.joker_slots} | "
                f"Consumable Slots: {self.consumable_slots} | Special Rules: {self.special_rules}>")



class Hand:
    """
    Represents a poker hand in Balatro.
    """
    HAND_BASE_MULTIPLIERS = {
        "High Card": 1.0,
        "Pair": 1.5,
        "Two Pair": 2.0,
        "Three of a Kind": 2.5,
        "Straight": 3.0,
        "Flush": 3.5,
        "Full House": 4.0,
        "Four of a Kind": 5.0,
        "Straight Flush": 7.0
    }
    
    HAND_BASE_CHIPS = {
        "High Card": 5,
        "Pair": 10,
        "Two Pair": 15,
        "Three of a Kind": 20,
        "Straight": 30,
        "Flush": 40,
        "Full House": 50,
        "Four of a Kind": 75,
        "Straight Flush": 100,
        "Royal Flush": 150
    }

    def __init__(self, name, cards):
        """
        Initialize a poker hand.

        :param name: Name of the hand (e.g., "Pair", "Full House").
        :param cards: List of cards forming the hand.
        """
        if name not in self.HAND_BASE_MULTIPLIERS:
            raise ValueError(f"Invalid hand name: {name}")
        
        self.name = name  # Name of the poker hand
        self.cards = cards  # List of cards in the hand
        self.level = 1  # All hands start at level 1
        self.base_chips = self.HAND_BASE_CHIPS[name]  # Base chip reward
        self.base_multiplier = self.HAND_BASE_MULTIPLIERS[name]  # Base multiplier

    def calculate_chips(self):
        """
        Calculate the chips for this hand based on its level.
        Chips increase linearly with the level.
        """
        return self.base_chips * self.level

    def calculate_multiplier(self):
        """
        Calculate the multiplier for this hand based on its level.
        Multiplier increases linearly with the level.
        """
        return self.base_multiplier * self.level

    def level_up(self):
        """
        Increase the level of the hand.
        """
        self.level += 1
        print(f"{self.name} leveled up to Level {self.level}!")

    def __repr__(self):
        return (f"<Hand: {self.name} | Level: {self.level} | Chips: {self.calculate_chips()} | "
                f"Multiplier: {self.calculate_multiplier()} | Cards: {self.cards}>")
    


class JokerCard:
    """
    Represents a Joker card in Balatro with unique attributes and abilities.
    """
    def __init__(self, name, effect_type, effect_description, rarity, value, unlock_condition):
        self.name = name  # Name of the Joker card (e.g., "The Fool", "The Collector")
        self.effect_type = effect_type  # Type of effect: e.g., "multiplier", "score boost", "resource gain"
        self.effect_description = effect_description  # Detailed description of its effect
        self.rarity = rarity  # Rarity: "Common", "Rare", "Legendary", "Celestial", etc.
        self.value = value  # Point value or cost associated with the Joker card
        self.unlock_condition = unlock_condition  # How the card is unlocked in gameplay

        # Advanced Attributes
        self.is_active = True  # Whether the Joker is active or disabled
        self.synergy_tags = []  # Tags like "Score", "Money", "Hand Size" for synergies
        self.limited_uses = None  # Number of times the card can be used (if limited)
        self.permanent = True  # If False, it can expire after certain uses



class Voucher:
    """
    Represents a Voucher in Balatro, providing persistent or passive effects.
    """
    def __init__(self, name, cost, description, rarity, effect_type, effect_value):
        """
        Initialize a voucher.

        :param name: Name of the voucher.
        :param cost: Cost to purchase the voucher.
        :param description: Description of the voucher's effect.
        :param rarity: Rarity level (e.g., "Common", "Rare", "Legendary").
        :param effect_type: Type of effect (e.g., "Discount", "Reroll Bonus", "Shop Slots").
        :param effect_value: Value of the effect (e.g., -10 for a 10% discount).
        """
        self.name = name
        self.cost = cost
        self.description = description
        self.rarity = rarity
        self.effect_type = effect_type
        self.effect_value = effect_value
    
    def apply_effect(self, game_state):
        """
        Apply the voucher's effect to the game state.
        """
        if self.effect_type == "Discount":
            game_state.shop_discount += self.effect_value
            print(f"{self.name} applied: Shop items cost {self.effect_value}% less.")
        elif self.effect_type == "Reroll Bonus":
            game_state.rerolls_remaining += self.effect_value
            print(f"{self.name} applied: +{self.effect_value} rerolls.")
        elif self.effect_type == "Shop Slots":
            game_state.shop_slots += self.effect_value
            print(f"{self.name} applied: +{self.effect_value} shop slots.")
        elif self.effect_type == "Bonus Chips":
            game_state.chips += self.effect_value
            print(f"{self.name} applied: +{self.effect_value} chips.")
        else:
            print(f"Unknown effect type: {self.effect_type}")
    
    def __repr__(self):
        return f"<Voucher: {self.name} ({self.rarity}) - {self.description}>"



class Consumable:
    """
    Base class for consumable cards in Balatro.
    """
    def __init__(self, name, cost, description, rarity):
        self.name = name  # Name of the consumable
        self.cost = cost  # Cost to purchase or play the consumable
        self.description = description  # Effect description
        self.rarity = rarity  # Rarity of the consumable: Common, Rare, Legendary, etc.
    
    def apply_effect(self, game_state):
        """
        Apply the card's effect to the game state.
        To be implemented by child classes.
        """
        raise NotImplementedError("Each consumable card must implement its own effect.")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.rarity})>"
        

# ----------------- Tarot Card Class -----------------
class TarotCard(Consumable):
    """
    Represents a Tarot Card in Balatro, providing buffs or score-related effects.
    """
    def __init__(self, name, cost, description, rarity, buff_type, buff_value):
        super().__init__(name, cost, description, rarity)
        self.buff_type = buff_type  # Type of buff: e.g., "Multiplier", "Chips", "Hand Size"
        self.buff_value = buff_value  # The value of the buff
    
    def apply_effect(self, game_state):
        """
        Apply the buff to the game state based on the buff type.
        """
        if self.buff_type == "Multiplier":
            game_state.multiplier += self.buff_value
        elif self.buff_type == "Chips":
            game_state.chips += self.buff_value
        elif self.buff_type == "Hand Size":
            game_state.hand_size += self.buff_value
        print(f"{self.name} applied: {self.buff_type} increased by {self.buff_value}.")

# ----------------- Planet Card Class -----------------
class PlanetCard(Consumable):
    """
    Represents a Planet Card in Balatro, often affecting hand scoring or multipliers.
    """
    def __init__(self, name, cost, description, rarity, special_effect):
        super().__init__(name, cost, description, rarity)
        self.special_effect = special_effect  # A string describing the unique effect
    
    def apply_effect(self, game_state):
        """
        Apply a unique planetary effect to the game state.
        """
        if self.special_effect == "Double Multiplier":
            game_state.multiplier *= 2
        elif self.special_effect == "Double Chips":
            game_state.chips *= 2
        print(f"{self.name} applied: {self.special_effect}.")

# ----------------- Spectral Card Class -----------------
class SpectralCard(Consumable):
    """
    Represents a Spectral Card in Balatro, often providing unique or mysterious effects.
    """
    def __init__(self, name, cost, description, rarity, duration, effect_function):
        super().__init__(name, cost, description, rarity)
        self.duration = duration  # Number of turns the effect lasts
        self.effect_function = effect_function  # Custom function for the effect
    
    def apply_effect(self, game_state):
        """
        Apply a spectral effect via a custom function.
        """
        self.effect_function(game_state)
        print(f"{self.name} applied: Effect active for {self.duration} turns.")



class BossBlinds:
    """
    Represents Boss Blinds in Balatro, which are special, higher blinds that escalate in difficulty.
    """
    def __init__(self, small_blind, big_blind, escalation_rate, max_blind_cap, difficulty_level=1, special_rules=None):
        """
        Initialize the BossBlinds system.
        
        :param small_blind: The starting small blind value.
        :param big_blind: The starting big blind value.
        :param escalation_rate: The rate at which the blinds increase.
        :param max_blind_cap: The maximum cap for small and big blinds.
        :param difficulty_level: The difficulty level that affects blind escalation speed.
        :param special_rules: Any special rules that apply during Boss Blinds mode.
        """
        self.small_blind = small_blind  # Starting small blind
        self.big_blind = big_blind  # Starting big blind
        self.escalation_rate = escalation_rate  # Rate at which the blinds increase
        self.max_blind_cap = max_blind_cap  # Maximum limit for blinds
        self.difficulty_level = difficulty_level  # Boss difficulty level
        self.special_rules = special_rules or {}  # Special rules specific to Boss Blinds
        self.round_counter = 0  # Track rounds to increase blinds
        self.boss_mode_active = False  # Flag to track if Boss Blinds mode is active

    def activate_boss_mode(self):
        """
        Activate Boss Blinds mode, changing the flow of the game.
        """
        self.boss_mode_active = True
        print("Boss Blinds Mode activated!")

    def deactivate_boss_mode(self):
        """
        Deactivate Boss Blinds mode, reverting to normal blinds.
        """
        self.boss_mode_active = False
        print("Boss Blinds Mode deactivated!")

    def increase_boss_blinds(self):
        """
        Increase the blinds according to the difficulty level and escalation rate.
        The blinds should not exceed the maximum cap.
        """
        if self.boss_mode_active:
            self.round_counter += 1
            if self.round_counter >= self.difficulty_level * self.escalation_rate:
                self.small_blind = min(self.small_blind + 5, self.max_blind_cap)
                self.big_blind = min(self.big_blind + 5, self.max_blind_cap)
                self.round_counter = 0
                print(f"Boss Blinds increased! New Small Blind: {self.small_blind}, New Big Blind: {self.big_blind}")
    
    def apply_boss_rules(self, game_state):
        """
        Apply any special rules or modifiers for Boss Blinds.
        
        :param game_state: The current game state.
        """
        for rule, value in self.special_rules.items():
            if rule == "bonus_chips":
                game_state.chips += value
                print(f"Boss Mode: +{value} bonus chips applied!")
            elif rule == "double_bet":
                game_state.double_bet = True
                print("Boss Mode: All bets are doubled!")
            else:
                print(f"Unknown Boss rule: {rule}")

    def get_current_boss_blinds(self):
        """
        Returns the current small and big blinds for Boss Blinds mode.
        """
        return self.small_blind, self.big_blind

    def __repr__(self):
        return (f"<BossBlinds: Small Blind = {self.small_blind}, Big Blind = {self.big_blind}, "
                f"Rounds Until Next Increment = {self.escalation_rate - self.round_counter}, "
                f"Difficulty Level = {self.difficulty_level}, Max Blind Cap = {self.max_blind_cap}>")

