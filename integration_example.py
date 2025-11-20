"""
Example: How to add FREE commentary to your existing game
"""

# Step 1: Import the commentary system
from free_commentary_system import WheelOfFortuneCommentary

def your_existing_game():
    """Example of integrating commentary into your existing game"""
    
    # Step 2: Initialize commentary (choose your style!)
    commentary = WheelOfFortuneCommentary(commentary_style="dramatic")  # or "humorous", "professional", "casual"
    
    # Your existing game variables
    puzzle = "YOUR PUZZLE HERE"
    clue = "YOUR CLUE HERE"
    winnings = [0, 0, 0]  # Player winnings
    current_player = 0
    
    # Step 3: Add commentary at key moments
    
    # Game start
    commentary.game_start_commentary(clue, "Your Category")
    
    # Your existing game loop
    while True:  # Your game condition
        
        # When a player spins the wheel
        spin_result = 750  # Your spin logic here
        commentary.wheel_spin_commentary(spin_result, current_player, winnings)
        
        # When a player guesses a letter
        guess = "R"  # Your guess input here
        correct_count = 2  # Your letter counting logic here
        dollar_value = spin_result
        showing = "_ _ R _ _ _"  # Your puzzle display here
        previous_guesses = ["R"]  # Your guess tracking here
        
        commentary.guess_result_commentary(
            guess, correct_count, dollar_value, 
            showing, clue, previous_guesses, 
            current_player, winnings
        )
        
        # When a player buys a vowel
        vowel = "A"  # Your vowel input here
        commentary.vowel_purchase_commentary(vowel, current_player, winnings)
        
        # When a player tries to solve
        solve_attempt = "YOUR GUESS"  # Your solve input here
        is_correct = True  # Your solve checking logic here
        commentary.solve_attempt_commentary(solve_attempt, is_correct, puzzle, current_player, winnings)
        
        # Break condition for your game
        if is_correct:
            break
    
    print("Game over!")

# Example of changing commentary style during game
def change_style_example():
    commentary = WheelOfFortuneCommentary(commentary_style="dramatic")
    
    # Play with dramatic style
    commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
    
    # Change to humorous
    commentary.set_commentary_style("humorous")
    commentary.wheel_spin_commentary(500, 0, [0, 0, 0])
    
    # Change to professional
    commentary.set_commentary_style("professional")
    commentary.guess_result_commentary("R", 1, 500, "R _ _ _ _ _", "FAMOUS PEOPLE", ["R"], 0, [500, 0, 0])
    
    # Toggle commentary off
    commentary.toggle_commentary()
    commentary.wheel_spin_commentary(300, 0, [500, 0, 0])  # No commentary will show
    
    # Toggle back on
    commentary.toggle_commentary()
    commentary.solve_attempt_commentary("ROBERT DOWNEY JR", True, "ROBERT DOWNEY JR", 0, [500, 0, 0])

if __name__ == "__main__":
    print("🎮 Integration Examples")
    print("1. Basic integration example")
    print("2. Style changing example")
    
    choice = input("Choose 1 or 2: ").strip()
    
    if choice == "2":
        change_style_example()
    else:
        your_existing_game()
