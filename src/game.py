import random
from banker import Banker
from contestant import Contestant

class DealOrNoDealGame:
    def __init__(self, player_type="human", pause_between_rounds=False):
        # Define the amounts for the boxes
        amounts = [
            0.01, 1, 5, 10, 50, 100, 250, 500, 750, 1000,
            3000, 5000, 7500, 10000, 15000, 20000, 35000,
            50000, 75000, 100000
        ]
        self.boxes = self._randomize_boxes(amounts)
        self.player_type = player_type
        self.pause_between_rounds = pause_between_rounds
        self.player_box_amount = None
        self.player_box_key = None
        self.banker = Banker()
        self.contestant = Contestant(player_type)

    def _randomize_boxes(self, amounts):
        # Generate random box keys and shuffle them
        box_keys = list(range(1, len(amounts) + 1))
        random.shuffle(box_keys)

        # Shuffle the amounts and assign to the randomized keys
        random.shuffle(amounts)
        return dict(zip(box_keys, amounts))

    def setup(self):
        # Player selects a box to keep
        self.player_box_key = random.choice(list(self.boxes.keys()))
        self.player_box_amount = self.boxes[self.player_box_key]
        del self.boxes[self.player_box_key]
        print(f"You have chosen box {self.player_box_key} to keep until the end.")

    def play(self):
        self.setup()
        round_structure = [5, 3, 3, 3, 2, 1]

        for round_number, num_to_open in enumerate(round_structure, 1):
            print(f"\nRound {round_number}: Open {num_to_open} boxes.")
            opened_boxes = self.contestant.select_boxes(self.boxes, num_to_open)
            
            for box in opened_boxes:
                print(f"Box {box} contained £{self.boxes[box]:,.2f}")
                del self.boxes[box]  # Remove opened box

            # List remaining amounts in ascending order
            remaining_amounts = sorted(self.boxes.values())
            print("\nRemaining amounts in unopened boxes:")
            print(", ".join(f"£{amount:,.2f}" for amount in remaining_amounts))

            offer = self.banker.make_offer(self.boxes, round_number)
            print(f"\nThe Banker offers you £{offer:,.2f}")

            if self.contestant.decide_offer(offer, self.boxes):
                print(f"You accepted the Banker's offer of £{offer:,.2f}. Game over!")
                return

            if self.pause_between_rounds and self.player_type == "llm":
                input("Press Enter to continue to the next round...")

        print("\nFinal round! Revealing your chosen box...")
        print(f"Your box {self.player_box_key} contained £{self.player_box_amount:,.2f}")
