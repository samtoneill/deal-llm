import random

class Contestant:
    def __init__(self, player_type="human"):
        self.player_type = player_type

    def select_boxes(self, boxes, num_to_open):
        remaining_boxes = list(boxes.keys())

        if self.player_type == "human":
            print(f"Remaining boxes: {sorted(remaining_boxes)}")
            boxes = input(f"Enter {num_to_open} boxes to open, separated by commas: ")
            return list(map(int, boxes.split(",")))
        else:
            return random.sample(remaining_boxes, num_to_open)

    def decide_offer(self, offer, boxes):
        if self.player_type == "human":
            decision = input(f"Do you accept the offer of £{offer:,.2f}? (deal/no deal): ").strip().lower()
            return decision == "deal"
        else:
            # LLM logic to decide based on offer
            return random.random() < 0.1  # Placeholder logic
