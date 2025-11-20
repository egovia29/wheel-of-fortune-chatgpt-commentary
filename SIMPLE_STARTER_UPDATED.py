"""
SIMPLE STARTER - Wheel of Fortune with FREE Commentary
Works immediately - no setup required!
Perfect for testing the FREE commentary system!
"""

from free_commentary_system import WheelOfFortuneCommentary
import random
import time

def simple_wheel_of_fortune():
    """
    Simple Wheel of Fortune game with FREE commentary
    Perfect for testing and demonstration
    """
    
    print("🎡 SIMPLE WHEEL OF FORTUNE WITH FREE COMMENTARY!")
    print("=" * 60)
    print("🆓 100% FREE - No API keys needed!")
    print("🎙️ Smart commentary that feels like real AI!")
    print("=" * 60)
    
    # Choose commentary style
    print("\n🎭 Choose your commentary style:")
    print("1. Dramatic (Exciting game show host)")
    print("2. Humorous (Witty jokes and puns)")
    print("3. Professional (Sports commentator)")
    print("4. Casual (Friendly conversation)")
    
    style_choice = input("Enter 1-4 (or press Enter for Dramatic): ").strip()
    
    styles = {
        "1": "dramatic",
        "2": "humorous", 
        "3": "professional",
        "4": "casual"
    }
    
    commentary_style = styles.get(style_choice, "dramatic")
    
    # Initialize commentary system
    commentary = WheelOfFortuneCommentary(
        commentary_style=commentary_style,
        enable_commentary=True,
        delay_range=(1, 2)
    )
    
    # Game setup
    puzzles = [
        ("WHEEL OF FORTUNE", "TV SHOW"),
        ("BARACK OBAMA", "FAMOUS PEOPLE"),
        ("NEW YORK CITY", "PLACE"),
        ("PIZZA AND SODA", "FOOD AND DRINK"),
        ("HAPPY BIRTHDAY", "PHRASE"),
        ("GOLDEN GATE BRIDGE", "LANDMARK")
    ]
    
    puzzle, clue = random.choice(puzzles)
    showing = ''.join('_' if c.isalpha() else c for c in puzzle)
    guessed_letters = []
    winnings = [0, 0, 0]
    current_player = 0
    
    print(f"\n🎮 Starting game with {commentary_style.upper()} commentary!")
    
    # Game start commentary
    commentary.game_start_commentary(clue, clue.title())
    
    # Display initial state
    print(f"\nPuzzle: {showing}")
    print(f"Clue: {clue}")
    print(f"Your winnings: ${winnings[current_player]}")
    
    # Game loop
    while '_' in showing:
        print("\n" + "-" * 40)
        action = input("Choose: (s)pin wheel, (b)uy vowel, s(o)lve puzzle: ").lower().strip()
        
        if action in ['s', 'spin']:
            # Spin wheel
            wheel_values = [500, 600, 700, 800, 900, 1000, -1, 0]  # -1=bankrupt, 0=lose turn
            spin_result = random.choice(wheel_values)
            
            print(f"\n🎡 You spun: ", end="")
            if spin_result == -1:
                print("BANKRUPT! 💸")
                winnings[current_player] = 0
                commentary.wheel_spin_commentary(spin_result, current_player, winnings)
                continue
            elif spin_result == 0:
                print("Lose a Turn! ⏭️")
                commentary.wheel_spin_commentary(spin_result, current_player, winnings)
                continue
            else:
                print(f"${spin_result}! 💰")
                commentary.wheel_spin_commentary(spin_result, current_player, winnings)
            
            # Get letter guess
            while True:
                letter = input("Guess a consonant: ").upper().strip()
                if len(letter) == 1 and letter.isalpha() and letter not in 'AEIOU':
                    if letter not in guessed_letters:
                        break
                    else:
                        print("Already guessed that letter!")
                else:
                    print("Please enter a single consonant (not A, E, I, O, U)")
            
            guessed_letters.append(letter)
            count = puzzle.count(letter)
            
            if count > 0:
                # Update showing
                new_showing = ""
                for c in puzzle:
                    if c.upper() == letter:
                        new_showing += c
                    elif c in showing:
                        new_showing += c
                    else:
                        new_showing += c if not c.isalpha() else '_'
                
                showing = new_showing
                earnings = spin_result * count
                winnings[current_player] += earnings
                
                print(f"✅ Found {count} {letter}'s! Earned ${earnings}!")
                
                # Commentary for correct guess
                commentary.guess_result_commentary(
                    letter, count, spin_result, showing, clue, 
                    guessed_letters, current_player, winnings
                )
            else:
                print(f"❌ No {letter}'s in the puzzle.")
                
                # Commentary for wrong guess
                commentary.guess_result_commentary(
                    letter, 0, spin_result, showing, clue, 
                    guessed_letters, current_player, winnings
                )
        
        elif action in ['b', 'buy']:
            # Buy vowel
            if winnings[current_player] < 250:
                print("❌ Not enough money! Need $250 to buy a vowel.")
                continue
            
            while True:
                vowel = input("Buy which vowel (A, E, I, O, U): ").upper().strip()
                if vowel in 'AEIOU' and len(vowel) == 1:
                    if vowel not in guessed_letters:
                        break
                    else:
                        print("Already guessed that vowel!")
                else:
                    print("Please enter a single vowel (A, E, I, O, U)")
            
            winnings[current_player] -= 250
            guessed_letters.append(vowel)
            count = puzzle.count(vowel)
            
            # Commentary for vowel purchase
            commentary.vowel_purchase_commentary(vowel, current_player, winnings)
            
            if count > 0:
                # Update showing
                new_showing = ""
                for c in puzzle:
                    if c.upper() == vowel:
                        new_showing += c
                    elif c in showing:
                        new_showing += c
                    else:
                        new_showing += c if not c.isalpha() else '_'
                
                showing = new_showing
                print(f"✅ Found {count} {vowel}'s!")
            else:
                print(f"❌ No {vowel}'s in the puzzle.")
        
        elif action in ['o', 'solve']:
            # Solve puzzle
            attempt = input("Enter your solution: ").strip()
            
            if attempt.upper() == puzzle.upper():
                print(f"🏆 CORRECT! You solved: {puzzle}")
                print(f"🎊 You won ${winnings[current_player]}!")
                
                # Commentary for correct solve
                commentary.solve_attempt_commentary(
                    attempt, True, puzzle, current_player, winnings
                )
                break
            else:
                print(f"❌ Incorrect! The answer was: {puzzle}")
                
                # Commentary for wrong solve
                commentary.solve_attempt_commentary(
                    attempt, False, puzzle, current_player, winnings
                )
                break
        
        else:
            print("Invalid choice. Use 's' for spin, 'b' for buy vowel, 'o' for solve.")
            continue
        
        # Display current state
        print(f"\nPuzzle: {showing}")
        print(f"Clue: {clue}")
        print(f"Guessed: {', '.join(guessed_letters)}")
        print(f"Your winnings: ${winnings[current_player]}")
        
        # Check if solved
        if '_' not in showing:
            print(f"\n🎉 PUZZLE SOLVED! The answer was: {puzzle}")
            print(f"🏆 Final winnings: ${winnings[current_player]}")
            
            # Final commentary
            commentary.solve_attempt_commentary(
                puzzle, True, puzzle, current_player, winnings
            )
            break
    
    print("\n🎊 Thanks for playing!")
    print("🎯 Want to play again? Just run this script again!")

