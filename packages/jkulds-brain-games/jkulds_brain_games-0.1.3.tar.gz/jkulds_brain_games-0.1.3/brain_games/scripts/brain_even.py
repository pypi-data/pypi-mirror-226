#!/usr/bin/python3
from brain_games.games.base_game import welcome_user
from brain_games.games.even_game import even_game


def main():
    print("Welcome to the Brain Games!")
    user = welcome_user()
    even_game(user)
