# Deniz Kaya 280201033
# Kürşat Çağrı Yakıcı 290201098

import random as rd

def getPinInputs(): # function to get valid inputs from the user

    # used flags to ask repeatedly until valid inputs are given
    roll1Invalid = True
    roll2Invalid = True
    roll2 = -1 # if it is a strike, this will return along with roll1, since it would be beneficial to count total rolls to determine where the game will end, although negative numbers for rolls will not be printed in ball score lists

    while roll1Invalid:
        roll1 = int(input("Pins: "))

        if roll1 > 10 or roll1 < 0:
            print("An invalid input")
        else:
            roll1Invalid = False

    if roll1 != 10:

        while roll2Invalid:
            roll2 = int(input("Pins: "))

            if roll1 + roll2 > 10 or roll2 < 0:
                print("An invalid input")
            else:
                roll2Invalid = False
    
    return roll1, roll2

def getLastFrameInputs(): # function to get valid inputs from the user for the last frame
    # used flags to ask repeatedly until valid inputs are given
    roll1Invalid = True
    roll2Invalid = True
    roll3Invalid = True
    roll3 = -1 # roll3 will return -1 if there is neither spare nor strike on the last frame
    while roll1Invalid:
        roll1 = int(input("Pins: "))
        if roll1 > 10 or roll1 < 0:
            print("An invalid input")
        else:
            roll1Invalid = False

    if roll1 != 10:

        while roll2Invalid:
            roll2 = int(input("Pins: "))

            if roll1 + roll2 > 10 or roll2 < 0:
                print("An invalid input")
            else:
                roll2Invalid = False

    elif roll1 == 10:
        while roll2Invalid:
            roll2 = int(input("Pins: "))

            if roll2 > 10 or roll2 < 0:
                print("An invalid input")
            else:
                roll2Invalid = False

    if (roll1 == 10 and roll2 == 10) or (roll1 + roll2 == 10): # conditions where roll3 can be max 10 regardless of what roll 2 is
        while roll3Invalid:
            roll3 = int(input("Pins: "))

            if roll3 > 10 or roll3 < 0:
                print("An invalid input")
            else:
                roll3Invalid = False
    
    elif roll1 == 10 and roll2 < 10: # conditions where max roll3 is determined by roll2
        while roll3Invalid:
            roll3 = int(input("Pins: "))

            if roll2 + roll3 > 10 or roll3 < 0:
                print("An invalid input")
            else:
                roll3Invalid = False

    return roll1, roll2, roll3

def printBallScores(ballScoreList): # function to print ball scores
    print(f"Ball scores: ", end="")
    for score in ballScoreList:
        if score >= 0: # so that negative numbers to distinguish will not be shown when they are in the list
            print(score, end=" ")
    print()
    
def printTotalScores(totalScoreList): # function to print total scores
    print("Total scores: ", end="")
    index = 0
    for score in totalScoreList:
        print(score, end="")
        if index != 9:
            print(" | ", end="")
        index += 1
    for i in range(0, 9 - len(totalScoreList)):
        print(" | ", end="")
    print()
    
def calculateTotalScore(ballScoreList, totalScoreList, pocket):
    if isDoubleStrikeInPocket(pocket): # if there are two strikes in the pocket, whatever the user scores next, roll1 will be added with first two strikes and will be appended to the frame which was 2 frames ago
        twoPreviousFrameScore = pocket[0] + pocket[1] + ballScoreList[-2]
        
        if len(totalScoreList) > 0:
            twoPreviousFrameScore += totalScoreList[-1]

        totalScoreList.append(twoPreviousFrameScore)

        pocket[0] = 0 # setting the pocket as zero because we used the first strike in addition

    if isSingleStrikeInPocket(pocket): # there is one strike in the pocket
        if isStrike(ballScoreList): # if there is a strike again, pocket will be updated to 10, 10 from 0, 10, nothing will be appended
            pocket[0] = 10
        else: # if it is either spare or open frame, roll1 and roll2 will be added together with the strike and will be appended to the score list on the one previous frame
            previousFrameScore = pocket[1] + ballScoreList[-1] + ballScoreList[-2]

            if len(totalScoreList) > 0:
                previousFrameScore += totalScoreList[-1]
            totalScoreList.append(previousFrameScore)

            pocket[1] = 0
          
    if isSpare(pocket): # one spare in pocket, roll1 will be added together with these values and they will be appended to the previous frame
        if pocket[0] == -1: # handling the roll1: 0 roll2: 10 case here for spare
            pocket[0] = 0
        
        previousFrameScore = ballScoreList[-2] + pocket[0] + pocket[1]
        
        if len(totalScoreList) > 0:
            previousFrameScore += totalScoreList[-1]
        totalScoreList.append(previousFrameScore)
        # setting pockets as zero because spare is used for addition
        pocket[0] = 0
        pocket[1] = 0
        
    
    if isStrike(ballScoreList): # if player strikes on the frame
        if isSingleStrikeInPocket(pocket): # two strikes will be saved in the pockets if there is one in it already
            pocket[0] = 10
        else: # if there is no strikes already, pocket will be updated accordingly and now the player has one strike in the pocket
            pocket[1] = 10
    

    if isSpare(ballScoreList) and isEmpty(pocket): # if pocket is empty and the frame is spare, nothing is added to the frame, only the pockets are updated
        # 0 10 geliyosa rollar 0,10 degil -1,10
        if ballScoreList[-2] == 0:
            pocket[0] = -1 # handling the roll1: 0 roll2: 10 case so that the program understands it is a spare and not a strike
            pocket[1] = 10
        else: # if spare is anything else other than 0, 10
            pocket[0] = ballScoreList[-2]
            pocket[1] = ballScoreList[-1]

    if not isStrike(ballScoreList) and not isSpare(ballScoreList) and isEmpty(pocket): # no spare, no strike, pocket is empty, both rolls will be added together and will be appended to the score list
        frameScore = ballScoreList[-1] + ballScoreList[-2]
        if len(totalScoreList) > 0:
            frameScore += totalScoreList[-1]
        
        totalScoreList.append(frameScore)