def demo_commentary_styles():
    """Demo all commentary styles"""
    print("🎭 COMMENTARY STYLES DEMO")
    print("=" * 40)
    
    styles = ["dramatic", "humorous", "professional", "casual"]
    
    for style in styles:
        print(f"\n🎨 {style.upper()} Style:")
        commentary = WheelOfFortuneCommentary(commentary_style=style, delay_range=(0.5, 1))
        commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
        commentary.wheel_spin_commentary(850, 0, [0, 0, 0])
        print("-" * 30)

def main():
    """Main function"""
    print("🎡 SIMPLE WHEEL OF FORTUNE STARTER")
    print("=" * 50)
    print("Choose an option:")
    print("1. Play game with commentary")
    print("2. Demo all commentary styles")
    print("3. Test commentary system only")
    
    choice = input("Enter 1, 2, or 3 (or press Enter for game): ").strip()
    
    if choice == "2":
        demo_commentary_styles()
    elif choice == "3":
        print("\n🎙️ Testing commentary system...")
        commentary = WheelOfFortuneCommentary(commentary_style="dramatic")
        
        print("\n🎮 Sample commentary events:")
        commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
        commentary.wheel_spin_commentary(750, 0, [0, 0, 0])
        commentary.guess_result_commentary("R", 2, 750, "_ _ R _ _ _", "FAMOUS PEOPLE", ["R"], 0, [1500, 0, 0])
        commentary.solve_attempt_commentary("BARACK OBAMA", True, "BARACK OBAMA", 0, [1500, 0, 0])
        
        print("\n✅ Commentary system test complete!")
    else:
        simple_wheel_of_fortune()

if __name__ == "__main__":
    main()
