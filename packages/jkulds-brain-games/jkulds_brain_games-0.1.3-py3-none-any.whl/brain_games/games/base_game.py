import prompt


def welcome_user() -> str:
    user = prompt.string("May I have your name? ")
    print("Hello, " + user)
    return user


def run_game(user_name: str,
             greet_message: str,
             print_game_question_and_get_result: callable) -> None:
    print(greet_message)

    run_game_loop(user_name, print_game_question_and_get_result)


def run_game_loop(user_name, print_question_and_get_lap_result):
    needed_correct_answers = 3
    correct_answer_count = 0

    while correct_answer_count < needed_correct_answers:
        result = str(print_question_and_get_lap_result())

        answer_message = "Your answer: "

        answer = prompt.string(answer_message)

        if answer == result:
            print("Correct!")
            correct_answer_count += 1
        else:
            print(f"'{answer}' is wrong answer ;(."
                  f" Correct answer was '{result}'.")
            print(f"Let's try again, {user_name}!")
            break

    if correct_answer_count == needed_correct_answers:
        print(f"Congratulations, {user_name}!")
