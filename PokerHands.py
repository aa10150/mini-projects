"""
Poker Hands by Anshu Aramandla

Royal flush: A, K, Q, J, 10 of same suit
Straight flush: Five sequential cards of same suit but not royal flush
Four of a kind: Four cards of same rank plus kicker
Full house: Three cards of one rank plus two of another
Flush: Five non-sequential cards of same suit
Straight: Five sequential cards of mixed suits
Three of a kind: Three cards of same rank plus two kickers
Two pair: Two cards of one rank, two of another, plus kicker
One pair: Two cards of same rank plus three kickers
High card: No matching set, value by highest card

card = [rank, suit]
hand = array of 5 cards
"""

import random

def main():
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ["S", "H", "C", "D"]
    hand = []
    inp = 0
    while inp != 1 and inp != 2:
        try:
            inp = int(input("1 for random hand, 2 to enter hand: "))
        except:
            continue
    if inp == 1:
        while len(hand) < 5:
            rank = random.choice(ranks)
            suit = random.choice(suits)
            card = [rank, suit]
            if card not in hand:
                hand.append(card)
        print()
        printHand(hand)
        checkHand(hand)
    else:
        while len(hand) < 5:
            rank = 0
            suit = "X"
            while True:
                try:
                    inp = int(input("Enter rank (J=11, Q=12, K=13, A=14): "))
                    if inp > 1 and inp < 14:
                        rank = inp
                        break
                except:
                    continue
            while True:
                inp = input("Enter suit (S, H, C, D): ")
                if inp in ["S", "H", "C", "D"]:
                    suit = inp
                    break
            card = [rank, suit]
            if card not in hand:
                hand.append(card)
                print("Card " + cardToStr(card) + " added")
                if len(hand) != 1:
                    print(str(len(hand)) + " cards in hand")
                else:
                    print("1 card in hand")
            else:
                print("Card " + cardToStr(card) + " already in hand")
                if len(hand) != 1:
                    print(str(len(hand)) + " cards in hand")
                else:
                    print("1 card in hand")
        print()
        printHand(hand)
        checkHand(hand)

def checkHand(hand):
    if royalFlush(hand):
        print("Royal Flush")
    elif straightFlush(hand):
        print("Straight Flush")
    elif fourOfAKind(hand):
        print("Four of a Kind")
    elif fullHouse(hand):
        print("Full House")
    elif flush(hand):
        print("Flush")
    elif straight(hand):
        print("Straight")
    elif threeOfAKind(hand):
        print("Three of a Kind")
    elif twoPair(hand):
        print("Two Pair")
    elif onePair(hand):
        print("One Pair")
    else:
        print("High Card")

"""
Three of a kind: Three cards of same rank plus two kickers
Two pair: Two cards of one rank, two of another, plus kicker
One pair: Two cards of same rank plus three kickers
High card: No matching set, value by highest card
"""

def royalFlush(hand):
    ranks = []
    suits = []
    for card in hand:
        ranks.append(card[0])
        suits.append(card[1])
    ranks.sort()
    # check that ranks are 10-A
    if ranks != [10, 11, 12, 13, 14]:
        return False
    # check that suits are the same
    for i in range(1,5):
        if suits[i] != suits[i-1]:
            return False
    return True

def straightFlush(hand):
    return straight(hand) and flush(hand)

def fourOfAKind(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    mismatches = 0
    for i in range(1,5):
        if ranks[i] != ranks[0]:
            mismatches += 1
        if mismatches > 1:
            return False
    return True

def fullHouse(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    ranks.sort()
    rank1 = ranks[0]
    rank2 = 0
    rank1found = 0
    rank2found = 0
    for rank in ranks:
        if rank == rank1:
            rank1found += 1
        if rank == rank2:
            rank2found += 1
        if rank != rank1 and rank2 == 0:
            rank2 = rank
            rank2found = 1
        elif rank != rank1 and rank != rank2:
            return False
    if not (rank1found == 3 and rank2found == 2) and not (rank1found == 2 and rank2found == 3):
        return False
    return True

def flush(hand):
    suits = []
    for card in hand:
        suits.append(card[1])
    # check that suits are the same
    for i in range(1,5):
        if suits[i] != suits[i-1]:
            return False
    return True

def straight(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    ranks.sort()
    # check that suits are sequential
    for i in range(1,5):
        if ranks[i] != ranks[i-1] + 1:
            return False
    return True

def threeOfAKind(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    ranks.sort()
    for i in range(2,15):
            if ranks.count(i) == 3:
                return True
    return False

def twoPair(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    ranks.sort()
    pairs = 0
    for i in range(2,15):
        if ranks.count(i) == 2:
            pairs += 1
    if pairs == 2:
        return True
    return False

def onePair(hand):
    ranks = []
    for card in hand:
        ranks.append(card[0])
    ranks.sort()
    pairs = 0
    for i in range(2,15):
        if ranks.count(i) == 2:
            pairs += 1
    if pairs == 1:
        return True
    return False

def cardToStr(card):
    val = card[0]
    suit = card[1]
    s = ""
    # red for hearts and diamonds
    if suit == "H" or suit == "D":
        s += "\033[31m"
    if val <= 10:
        s += str(val)
    elif val == 11:
        s += "J"
    elif val == 12:
        s += "Q"
    elif val == 13:
        s += "K"
    else:
        s += "A"
    if suit == "S":
        s += "♠"
    elif suit == "H":
        s += "♥\033[0m"
    elif suit == "D":
        s += "♦\033[0m"
    else:
        s += "♣"
    return s

def printHand(hand):
    for card in hand:
        print(cardToStr(card), end=" ")
    print()

# execute main function
if __name__ == "__main__":
    main()