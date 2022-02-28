
"""
Author: Kevin Peterson
Course: OSU CS 361 - Software Engineering I
Assignment: Team Project, Microservice
File: GameLeaderboard.py

Description: Python file that takes an individual entry from a winner file (name,score) named 'LastWinnerScore.txt', e.g.

Sarah Scholl,25

It then uses the entry to create a leaderboard (name,score) file named 'Leaderboard.txt' which displays entries in order
from highest to lowest, e.g.

Rachel Scholl,18
Ben B,15
James,12
Henry-Hearst,4

Useage:
GameLeaderboard.py
or
GameLeaderboard.py numLeaders
"""

#--------------------------------------
# Module imports
#--------------------------------------
import sys
from os.path import exists

#--------------------------------------
# Helper classes
#--------------------------------------

# Winner class to make comparison easier
class Winner:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    # custom equality check so we don't add duplicates
    def __eq__(self, other):
        return self.getScore() == other.getScore() and self.getName() == other.getName()

    def getName(self):
        return self.name

    def getScore(self):
        return self.score

#--------------------------------------
# Global variables
#--------------------------------------
DEFAULT_NUM_LEADERS = 10
numLeadersToWrite = DEFAULT_NUM_LEADERS
lastWinnerFileName = "LastWinnerScore.txt"
leaderboardFileName = "Leaderboard.txt"

#--------------------------------------
# Program logic
#--------------------------------------

# Recieves the most recent winner from parseLastWinnerFile, then updates the current leaderboard as needed
def updateLeaderboard(nextWinner):
    # create new list of winners and start by adding our newest
    winners = []
    winners.append(nextWinner)

    # create leaderboard file if it doesn't exist yet and populate winners list using data from file
    with open(leaderboardFileName, 'r+') as file:
        for line in file:
            winnerInfo = line.strip()
            winnerInfo = winnerInfo.split(",")
            winners.append(Winner(winnerInfo[0], int(winnerInfo[1])))

    # sort list by score and re-write file using top scores (no repeating matching entries)
    winners.sort(key=lambda x: x.getScore(), reverse=True)
    finalWinnersList = []
    [finalWinnersList.append(winner) for winner in winners if winner not in finalWinnersList]

    # only write as many names as we have room for
    numToWrite = numLeadersToWrite
    if len(finalWinnersList) < numToWrite:
        numToWrite = len(finalWinnersList)

    # open file, clear contents, and write final winner list, 1 per line in format of (name, score)
    with open(leaderboardFileName, 'r+') as file:
        file.truncate(0)
        for i in range(numToWrite):
            lineToWrite = finalWinnersList[i].getName() + "," + str(finalWinnersList[i].getScore()) + "\n"
            file.write(lineToWrite)


# Attempts to parse the last winner file in order to create a new Winner instance, which it then passes to the
# updateLeaderboard(nextWinner) function
def parseLastWinnerFile():
    lastWinnerFileExists = exists(lastWinnerFileName)
    if lastWinnerFileExists:
        fileLastWinner = open(lastWinnerFileName, "r")
        fileContents = fileLastWinner.read()
        fileLastWinner.close()
        if fileContents == "":
            print("GameLeaderboard.py failed to update leaderboard because the file was empty:", lastWinnerFileName)
        else:
            # Found valid data in file in form of "name,score", process new winner and pass to leaderboard function
            fileContents = fileContents.strip()
            fileContents.replace(" ,", ",")
            fileContents.replace(", ", ",")
            winnerInfo = fileContents.split(",")
            nextWinner = Winner(winnerInfo[0], int(winnerInfo[1]))
            updateLeaderboard(nextWinner)
    else:
        print("GameLeaderboard.py failed to update leaderboard because it could not find the required file:", lastWinnerFileName)

# entry point callback function
def main():
    parseLastWinnerFile()

# Run file as standalone, entry point
if __name__ == "__main__":
    # Allow for variable length leaderboard, passed as 1st argument
    numLeadersToWrite = DEFAULT_NUM_LEADERS

    if (len(sys.argv) > 1):
        numLeadersToWrite = sys.argv[1]

    main()