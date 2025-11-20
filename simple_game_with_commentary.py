"""
Simple Wheel of Fortune with FREE Commentary
Perfect for testing the commentary system!
"""

from free_commentary_system import WheelOfFortuneCommentary
import random
import time

def simple_wheel_of_fortune_demo():
    """Demo game showing off the commentary system"""
    
    print("🎡 WHEEL OF FORTUNE WITH FREE COMMENTARY!")
    print("=" * 50)
    
    # Initialize commentary system
    commentary = WheelOfFortuneCommentary(commentary_style="dramatic")
    
    # Game setup
    puzzle = "WHEEL OF FORTUNE"
    clue = "TV SHOW"
    showing = "_ _ _ _ _   _ _   _ _ _ _ _ _ _"
    winnings = [0, 0, 0]
    current_player = 0
    
    # Game start commentary
    commentary.game_start_commentary(clue, "TV Show")
    
    print(f"Puzzle: {showing}")
    print(f"Clue: {clue}")
    print(f"Player winnings: {winnings}")
    
    # Simulate some game events
    events = [
        ("spin", 750),
        ("guess", "R", 3),
        ("spin", 500), 
        ("guess", "T", 2),
        ("vowel", "E"),
        ("solve", "WHEEL OF FORTUNE", True)
    ]
    
    for event_type, *args in events:
        input(f"\nPress Enter for next event: {event_type.upper()}...")
        
        if event_type == "spin":
            spin_value = args[0]
            print(f"\n🎡 Player {current_player} spins... ${spin_value}!")
            commentary.wheel_spin_commentary(spin_value, current_player, winnings)
            
        elif event_type == "guess":
            letter, count = args
            earnings = 750 * count if count > 0 else 0
            winnings[current_player] += earnings
            
            print(f"\n🎯 Player {current_player} guesses '{letter}'!")
            if count > 0:
                print(f"✅ Found {count} {letter}'s! Earned ${earnings}!")
                showing = showing.replace("_", letter, count)
            else:
                print(f"❌ No {letter}'s in the puzzle!")
            
            commentary.guess_result_commentary(letter, count, 750, showing, clue, [letter], current_player, winnings)
            print(f"Puzzle now: {showing}")
            
        elif event_type == "vowel":
            vowel = args[0]
            winnings[current_player] -= 250
            print(f"\n💰 Player {current_player} buys vowel '{vowel}' for $250!")
            commentary.vowel_purchase_commentary(vowel, current_player, winnings)
            
        elif event_type == "solve":
            attempt, correct = args
            print(f"\n🎯 Player {current_player} attempts to solve: '{attempt}'!")
            if correct:
                print(f"🏆 CORRECT! Player {current_player} wins ${winnings[current_player]}!")
            commentary.solve_attempt_commentary(attempt, correct, puzzle, current_player, winnings)
    
    print(f"\n🎊 Final winnings: {winnings}")
    print("🎉 Thanks for playing!")

def test_different_styles():
    """Test different commentary styles"""
    print("\n🎭 TESTING DIFFERENT COMMENTARY STYLES")
    print("=" * 50)
    
    styles = ["dramatic", "humorous", "professional", "casual"]
    
    for style in styles:
        print(f"\n🎨 Testing {style.upper()} style:")
        commentary = WheelOfFortuneCommentary(commentary_style=style, delay_range=(0.5, 1))
        commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
        commentary.wheel_spin_commentary(850, 0, [0, 0, 0])

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Play demo game with commentary")
    print("2. Test different commentary styles")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        simple_wheel_of_fortune_demo()
    elif choice == "2":
        test_different_styles()
    else:
        print("🎡 Running demo game...")
        simple_wheel_of_fortune_demo()
