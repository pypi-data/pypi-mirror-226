from random import choice, randint

from brain_games.games.base_game import run_game


def calc_game(user_name: str) -> None:
    run_game(user_name,
             "What is the result of the expression?",
             process_calc_question)


def process_calc_question() -> int:
    signs = ['+', '-', '*']
    sign = choice(signs)
    min_num = 3
    max_num = 10
    a = randint(min_num, max_num)
    b = randint(min_num, max_num)
    result = 0
    match sign:
        case '+':
            result = a + b
        case '-':
            result = a - b
        case '*':
            result = a * b

    print("Question:", a, sign, b)

    return result
