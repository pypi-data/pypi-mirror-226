#!/usr/bin/python3
from brain_games.games.base_game import welcome_user
from brain_games.games.calc_game import calc_game


def main():
    print("Welcome to the Brain Games!")
    user = welcome_user()
    calc_game(user)
