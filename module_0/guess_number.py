"""Guess a number game"""
import numpy as np
import math


def game_core_v3(number, lower_limit=1, upper_limit=100):
    """
    The function takes a hidden number and its range and returns this number and the count of attempts to success
    or None if the number was not guessed successfully.
    The number is guessed via "bisection method".
    Expected count of trials for worth case is about log2(upper_limit-lower_limit)
    where upper_limit and lower_limit are upper and lower limits of specified number range.
    """

    # just not to forget our initial range
    lower = lower_limit
    upper = upper_limit

    count = 0
    predict = round((lower + upper) / 2)
    while lower != upper:
        count += 1
        if number == predict:
            return number, count  # return from loop and function if guessed
        elif number > predict:
            lower = predict  # shift lower limit up
            predict = math.ceil((predict + upper) / 2)
        elif number < predict:
            upper = predict  # shift upper limit down
            predict = math.floor((lower + predict) / 2)
    else:
        print(f'Sorry, the hidden number={number} is not in the expected range=[{lower_limit},{upper_limit}] :-(')

    return number, None  # exit with None value for "count to success"


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    lower_limit = 1
    upper_limit = 100
    run_times = 1000

    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(lower_limit, upper_limit + 1, size=run_times)
    for number in random_array:
        count_ls.append(game_core(number, lower_limit, upper_limit)[1])
    score = np.mean(count_ls)
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


if __name__ == "__main__":
    score_game(game_core_v3)
