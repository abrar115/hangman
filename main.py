import requests
import random

# Fetch a 6-letter word
try:
    response = requests.get("https://api.datamuse.com/words?sp=??????")
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Error fetching word from Datamuse API:", e)
    exit()

words = [w['word'] for w in response.json() if w['word'].isalpha() and len(w['word']) == 6]

if not words:
    print("Could not fetch a 6-letter word. Try again later.")
    exit()

word = random.choice(words).lower()

# Hangman ASCII art
hangman = [r'''
  +---+
  |   |
      |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# Initialize game state
blank_list = ['_' for _ in word]
update_display = 0
mult = 0

print("Would you like to play a game? Or view game history? [YG/NG] to play || [YH/NH] for game history")
msg = input("").strip().lower()

if msg == "yh":
    print(hangman[update_display])
    print(''.join(blank_list))

    while update_display < 6:
        guess = input("Make a guess (one letter): ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            mult += 1
            print("Please guess only one letter.")
            if mult > 3:
                update_display += 1
                print(f"Too many invalid attempts. Penalty applied.")
            print(hangman[update_display])
            continue

        correct = False
        for i, letter in enumerate(word):
            if guess == letter and blank_list[i] == '_':
                blank_list[i] = guess
                correct = True

        if not correct:
            print(f"There is no '{guess}', sorry.")
            update_display += 1

        print(hangman[update_display])
        print(''.join(blank_list))

        if ''.join(blank_list) == word:
            print("🎉 YOU WIN!")
            with open("score.txt", "a") as f:
                f.write("win\n")
            break

    if update_display == 6:
        print("💀 GAME OVER.")
        print(f"The word was: {word}")
        with open("score.txt", "a") as f:
            f.write("loss\n")
    try:
        with open("score.txt", "r") as f:
            lines = f.readlines()
            wins = lines.count("win\n")
            losses = lines.count("loss\n")
            print(f"📊 Game History — Wins: {wins}, Losses: {losses}")
            print(f"Win Rate - {wins/(wins+losses)}")
    except FileNotFoundError:
        print("No previous game history found.")



elif msg !="yg":
    print("Alrighty, let me know when you'd like to play.")

elif msg == "yh":
    try:
        with open("score.txt", "r") as f:
            lines = f.readlines()
            wins = lines.count("win\n")
            losses = lines.count("loss\n")
            print(f"📊 Game History — Wins: {wins}, Losses: {losses}")
            print(f"Win Rate - {wins/(wins+losses)}")
    except FileNotFoundError:
        print("No previous game history found.")
elif msg == "nh":
    print("Alrighty, let me know when you'd like to view game history.")