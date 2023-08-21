from random import randint
from brain_games.games.base_game import run_game


def progression_game(user_name: str) -> None:
    run_game(user_name,
             "What number is missing in the progression?",
             process_progression_question)


def process_progression_question() -> int:
    progression_length = 10
    windows_start = 3
    min_num = 1
    max_num = 5
    progression_diff = randint(min_num, max_num)
    start_num = randint(min_num, max_num)
    result_index = randint(windows_start, progression_length - windows_start)
    num_list = []
    result = 0
    for i in range(progression_length):
        current = start_num + i * progression_diff
        if i == result_index:
            result = current
            num_list.append('..')
        else:
            num_list.append(current)

    print("Question:", " ".join(map(str, num_list)))

    return result
