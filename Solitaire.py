"""
Solitaire by Anshu Aramandla
"""

import random

def main():
    # spades and clubs are black, hearts and diamonds are red
    suits = ["S", "H", "C", "D"]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    deck = []
    for val in values:
        for suit in suits:
            # [card, drawn]
            deck.append([[val, suit], False])
    field = []
    # deal initial cards
    for i in range(7):
        field.append([])
        for j in range(i+1):
            card = pickCard(deck)
            # [card, revealed]
            if j==i:
                # face up card
                field[i].append([card, True])
            else:
                # face down card
                field[i].append([card, False])
    # initialize side deck
    sideDeck = []
    for d in deck:
        if not d[1]:
            sideDeck.append(d)
    random.shuffle(sideDeck)
    SDVisIdx = 0
    SDVisLen = 0
    sStack = []
    hStack = []
    cStack = []
    dStack = []
    while True:
        # check for win
        if len(sStack) == 13 and len(hStack) == 13 and len(cStack) == 13 and len(dStack) == 13:
            break
        sideDeckInView = sideDeck[SDVisIdx:(SDVisIdx+SDVisLen)]
        for item in sideDeck:
            item[1] = False
        for item in sideDeckInView:
            sideDeckItem = sideDeck[sideDeck.index(item)]
            sideDeckItem[1] = True
        printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
        drawFrom = takeInt("Draw from:\n1-7 for columns\n0 for right side stacks\n" \
        "8 for left side deck\n9 for left side cards\n", False)
        # draw from a right side stack
        if drawFrom == 0:
            printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
            drawStack = takeInt("Draw from:\n1 for ♠\n2 for \033[31m♥\033[0m\n3 for ♣\n4 for \033[31m♦\033[0m\n", False)
            printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
            print("\n"*2)
            placeOn = takeInt("Place on:\n1-7 for columns\n", False)
            if drawStack == 1:
                if len(sStack) == 0:
                    continue
                if placeOn > 0 and placeOn <= 7:
                    placeUnderColumnFromStack(sStack, field, placeOn-1)
                else:
                    continue
            elif drawStack == 2:
                if len(hStack) == 0:
                    continue
                if placeOn > 0 and placeOn <= 7:
                    placeUnderColumnFromStack(hStack, field, placeOn-1)
                else:
                    continue
            elif drawStack == 3:
                if len(cStack) == 0:
                    continue
                if placeOn > 0 and placeOn <= 7:
                    placeUnderColumnFromStack(cStack, field, placeOn-1)
                else:
                    continue
            elif drawStack == 4:
                if len(dStack) == 0:
                    continue
                if placeOn > 0 and placeOn <= 7:
                    placeUnderColumnFromStack(dStack, field, placeOn-1)
                else:
                    continue
            else:
                continue
        # draw from a column
        elif drawFrom <= 7:
            colNo = drawFrom - 1
            printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, True)
            print("\n"*2)
            drawRow = takeInt(f"Drawing from column {drawFrom}:\n1-13 for rows\n", False)
            rowNo = drawRow - 1
            # if not within the length of the column
            if rowNo >= len(field[colNo]):
                continue
            # if not a revealed card
            if not field[colNo][rowNo][1]:
                continue
            card = field[colNo][rowNo][0]
            cards = field[colNo][rowNo:]
            printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
            if len(cards) == 1:
                print("\n")
                placeOn = takeInt("Place on:\n1-7 for columns\n0 for right side stacks\n", False)
            else:
                print("\n"*2)
                placeOn = takeInt("Place on:\n1-7 for columns\n", False)
            # place on matching stack
            if placeOn == 0:
                if len(cards) == 1:
                    suit = card[1]
                    match suit:
                        case "S":
                            placeOnStack(sStack, field[colNo], card, field[colNo])
                            if len(field[colNo]) > 0:
                                field[colNo][-1][1] = True
                        case "H":
                            placeOnStack(hStack, field[colNo], card, field[colNo])
                            if len(field[colNo]) > 0:
                                field[colNo][-1][1] = True
                        case "C":
                            placeOnStack(cStack, field[colNo], card, field[colNo])
                            if len(field[colNo]) > 0:
                                field[colNo][-1][1] = True
                        case "D":
                            placeOnStack(dStack, field[colNo], card, field[colNo])
                            if len(field[colNo]) > 0:
                                field[colNo][-1][1] = True
            # place under column
            elif placeOn <= 7:
                if len(field[placeOn-1]) == 0:
                    if card[0] == 13:
                        field[placeOn-1].extend(cards)
                        field[colNo] = field[colNo][:rowNo]
                        if len(field[colNo]) > 0:
                            field[colNo][-1][1] = True
                else:
                    targetCard = field[placeOn-1][-1][0]
                    if checkValidMove(card, targetCard):
                        field[placeOn-1].extend(cards)
                        field[colNo] = field[colNo][:rowNo]
                        if len(field[colNo]) > 0:
                            field[colNo][-1][1] = True
            else:
                continue
        # draw from left side deck
        elif drawFrom == 8:
            # draw one more, hide one if already three
            if SDVisIdx + SDVisLen <= len(sideDeck) - 1:
                if SDVisLen < 3:
                    SDVisLen += 1
                else:
                    SDVisIdx += 1
            # reset side deck
            else:
                SDVisLen = 0
                SDVisIdx = 0
        # draw from left side face up cards
        elif drawFrom == 9:
            if SDVisLen == 0:
                continue
            else:
                printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
                print("\n")
                placeOn = takeInt("Place on:\n1-7 for columns\n0 for right side stacks\n", False)
                card = sideDeckInView[-1][0]
                # place on matching stack
                if placeOn == 0:
                    suit = card[1]
                    match suit:
                        case "S":
                            if placeOnStack(sStack, sideDeck, card, sideDeckInView):
                                if SDVisIdx < 3:
                                    SDVisLen -= 1
                                else:
                                    SDVisIdx -= 1
                        case "H":
                            if placeOnStack(hStack, sideDeck, card, sideDeckInView):
                                if SDVisIdx < 3:
                                    SDVisLen -= 1
                                else:
                                    SDVisIdx -= 1
                        case "C":
                            if placeOnStack(cStack, sideDeck, card, sideDeckInView):
                                if SDVisIdx < 3:
                                    SDVisLen -= 1
                                else:
                                    SDVisIdx -= 1
                        case "D":
                            if placeOnStack(dStack, sideDeck, card, sideDeckInView):
                                if SDVisIdx < 3:
                                    SDVisLen -= 1
                                else:
                                    SDVisIdx -= 1
                # place at bottom of column
                elif placeOn <= 7:
                    if len(field[placeOn-1]) == 0:
                        if card[0] == 13:
                            if SDVisIdx < 3:
                                SDVisLen -= 1
                            else:
                                SDVisIdx -= 1
                            field[placeOn-1].append(sideDeckInView[-1])
                            sideDeck.remove(sideDeckInView[-1])
                    else:
                        targetCard = field[placeOn-1][-1][0]
                        if checkValidMove(card, targetCard):
                            if SDVisIdx < 3:
                                SDVisLen -= 1
                            else:
                                SDVisIdx -= 1
                            field[placeOn-1].append(sideDeckInView[-1])
                            sideDeck.remove(sideDeckInView[-1])
                else:
                    continue
        else:
            continue
    # print win state
    printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, False)
    print("\n"*2)
    print("Win!")

