from random import random



with open("C:/Users/moham/VSCode/GuessTheWord/german.txt") as f:
    data = f.read()

score = 4
wordList = data.split("\n")

ranNum = int(random() * 10)

WordToGuess = wordList[ranNum].lower()


SingleWordArray = [len(WordToGuess) * "_"]



def convert(word):
    x = ""
    for letter in word:
        x += letter
    return x
def checkGuess(s):
    
    if s == WordToGuess[i]:
        return True
    else:
        return False
            
def replaceLetter(s):
    for i in range(len(SingleWordArray) -1):
        if checkGuess(s):
            SingleWordArray[i] = s
            print("Correct")
        else:
            print("Wrong")


while score>0:
    print(SingleWordArray)
    if convert(SingleWordArray) == WordToGuess:
        break
    else:
        userInput = input("Start guessing by picking a letter: ").lower()
        replaceLetter(userInput)
        score -= 1
