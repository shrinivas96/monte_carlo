"""
A small change on Sentdex's Monte Carlo Tutorials: https://pythonprogramming.net/monte-carlo-simulator-python/
I have just taken each gabler's final result and mone transition and made a plot of them.
"""
import matplotlib.pyplot as plt
import random


def roll_dice():
    """Rolling a dice between 1-100 and placing a bet on the outcome.
       If the number comes out to be in the range [51, 99], then the 
       user wins or else the 'house ' wins. """
    roll = random.randint(1, 100)                       # randomly picks a number N such that 1 <= N <= 100

    if roll <= 50:                                      # house wins for number 1-50
        return False                                    # so false for the user
    elif 50 < roll < 100:                               
        return True                                     # win for the user
    elif roll == 100:
        return False                                    # user loses even when the number 100 appears


def place_bet(funds, bet_amnt, wage_count):
    """A function that takes in 'funds' amount of money and places
       'wage_count" number of bets of 'bet_amnt' money in each bet"""
    value = funds                                       # variable to hold the current about of money gambler has
    track_money = [value]                               # to track the change of how much money they win/lose

    bet_count = 0                                       # total number of bets to be placed = wage_count
    while bet_count < wage_count:                       
        if roll_dice():         
            value += bet_amnt                           # if user wins, the money they have increases by bet_amnt
        else:
            value -= bet_amnt                           # or decreases by bet_amnt, if they loose
        bet_count += 1
        track_money.append(value)                       # append the current money for future plotting
        # print("Funds now: ", value)
    return track_money                                  # return the progress after all bets have been placed


def main():
    repeat = 10                                                     # how many gamblers do you want?
    init_money = 10000                                              # initial money given to all
    plt.figure()                                                    # create simple figure
    plt.axhline(y=init_money, color='g', linestyle='-')             # mark a line where everyone started
    for _ in range(repeat):                                     
        plt.plot(place_bet(init_money, 100, 100))                   # plot the money change for each gambler
    plt.xlabel("Iterations")
    plt.ylabel("Money")
    plt.show()                                                      # show the plot


if __name__ == "__main__":
    main()