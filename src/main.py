from game import DealOrNoDealGame

def main():
    print("Welcome to Deal or No Deal!")
    mode = input("Who will play the game? (human/llm): ").strip().lower()
    pause_between_rounds = False

    if mode == "llm":
        pause_input = input("Pause between rounds? (yes/no): ").strip().lower()
        pause_between_rounds = pause_input == "yes"

    game = DealOrNoDealGame(player_type=mode, pause_between_rounds=pause_between_rounds)
    game.play()

if __name__ == "__main__":
    main()
