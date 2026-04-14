"""
Polyrhythm Player by Anshu Aramandla
Run in Python virtual environment with pygame-ce
"""
import time
import math
import pygame

def main():
    pygame.mixer.init()
    strong = pygame.mixer.Sound("strong_beat.wav")
    weak = pygame.mixer.Sound("weak_beat.wav")
    other = pygame.mixer.Sound("other_beat.mp3")
    numTs = takeInt("Number of rhythms: ")
    tArray = []
    for i in range(numTs):
        s = "Rhythm " + str(i+1) + ": "
        if i == 0:
            tArray.append(takeInt("Base rhythm: "))
        else:
            tArray.append(takeInt(s))
    lcm = math.lcm(*tArray)
    if lcm > 120:
        print("LCM too high (" + str(lcm) + "). Choose a simpler polyrhythm with LCM <= 120.")
        exit()
    tempo = takeInt("Tempo (BPM): ")
    secondsPerBeat = (60 / tempo) / (lcm/tArray[0])
    displayNumsInput = input("Display numbers? (Y/N) ").capitalize()
    displayNums = False
    if displayNumsInput == "Y":
        displayNums = True
    i = 0
    while True:
        if (i >= lcm):
            i = 0
        if i == 0:
            strong.play()
        elif i % (lcm/tArray[0]) == 0:
            weak.play()
        else:
            for t in tArray:
                if i % (lcm/t) == 0:
                    other.play()
        print("\n"*50)
        print(" "*(i+5), end="")
        print("*")
        printPR(tArray, lcm, displayNums)
        i += 1
        time.sleep(secondsPerBeat)

def takeInt(s):
    numTs = 0
    while True:
        try:
            numTs = int(input(s))
            break
        except ValueError:
            print("Integer required")
    return numTs

def printPR(tArray, lcm, nums):
    for tempo in tArray:
        div = int(lcm / tempo)
        print(str(tempo).rjust(3), end=": ")
        for t in range(tempo):
            if nums:
                print((t+1)%10, end="")
            else:
                print("■", end="")
            print("□"*(div-1), end="")
        print()

# execute main function
if __name__ == "__main__":
    main()