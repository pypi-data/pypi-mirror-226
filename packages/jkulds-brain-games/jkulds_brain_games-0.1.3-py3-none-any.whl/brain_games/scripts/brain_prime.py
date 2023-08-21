#!/usr/bin/python3
from brain_games.games.base_game import welcome_user
from brain_games.games.prime_game import prime_game


def main():
    print("Welcome to the Brain Games!")
    user = welcome_user()
    prime_game(user)
