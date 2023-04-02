from random import randint
from time import sleep


def get_user_guess():
    guess = int(input("Please enter your guess: "))
    return guess


def roll_dice(number_of_sides):
    first_roll = randint(1, number_of_sides)
    second_roll = randint(1, number_of_sides)
    max_val = number_of_sides * 2
    print("The maximum possible value is %d" % max_val)
    guess = get_user_guess()
    if guess > max_val:
        print("Your guess is invalid")
    else:
        print("Rolling...")
        sleep(2)
        print("the first roll is %d" % first_roll)
        sleep(2)
        print("the second roll is %d" % second_roll)
        sleep(2)
        total_roll = first_roll + second_roll
        print("The total roll is %d" % total_roll)
        print("Result....")
        sleep(2)
        if total_roll == guess:
            print("congrats you have won")
        else:
            print("you have lost. good luck next time!")


roll_dice(6)
