"""
Manual ChatGPT Commentary System - 100% FREE!
Copy prompts to ChatGPT and paste responses back
"""

import pyperclip  # pip install pyperclip
import time

class ManualChatGPTCommentary:
    def __init__(self, commentary_style="dramatic"):
        self.commentary_style = commentary_style
        print("🎙️ FREE ChatGPT Commentary Mode Activated!")
        print("=" * 50)
        print("📋 I'll give you prompts to copy to ChatGPT")
        print("💬 You paste the responses back")
        print("🆓 Completely FREE to use!")
        print("=" * 50)
        
        # Set up ChatGPT with your style
        self.setup_chatgpt_style()
    
    def setup_chatgpt_style(self):
        """Give user the initial setup prompt for ChatGPT"""
        style_prompts = {
            "dramatic": "You are a dramatic game show host like Pat Sajak. Be enthusiastic, use exclamation points, and build suspense. Keep all responses to 1-2 sentences maximum.",
            "humorous": "You are a witty, humorous game show commentator. Make clever jokes and puns, but keep it family-friendly. Keep all responses to 1-2 sentences maximum.",
            "professional": "You are a professional sports commentator covering Wheel of Fortune. Be informative and analytical. Keep all responses to 1-2 sentences maximum.",
            "casual": "You are a friendly, casual observer commenting on the game. Be conversational and encouraging. Keep all responses to 1-2 sentences maximum."
        }
        
        setup_prompt = f"""
{style_prompts[self.commentary_style]}

I'm going to send you Wheel of Fortune game events, and you should respond with brief commentary in this style. 
Always keep responses to 1-2 sentences maximum.
Just respond with "Ready for commentary!" to confirm you understand.
"""
        
        print("\n🚀 STEP 1: Copy this setup prompt to ChatGPT:")
        print("=" * 60)
        print(setup_prompt)
        print("=" * 60)
        
        # Copy to clipboard
        try:
            pyperclip.copy(setup_prompt)
            print("✅ Setup prompt copied to clipboard!")
        except:
            print("📋 Copy the text above manually")
        
        input("\n⏳ Paste this in ChatGPT, wait for 'Ready for commentary!' response, then press Enter...")
        print("🎮 Great! Now let's play with commentary!\n")
    
    def get_commentary(self, prompt):
        """Get commentary by showing prompt to copy to ChatGPT"""
        print(f"\n📋 COPY THIS TO CHATGPT:")
        print("-" * 40)
        print(prompt)
        print("-" * 40)
        
        # Copy to clipboard automatically
        try:
            pyperclip.copy(prompt)
            print("✅ Copied to clipboard! Paste it in ChatGPT")
        except:
            print("📋 Copy the text above manually")
        
        # Wait for user to get response
        response = input("💬 Paste ChatGPT's response here: ").strip()
        
        if not response:
            response = "🎡 The excitement continues!"
        
        return response
    
    def game_start_commentary(self, puzzle_clue, game_type):
        """Commentary for game start"""
        prompt = f"Game starting! We have a {game_type} puzzle with the clue: '{puzzle_clue}'. Welcome the players and build excitement for the game ahead!"
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)
    
    def wheel_spin_commentary(self, spin_result, player_num, winnings):
        """Commentary for wheel spins"""
        if spin_result == -1:  # Bankrupt
            prompt = f"OH NO! Player {player_num} just hit BANKRUPT! They lost all their winnings of ${winnings[player_num]}. React with drama and sympathy!"
        elif spin_result == 0:  # Lose a turn
            prompt = f"Player {player_num} hit 'Lose a Turn'! Comment on this unfortunate spin and encourage them for next time."
        else:  # Regular dollar amount
            prompt = f"Player {player_num} spun ${spin_result}! Comment on this spin result and build anticipation for their letter guess."
        
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)
    
    def guess_result_commentary(self, guess, correct_count, dollar_value, showing, clue, previous_guesses, player_num, winnings):
        """Commentary for letter guess results"""
        if correct_count > 0:
            earnings = dollar_value * correct_count
            prompt = f"GREAT GUESS! Player {player_num} guessed '{guess}' and found {correct_count} letter(s), earning ${earnings}! The puzzle now shows: '{showing}'. Comment on this success!"
        else:
            prompt = f"Player {player_num} guessed '{guess}' but it's not in the puzzle. The clue is '{clue}'. Provide encouraging commentary about this miss."
        
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)
    
    def vowel_purchase_commentary(self, vowel, player_num, winnings):
        """Commentary for vowel purchases"""
        prompt = f"Player {player_num} bought the vowel '{vowel}' for $250. They now have ${winnings[player_num]} remaining. Comment on this strategic move."
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)
    
    def solve_attempt_commentary(self, attempt, correct, puzzle, player_num, winnings):
        """Commentary for solve attempts"""
        if correct:
            prompt = f"INCREDIBLE! Player {player_num} solved the puzzle '{puzzle}' and won ${winnings[player_num]}! Celebrate this victory with maximum enthusiasm!"
        else:
            prompt = f"Player {player_num} guessed '{attempt}' but the correct answer was '{puzzle}'. Provide encouraging commentary about this close attempt."
        
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)
    
    def player_turn_commentary(self, player_num, player_type, winnings):
        """Commentary for player turn transitions"""
        prompt = f"It's Player {player_num}'s turn! They are a {player_type} player with ${winnings[player_num]} in winnings. Build anticipation for their turn."
        response = self.get_commentary(prompt)
        print(f"\n🎙️ COMMENTARY: {response}\n")
        time.sleep(1)

# Example usage and testing
if __name__ == "__main__":
    print("🎡 TESTING FREE CHATGPT COMMENTARY SYSTEM")
    print("=" * 50)
    
    # Initialize commentary system
    commentary = ManualChatGPTCommentary(commentary_style="dramatic")
    
    # Test different types of commentary
    print("\n🎮 Testing commentary...")
    
    commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
    commentary.player_turn_commentary(0, "human", [0, 0, 0])
    commentary.wheel_spin_commentary(750, 0, [0, 0, 0])
    commentary.guess_result_commentary("R", 2, 750, "_ _ R _ _ _", "FAMOUS PEOPLE", ["R"], 0, [1500, 0, 0])
    commentary.vowel_purchase_commentary("A", 0, [1250, 0, 0])
    commentary.solve_attempt_commentary("BARACK OBAMA", True, "BARACK OBAMA", 0, [1250, 0, 0])
    
    print("\n🎉 Testing complete! Your free ChatGPT commentary system is ready!")
