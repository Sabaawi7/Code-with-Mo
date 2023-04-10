word = "hello"
testWord = len(word) * ["_"]
word_list = list(word)


score = 10

def checkContains(char, word):
    return char in word


def replaceChar(char, word, word_duplicate):
    for i in range(len(word)):
        if word[i] == char:
            word_duplicate[i] = word[i]

def representWordDuplicate():
    print ("".join(testWord))






while True:
    if (representWordDuplicate() == word):
        print("Game won")
        break
    elif score == 0:
        print("Game over")
        break


    elif (checkContains(userInput = input("Enter a letter:").lower(), word)):
        
        replaceChar(userInput, word, testWord)
        representWordDuplicate()
    else:
        score -= 1
    








# def contains(word, testLetter):
#     for letter in word:
#         if testLetter == letter:
#             return True
#         else:
#             return False
# if contains(word, userInput):
#     for i in range(len(word)):
#         if userInput == word[i]:
#             testWord = testWord.replace(testWord[i], userInput)
#     print("Correct")
# else:
#     print("Wrong")

# print(testWord)