def placeUnderColumnFromStack(stack, field, colNo):
    card = stack[-1][0]
    if len(field[colNo]) == 0:
        if card[0] == 13:
            field[colNo].append(stack[-1])
            stack.pop()
    elif checkValidMove(card, field[colNo][-1][0]):
        field[colNo].append(stack[-1])
        stack.pop()

def placeOnStack(stack, removeFrom, card, takeFrom):
    if len(stack) == 0 and card[0] == 1:
        stack.append(takeFrom[-1])
        removeFrom.remove(takeFrom[-1])
        return True
    elif len(stack) > 0 and card[0] == (stack[-1][0][0] + 1):
        stack.append(takeFrom[-1])
        removeFrom.remove(takeFrom[-1])
        return True
    return False

def checkValidMove(card, targetCard):
    val = card[0]
    suit = card[1]
    targetVal = targetCard[0]
    targetSuit = targetCard[1]
    if (suit == "S" or suit == "C"):
        if (targetSuit == "H" or targetSuit == "D"):
            if (targetVal == val + 1):
                return True
    elif (suit == "H" or suit == "D"):
        if (targetSuit == "S" or targetSuit == "C"):
            if (targetVal == val + 1):
                return True
    else:
        return False

def checkValidStack(card, targetCard):
    val = card[0]
    suit = card[1]
    targetVal = targetCard[0]
    targetSuit = targetCard[1]
    if (val == (targetVal+1) and suit == targetSuit):
        return True
    else:
        return False

