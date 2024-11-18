import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

class Contestant:
    def __init__(self, player_type="human"):
        self.player_type = player_type
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if self.player_type == "llm":
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    def select_boxes(self, boxes, num_to_open):
        remaining_boxes = list(boxes.keys())

        if self.player_type == "human":
            print(f"Remaining boxes: {sorted(remaining_boxes)}")
            boxes = input(f"Enter {num_to_open} boxes to open, separated by commas: ")
            return list(map(int, boxes.split(",")))
        else:
            return random.sample(remaining_boxes, num_to_open)

    def decide_offer(self, offer, boxes):
        remaining_boxes = list(boxes.keys())
        remaining_amounts = sorted(boxes.values())
        if self.player_type == "human":
            decision = input(f"Do you accept the offer of £{offer:,.2f}? (deal/no deal): ").strip().lower()
            return decision == "deal"
        elif self.player_type == "random":
            # LLM logic to decide based on offer
            decision = random.random() < 0.1
            print(decision)
            return decision  # Placeholder logic
        else:
                        # Use LLM to evaluate the offer
            prompt = PromptTemplate(
                input_variables=["offer", "remaining_boxes", "remaining_amounts"],
                template="""
You are playing Deal or No Deal. The Banker has offered you £{offer:,.2f}.
The remaining boxes are: {remaining_boxes}.
The amounts in the remaining boxes are: {remaining_amounts}.

Consider:
- The average value of the remaining amounts.
- The likelihood of obtaining a higher value by continuing.
- Risk tolerance and potential winnings.

Respond with either "deal" to accept the offer or "no deal" to decline it.
"""
            )
            input_text = prompt.format(
                offer=offer,
                remaining_boxes=sorted(remaining_boxes),
                remaining_amounts=[f"£{amount:,.2f}" for amount in remaining_amounts],
            )
            response = self.llm(input_text).content.lower().strip()

            # Check for "deal" or "no deal" explicitly in the response
            if "no deal" in response:
                return False  # Decline the offer
            elif "deal" in response:
                return True  # Accept the offer
            else:
                # Fallback if the response is ambiguous
                print("LLM response was unclear; defaulting to 'no deal'.")
                return False