"""
Smart player implementations for Wheel of Fortune
Mock implementations for testing
"""

import random

def computer_turn_smart(showing, winnings, previous_guesses, turn):
    """Smart computer player strategy"""
    # Simple implementation - prioritize common letters
    common_letters = "RSTLNE"  # Wheel of Fortune bonus round letters
    alphabet = "ETAOINSHRDLUCMFWYGPBVKQJXZ"
    
    dollar = 0
    for character in alphabet:
        if character in previous_guesses:
            continue
        if character in "AEIOU":  # Vowel
            if winnings[(turn % 3)] < 250:
                continue
            else:
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Consonant
        dollar = spin_wheel_simple()
        if dollar == 0:
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            print("Computer guessed:", character)
            break
    return character, dollar

def computer_turn_smart_conservative(showing, winnings, previous_guesses, turn):
    """Conservative smart computer player"""
    # More cautious approach - focus on safe, common letters
    safe_letters = "RSTLNE"
    
    dollar = 0
    for character in safe_letters:
        if character in previous_guesses:
            continue
        if character in "AEIOU":
            if winnings[(turn % 3)] < 500:  # More conservative with vowels
                continue
            else:
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Consonant
        dollar = spin_wheel_simple()
        if dollar == 0:
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            print("Computer guessed:", character)
            break
    return character, dollar

def computer_turn_smart_aggressive(showing, winnings, previous_guesses, turn):
    """Aggressive smart computer player"""
    # More aggressive - willing to take risks
    alphabet = "ETAOINSHRDLUCMFWYGPBVKQJXZ"
    
    dollar = 0
    for character in alphabet:
        if character in previous_guesses:
            continue
        if character in "AEIOU":
            if winnings[(turn % 3)] < 250:  # Will buy vowels with minimum money
                continue
            else:
                print("Computer bought:", character)
                winnings[(turn % 3)] = winnings[(turn % 3)] - 250
                break
        # Consonant
        dollar = spin_wheel_simple()
        if dollar == 0:
            print("Computer lost a turn")
            character = "_"
            break
        elif dollar == -1:
            print("Computer went bankrupt")
            winnings[(turn % 3)] = 0
            character = "_"
            break
        else:
            print("Computer guessed:", character)
            break
    return character, dollar

def spin_wheel_simple():
    """Simplified wheel spin for smart players"""
    wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900]
    return random.choice(wheel_values)
