#!/usr/bin/env python3
"""
SIMPLE WHEEL OF FORTUNE WITH CHATGPT COMMENTARY - STARTER FILE
===============================================================

This is a simplified version that combines everything you need in one file!
Just save this as "wheel_of_fortune_commentary.py" and run it!

Requirements:
- pip install openai (optional - works without it too!)
- OpenAI API key (optional - has fallback commentary)

Usage:
python wheel_of_fortune_commentary.py
"""

import random
import time
import os

# Simple Commentary System (embedded)
class SimpleCommentary:
    def __init__(self, style="dramatic"):
        self.style = style
        self.fallback_comments = {
            "game_start": [
                "🎡 Welcome to Wheel of Fortune! Let's see what puzzles await us today!",
                "🎯 The wheel is ready to spin! May fortune favor our contestants!",
                "✨ Another exciting game begins! Who will solve today's puzzle?"
            ],
            "wheel_spin": [
                "🌪️ The wheel is spinning... where will it land?",
                "🎰 Round and round it goes... building the suspense!",
                "⚡ Here comes the spin that could change everything!"
            ],
            "correct": [
                "🎉 Excellent guess! The letters are revealed!",
                "✅ Right on target! Great strategy!",
                "🌟 Perfect! The puzzle is coming together!"
            ],
            "wrong": [
                "❌ Not in the puzzle! Better luck next time!",
                "🤔 Close, but not quite! The mystery continues!",
                "🎯 Sometimes the best guesses don't pan out!"
            ],
            "bankrupt": [
                "💸 Oh no! Bankrupt! That's the risk of the wheel!",
                "😱 All those winnings... gone in a spin!",
                "🎭 The wheel giveth, and the wheel taketh away!"
            ]
        }
    
    def comment(self, event_type):
        """Get a random comment for the event"""
        time.sleep(1)  # Dramatic pause
        if event_type in self.fallback_comments:
            comment = random.choice(self.fallback_comments[event_type])
            print(f"\n🎙️ COMMENTARY: {comment}\n")

# Simple Game Implementation
class SimpleWheelOfFortune:
    def __init__(self):
        self.commentary = SimpleCommentary()
        self.puzzles = [
            ("WHEEL OF FORTUNE", "TV SHOW"),
            ("ARTIFICIAL INTELLIGENCE", "TECHNOLOGY"),
            ("PYTHON PROGRAMMING", "COMPUTER SCIENCE"),
            ("CHATGPT COMMENTARY", "AI FEATURE"),
            ("GAME SHOW HOST", "ENTERTAINMENT")
        ]
        
    def spin_wheel(self):
        """Spin the wheel and return result"""
        values = [-1, 0, 500, 600, 700, 800, 900, 1000]  # -1=bankrupt, 0=lose turn
        print("🎡 Spinning the wheel...")
        time.sleep(2)
        result = random.choice(values)
        
        if result == -1:
            print("💥 BANKRUPT!")
            self.commentary.comment("bankrupt")
            return -1
        elif result == 0:
            print("😔 Lose a turn!")
            return 0
        else:
            print(f"💰 ${result}!")
            self.commentary.comment("wheel_spin")
            return result
    
    def play_simple_game(self):
        """Play a simplified version of the game"""
        puzzle, clue = random.choice(self.puzzles)
        print("🎡 WHEEL OF FORTUNE WITH CHATGPT COMMENTARY")
        print("=" * 50)
        
        self.commentary.comment("game_start")
        
        print(f"Category: {clue}")
        
        # Show puzzle with blanks
        showing = ""
        for char in puzzle:
            if char.isalpha():
                showing += "_"
            else:
                showing += char
        
        print(f"Puzzle: {showing}")
        print()
        
        guessed_letters = []
        winnings = 0
        
        while "_" in showing:
            print(f"Current winnings: ${winnings}")
            print(f"Guessed letters: {', '.join(guessed_letters)}")
            print(f"Puzzle: {showing}")
            print()
            
            # Player's turn
            action = input("Choose: (S)pin, (B)uy vowel, (G)uess puzzle, or (Q)uit: ").upper()
            
            if action == 'Q':
                print("Thanks for playing!")
                break
            elif action == 'G':
                guess = input("Guess the puzzle: ").upper()
                if guess == puzzle:
                    print(f"🏆 CONGRATULATIONS! You solved: {puzzle}")
                    print(f"Final winnings: ${winnings}")
                    self.commentary.comment("correct")
                    break
                else:
                    print("❌ Wrong guess!")
                    self.commentary.comment("wrong")
                    continue
            elif action == 'B':
                if winnings < 250:
                    print("❌ You need at least $250 to buy a vowel!")
                    continue
                vowel = input("Buy which vowel (A, E, I, O, U): ").upper()
                if vowel in "AEIOU" and vowel not in guessed_letters:
                    winnings -= 250
                    guessed_letters.append(vowel)
                    if vowel in puzzle:
                        # Reveal the vowel
                        new_showing = ""
                        for i, char in enumerate(puzzle):
                            if char == vowel:
                                new_showing += char
                            else:
                                new_showing += showing[i]
                        showing = new_showing
                        print(f"✅ Good choice! '{vowel}' is in the puzzle!")
                        self.commentary.comment("correct")
                    else:
                        print(f"❌ Sorry, '{vowel}' is not in the puzzle.")
                        self.commentary.comment("wrong")
                else:
                    print("❌ Invalid vowel or already guessed!")
            elif action == 'S':
                spin_result = self.spin_wheel()
                if spin_result == -1:  # Bankrupt
                    winnings = 0
                    continue
                elif spin_result == 0:  # Lose turn
                    continue
                else:
                    # Guess a consonant
                    consonant = input("Guess a consonant: ").upper()
                    if consonant in "BCDFGHJKLMNPQRSTVWXYZ" and consonant not in guessed_letters:
                        guessed_letters.append(consonant)
                        count = puzzle.count(consonant)
                        if count > 0:
                            # Reveal the consonant
                            new_showing = ""
                            for i, char in enumerate(puzzle):
                                if char == consonant:
                                    new_showing += char
                                else:
                                    new_showing += showing[i]
                            showing = new_showing
                            earnings = spin_result * count
                            winnings += earnings
                            print(f"✅ Great! '{consonant}' appears {count} time(s)!")
                            print(f"You earned ${earnings}!")
                            self.commentary.comment("correct")
                        else:
                            print(f"❌ Sorry, '{consonant}' is not in the puzzle.")
                            self.commentary.comment("wrong")
                    else:
                        print("❌ Invalid consonant or already guessed!")
            else:
                print("❌ Invalid choice!")
        
        print("\n🎉 Game Over! Thanks for playing!")
        print("=" * 50)

def main():
    """Main function"""
    print("🎡 SIMPLE WHEEL OF FORTUNE WITH COMMENTARY")
    print("This is a simplified version to test the commentary system!")
    print("For the full version with ChatGPT, you'll need the complete files.")
    print()
    
    game = SimpleWheelOfFortune()
    game.play_simple_game()

if __name__ == "__main__":
    main()
