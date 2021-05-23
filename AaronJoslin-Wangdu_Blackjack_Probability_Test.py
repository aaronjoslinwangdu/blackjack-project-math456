# -*- coding: utf-8 -*-
"""
Created on Sat May  1 14:11:47 2021

@author: Aaron Joslin-Wangdu
"""

import numpy as np
import matplotlib.pyplot as plt
import random

suits = ('Diamonds','Hearts','Clubs','Spades')
ranks = ('Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King')
values = {'Ace':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,
           'Jack':10,'Queen':10,'King':10}

inGame = True
hitStand = True

#card class

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
       
class Deck:

    
    
    def __init__(self):
        self.deck = []
        
       
        deckCount = 1
      
        #adjust number of decks here
        while deckCount<2:
            
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit,rank))
            
            deckCount= deckCount + 1     
        
    #print the current deck        
    def __str__(self):
        deckList = ''
        for card in self.deck:
            deckList = deckList + '\n' + card.__str__()
        return 'Current deck is:' + deckList
    
    #shuffle deck
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    #deal a card from the "top" of the deck
    def deal(self):
        singleCard = self.deck.pop()
        return singleCard
    
    def length(self):
        deckLength = 0
        for card in self.deck:
            deckLength = deckLength + 1
        return deckLength

    def dealSpecific(self,card):
        specificCard = Card(card.suit,card.rank)
        self.deck.remove(specificCard)
        
        
        return specificCard
    

class Hand:
    
    def __init__(self):
        self.cards = [] #empty hand at first
        self.value = 0
        self.aces = 0
        
    def addCard(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]
        
        
        
        #change ace value if you go over 21
        if card.rank == 'Ace':
            self.aces = self.aces + 1
    
    
    #chagnes ace values from 11 to 1 and removes "ace" from hand    
    def removeAces(self):
        while self.aces:
            self.value = self.value - 10
            self.aces = self.aces - 1
            
    def clear(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        

#hit function
            
def hit(deck,hand):
    hand.addCard(deck.deal())
    hand.removeAces()
    
    
    
#functions for showing the player's and dealer's hands. only used in testing
    
def showSome(player,dealer):
    print("\nDealer's Hand: ")
    print(" HIDDEN ")
    print('', dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand Total =", player.value)
    

def showAll(player,dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("Dealer's Hand Total=", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand Total =", player.value)
    
def show(player):
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand Total =", player.value)


#ASSUMPTIONS (SIMPLE GAME OF BLACKJACK)

#WE ARE PLAYING WITH ONE DECK OF CARDS

#ONLY ONE PLAYER VS DEALER

#NO SPLITTING, DOUBLING, SURRENDERING

#ACES ARE COUNTED AS 11 UNLESS THEY WOULD MAKE YOU BUST, THEN ALL ACES ARE 
#CHANGED TO BE EQUAL TO 1

#NEW GAME AND DECK EVERY TEST RUN



#calculate the probability of busting for a given hand and deck 
def bustFunc(deck,hand):
    
    
    playerTotal = hand.value    #take players current hand value
    
    
    #calculate value needed to bust the player
    howMuchToBust = 22 - playerTotal
   

    cardsThatBust = []
    cardsThatDontBust = []
    
    
    #checks whether each card left in the deck will make the current hand bust 
    #or not, and adds to respsective lists
    
    for card in deck.deck:
        if values[card.rank] >= howMuchToBust:
            cardsThatBust.append(card.__str__())
        else:
            cardsThatDontBust.append(card.__str__()) 
    
    #probability to bust for the given hand and deck is equal to
    #number of cards left that make you bust / total number of cards left
    
    probToBust = len(cardsThatBust)/deck.length()
    
    return probToBust


def winPercent(maxProbability,gamesPlayed):
    wins = 0
    losses = 0
    
    #this will simulate gamesPlayed amount of games where the player will hit
    #as long as their probability ig lower than maxProbability
    
    for int in range (0,gamesPlayed):
       
        #creates a new deck, player hand, and dealer hand for each "new" game
        deck = Deck()
        deck.shuffleDeck() 
        ph = Hand()
        ph.addCard(deck.deal())
        ph.addCard(deck.deal())
        dh = Hand()
        dh.addCard(deck.deal())
        dh.addCard(deck.deal())
        
        #uses previously defined function to calculate initial probability 
        #to bust
        probToBust = bustFunc(deck,ph)
        
        #while the probability to bust is less than maxProbability, hit
        while probToBust <= maxProbability:
            ph.addCard(deck.deal())
            probToBust = bustFunc(deck,ph)
        
        #value of player hand after they stop hitting
        playerTotal = ph.value   
        
        #make dealer hit while less than 17
        while dh.value < 17:
                hit(deck,dh)    
        
        #value of dealer hand after they stop hitting
        dealerTotal = dh.value
        
        #check who won the game and tally
        if playerTotal > 21:
            losses = losses + 1
        elif dealerTotal > 21:
            wins = wins + 1
        elif dealerTotal >= playerTotal:
            losses = losses + 1
        else:
            wins = wins + 1
        
    #calculate percent of total games that were won
    winPercent = wins/gamesPlayed
        
    return winPercent
    



#this function creates a "matrix" with i,j values corresponding to the 
#probability to bust for any given 2 card hand

def probBustArray():

    cardList1 = [Card('Clubs','Ace'),Card('Clubs','2'),Card('Clubs','3'),Card('Clubs','4')
         ,Card('Clubs','5'),Card('Clubs','6'),Card('Clubs','7'),Card('Clubs','8'),
         Card('Clubs','9'),Card('Clubs','10'),Card('Clubs','Jack'),Card('Clubs','Queen'),
         Card('Clubs','King')]

    cardList2 = [Card('Diamonds','Ace'),Card('Diamonds','2'),Card('Diamonds','3'),Card('Diamonds','4')
         ,Card('Diamonds','5'),Card('Diamonds','6'),Card('Diamonds','7'),Card('Diamonds','8'),
         Card('Diamonds','9'),Card('Diamonds','10'),Card('Diamonds','Jack'),Card('Diamonds','Queen'),
         Card('Diamonds','King')]

    probBustArray = np.zeros((13,13))

    for i in range(0,13):
        for j in range(0,13):
        
            #initialize deck and hand
            deck = Deck()
            ph = Hand()
        
            #add cards to compute all cases
            ph.addCard(deck.dealSpecific(cardList1[i]))     
            ph.addCard(deck.dealSpecific(cardList2[j])) 
        
            x = bustFunc(deck,ph)
        
            probBustArray[i][j] = x
        
        
    return probBustArray
               
    

















    
    