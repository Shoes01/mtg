import random

class Deck:
    def __init__(self, cards):
        self._cards = cards     
        self.library = cards.copy()
        self.hand = []


    def restock_library(self):
        self.library = self._cards.copy()
        random.shuffle(self.library)
        print(f"Library back up to {len(self.library)} cards.")


    def new_hand(self):
        self.restock_library()
        self.hand.clear()

        for _ in range(0, 7):
            self.draw()
    

    def draw(self):
        self.hand.append(self.library.pop())
