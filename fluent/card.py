import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range (2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits 
                                        for rank in self.ranks]
        
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
    
    
deck = FrenchDeck()
#print(len(deck))
#print(deck[12], deck[25], deck[38], deck[51])
#print(choice(deck), choice(deck), choice(deck), choice(deck))
#for card in reversed(deck):
#    print(card)
#print(Card('Q', 'hearts') in deck)
#print(Card('A', 'beasts') in deck)
#suit_values = dict(spades = 3, hearts = 2, diamonds = 1, clubs = 0)

#def spades_high_sort(card):
#        rank_value = FrenchDeck.ranks.index(card.rank)
#        return rank_value * len(suit_values) + suit_values[card.suit]

#for card in sorted(deck, key=spades_high_sort):
#    print(card)
#ba = bytearray(b'Abc')
#print(chr(ba[0]))
#print(ba.decode())
#ba[0] = 72
#ba[1] = ord('i')
#print(ba.decode())
