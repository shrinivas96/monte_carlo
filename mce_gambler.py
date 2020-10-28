"""
Simulate the money a gambler wins/loses.
A small change on Sentdex's Monte Carlo Tutorials: https://pythonprogramming.net/monte-carlo-simulator-python/
I have just taken each gabler's final result and mone transition and made a plot of them. Then finally to show
that the house always wins, we take 1000 gamplers and have them play 100 times to see how much the house won.
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


def place_bet(funds, bet_amnt, bet_counts):
    """A function that takes in 'funds' amount of money and places
       'bet_counts' number of bets of 'bet_amnt' money in each bet"""
    value = funds                                       # variable to hold the current about of money gambler has
    track_money = [value]                               # track change of money won/lost. first entry is starting money

    bet_count = 0                                       # total number of bets to be placed = bet_counts
    while bet_count < bet_counts:                       
        if roll_dice():         
            value += bet_amnt                           # if user wins, the money they have increases by bet_amnt
        else:
            value -= bet_amnt                           # or decreases by bet_amnt, if they loose
        bet_count += 1
        track_money.append(value)                       # append the current money for future plotting
    return track_money                                  # return the progress after all bets have been placed


def main():
    house_money = []                                                # how much money did the house win/lose?
    repeat = 1000                                                     # how many gamblers do you want?
    init_money = 10000                                              # initial money given to all
    highest_win = 0                                                 # who one the most?

    plt.figure()                                                    # create simple figure
    plt.axhline(y=init_money, color='g', linestyle='-')             # mark a line where everyone started

    for _ in range(repeat):        
        track_money = place_bet(init_money, 100, 1000)               # list of money transition
        if max(track_money) > highest_win:
            highest_win = max(track_money)

        difference_amnt = track_money[-1] - track_money[0]          # (money gambler took away) - (money they started at)
        house_money.append(difference_amnt)                         # difference_amnt is how much house won/lost

        plt.plot(track_money)                                       # plot the money change for each gambler

    dtext = "House final ammount = " + str(sum(house_money))
    plt.text(0, highest_win, dtext)
    plt.xlabel("Iterations")
    plt.ylabel("Money")
    plt.show()                                                      # show the plot


if __name__ == "__main__":
    main()