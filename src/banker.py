class Banker:
    def make_offer(self, boxes, round_number):
        remaining_amounts = list(boxes.values())
        expected_value = sum(remaining_amounts) / len(remaining_amounts)
        round_multiplier = {
            1: 0.3, 2: 0.4, 3: 0.5, 4: 0.6, 5: 0.8, 6: 0.9
        }
        multiplier = round_multiplier.get(round_number, 0.5)
        return expected_value * multiplier
