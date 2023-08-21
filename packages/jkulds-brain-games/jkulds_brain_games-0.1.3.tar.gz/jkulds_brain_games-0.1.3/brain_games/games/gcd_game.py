from random import randint

from brain_games.games.base_game import run_game


def gcd_game(user_name: str) -> None:
    run_game(user_name,
             "Find the greatest common divisor of given numbers.",
             process_gcd_question)


def gcd(a, b):
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a


def process_gcd_question() -> int:
    min_num = 1
    max_num = 100
    a = randint(min_num, max_num)
    b = randint(min_num, max_num)
    result = gcd(a, b)

    print("Question:", a, b)

    return result