def printField(field, sideDeck, sideDeckInView, sStack, hStack, cStack, dStack, showRows):
    print("\n"*30)
    print("      1  2  3  4  5  6  7")
    # side deck
    if len(sideDeck) > 0:
        print("[]   ", end="")
    else:
        print("     ", end="")
    # field
    k = 0
    for i in range(13):
        # main playing field
        for j in range(7):
            if (i < len(field[j])):
                print(cardToStr(field[j][i][0], field[j][i][1]), end=" ")
            else:
                print("   ", end="")
        if showRows:
            print(i+1, end="")
        # right side stacks
        if i == 0:
            if showRows:
                print(" ", end="")
            else:
                print("  ", end="")
            if len(sStack) > 0:
                print(cardToStr(sStack[-1][0], sStack[-1][1]), end=" ")
            else:
                print("[]", end="")
        elif i == 2:
            if showRows:
                print(" ", end="")
            else:
                print("  ", end="")
            if len(hStack) > 0:
                print(cardToStr(hStack[-1][0], hStack[-1][1]), end=" ")
            else:
                print("[]", end="")
        elif i == 4:
            if showRows:
                print(" ", end="")
            else:
                print("  ", end="")
            if len(cStack) > 0:
                print(cardToStr(cStack[-1][0], cStack[-1][1]), end=" ")
            else:
                print("[]", end="")
        elif i == 6:
            if showRows:
                print(" ", end="")
            else:
                print("  ", end="")
            if len(dStack) > 0:
                print(cardToStr(dStack[-1][0], dStack[-1][1]), end=" ")
            else:
                print("[]", end="")
        print()
        # side deck
        if k < len(sideDeckInView):
            if i+1 == len(sideDeckInView):
                print(cardToStr(sideDeckInView[k][0], sideDeckInView[k][1]), end="*  ")
            else:
                print(cardToStr(sideDeckInView[k][0], sideDeckInView[k][1]), end="   ")
        else:
            print("     ", end="")
        k += 1
    print()

def pickCard(deck):
    # check if there are any cards left
    noCardsLeft = True
    for d in deck:
        if not d[1]:
            noCardsLeft = False
    if noCardsLeft:
        return None
    num = random.randint(0, len(deck)-1)
    # try again if already drawn
    if deck[num][1]:
        return pickCard(deck)
    # draw card
    else:
        deck[num][1] = True
        return deck[num][0]

def cardToStr(card, faceUp):
    if not faceUp:
        return "[]"
    val = card[0]
    suit = card[1]
    s = ""
    # red for hearts and diamonds
    if suit == "H" or suit == "D":
        s += "\033[31m"
    if val == 1:
        s += "A"
    elif val <= 9:
        s += str(val)
    elif val == 10:
        s += "T"
    elif val == 11:
        s += "J"
    elif val == 12:
        s += "Q"
    else:
        s += "K"
    if suit == "S":
        s += "♠"
    elif suit == "H":
        s += "♥\033[0m"
    elif suit == "D":
        s += "♦\033[0m"
    else:
        s += "♣"
    return s

def takeInt(s, repeat):
    num = 0
    while True:
        try:
            num = int(input(s))
            break
        except ValueError:
            print("Invalid input")
            if not repeat:
                s = ""
    return num

# execute main function
if __name__ == "__main__":
    main()