def handleLastFrame(ballScoreList, totalScoreList, pocket): # last frame functions a bit different, therefore this function is to handle that
    roll1, roll2, roll3 = getLastFrameInputs()
    
    ballScoreList.append(roll1)
    ballScoreList.append(roll2)
    if roll3 >= 0:
        ballScoreList.append(roll3)
        
    printBallScores(ballScoreList)
    
    if isSpare(pocket): # spare in pocket
        if pocket[0] == -1: # handling 0, 10 spare case
            pocket[0] = 0

        previousFrameScore = roll1 + pocket[0] + pocket[1] + totalScoreList[-1] # spare will be added together with two rolls and total score will be appended to the previous frame
        totalScoreList.append(previousFrameScore)

        pocket[0] = 0 # resetting the pockets after addition
        pocket[1] = 0
    
    if isDoubleStrikeInPocket(pocket): # double strike in pocket
        twoPreviousFrameScore = pocket[0] + pocket[1] + roll1 + totalScoreList[-1] # using both of the strikes for addition from the frame number 8 and 9, summing them with first roll on the last frame
        totalScoreList.append(twoPreviousFrameScore) # result is added to the 2 frames before

        pocket[0] = 0 # pocket is updated because one strike is used
    
    # Pocketimda single strike var -> bir oncekine yaziyoruz 9. 
        # 10 + roll1 + roll2 + totalScoreList[-1] -> totalScoreList append
        # clear pocket -> 0,0
    if isSingleStrikeInPocket(pocket): # one strike in pocket
        previousFrameScore = pocket[1] + roll1 + roll2 + totalScoreList[-1] # strike is used with roll1 and roll2
        totalScoreList.append(previousFrameScore) # summing all together, the result is to be added for total score for the 9. frame

        pocket[1] = 0 # strike in the pocket is used
    
    roll3 = 0 if roll3 == -1 else roll3 # if the last frame is an open frame, setting roll3 as 0 because it was -1
    frameScore = roll1 + roll2 + roll3 + totalScoreList[-1] # the last frame's scores
    totalScoreList.append(frameScore)
        
    printTotalScores(totalScoreList)

def isStrike(ballScoreList):
    return ballScoreList[-2] == 10

def isSingleStrikeInPocket(pocket):
    return pocket[0] == 0 and pocket[1] == 10

def isDoubleStrikeInPocket(pocket):
    return pocket[0] == 10 and pocket[1] == 10

def isSpare(list):
    return list[-1] + list[-2] == 10 or list[-2] == -1
    
def isEmpty(pocket):
    return pocket[0] == 0 and pocket[1] == 0

def main():
    currentPlayer = "A" if rd.randint(0, 1) else "B" # choosing a random player
    ballScoresA = []
    ballScoresB = []
    totalScoresA = []
    totalScoresB = []
    pocketA = [0, 0]
    pocketB = [0, 0]
    
    while True:
        currentBallScoreList = ballScoresA if currentPlayer == "A" else ballScoresB # cycling between ball score list for individual players so that the scores are appended to the corresponding list of the player
        currentTotalScoreList = totalScoresA if currentPlayer == "A" else totalScoresB # cycling between total score list for individual players so that the scores are appended to the corresponding list of the player
        currentPocket = pocketA if currentPlayer == "A" else pocketB # cycling between pockets for individual players so that spares and strikes are stored in the corresponding list of the player
        
        print(f"Player {currentPlayer} rolls...")
        roll1, roll2 = getPinInputs() # get rolls
        
        # append rolls to the ball score list
        currentBallScoreList.append(roll1)
        currentBallScoreList.append(roll2)

        printBallScores(currentBallScoreList)
        
        calculateTotalScore(currentBallScoreList, currentTotalScoreList, currentPocket)
        
        printTotalScores(currentTotalScoreList)
        
        # change players at the end of the turn
        if currentPlayer == "A": 
            currentPlayer = "B"
        else:
            currentPlayer = "A"
        # if length of ball score list is 18, it means that 9 frames are played for both players    
        if len(ballScoresA) == 18 and len(ballScoresB) == 18:
            break
    
    # procedure on the last frame is a bit different, therefore it is handled after the loop ends and 9. frame is played
    if currentPlayer == "A": # continuing with player A if he was the starting player
        print("Player A rolls...")
        handleLastFrame(ballScoresA, totalScoresA, pocketA)
        print("Player B rolls...")
        handleLastFrame(ballScoresB, totalScoresB, pocketB)
    else: # continuing with player B if he was the starting player
        print("Player B rolls...")
        handleLastFrame(ballScoresB, totalScoresB, pocketB)
        print("Player A rolls...")
        handleLastFrame(ballScoresA, totalScoresA, pocketA)
        
    # comparing total scores
    if totalScoresA[-1] == totalScoresB[-1]:
        print("It's a tie!")
    else:
        winner = "A" if totalScoresA[-1] > totalScoresB[-1] else "B"
        print(f"Winner is Player {winner}")

if __name__ == "__main__":
    main()
