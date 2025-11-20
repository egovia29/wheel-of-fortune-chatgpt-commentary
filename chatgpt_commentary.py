"""
ChatGPT Commentary System for Wheel of Fortune
A wrapper that provides AI-powered commentary for game events
"""

import openai
import time
import random
from typing import List, Dict, Optional
import json
import os

class WheelOfFortuneCommentary:
    """
    ChatGPT-powered commentary system for Wheel of Fortune game
    """
    
    def __init__(self, api_key: Optional[str] = None, commentary_style: str = "dramatic", 
                 enable_commentary: bool = True, delay_range: tuple = (1, 3)):
        """
        Initialize the commentary system
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
            commentary_style: Style of commentary ("dramatic", "humorous", "professional", "casual")
            enable_commentary: Whether commentary is enabled
            delay_range: Range of seconds to wait before commentary (min, max)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.commentary_style = commentary_style
        self.enable_commentary = enable_commentary
        self.delay_range = delay_range
        self.client = None
        
        # Initialize OpenAI client if API key is available
        if self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.enable_commentary = False
        else:
            print("Warning: No OpenAI API key found. Commentary will be disabled.")
            self.enable_commentary = False
            
        # Commentary style prompts
        self.style_prompts = {
            "dramatic": "You are a dramatic game show host like Pat Sajak. Be enthusiastic, use exclamation points, and build suspense.",
            "humorous": "You are a witty, humorous game show commentator. Make clever jokes and puns, but keep it family-friendly.",
            "professional": "You are a professional sports commentator covering Wheel of Fortune. Be informative and analytical.",
            "casual": "You are a friendly, casual observer commenting on the game. Be conversational and encouraging."
        }
        
        # Fallback commentary for when API is unavailable
        self.fallback_commentary = {
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
            "bankrupt": [
                "💸 Oh no! Bankrupt! That's the risk of the wheel!",
                "😱 All those winnings... gone in a spin!",
                "🎭 The wheel giveth, and the wheel taketh away!"
            ],
            "lose_turn": [
                "⏭️ Lose a turn! Sometimes the wheel has other plans!",
                "🔄 Next player's chance! The wheel keeps everyone on their toes!",
                "⏸️ A brief setback, but the game continues!"
            ],
            "correct_guess": [
                "🎉 Excellent guess! The letters are revealed!",
                "✅ Right on target! Great strategy!",
                "🌟 Perfect! The puzzle is coming together!"
            ],
            "wrong_guess": [
                "❌ Not in the puzzle! Better luck next time!",
                "🤔 Close, but not quite! The mystery continues!",
                "🎯 Sometimes the best guesses don't pan out!"
            ],
            "game_end": [
                "🏆 Congratulations to our winner! What a fantastic game!",
                "🎊 Another thrilling game comes to an end!",
                "👏 Well played everyone! Thanks for a great game!"
            ]
        }
    
    def _get_commentary_delay(self) -> float:
        """Get a random delay for natural commentary timing"""
        return random.uniform(self.delay_range[0], self.delay_range[1])
    
    def _get_fallback_commentary(self, event_type: str) -> str:
        """Get fallback commentary when API is unavailable"""
        if event_type in self.fallback_commentary:
            return random.choice(self.fallback_commentary[event_type])
        return "🎡 The game continues!"
    
    def _generate_commentary(self, prompt: str, context: Dict) -> str:
        """
        Generate commentary using ChatGPT API
        
        Args:
            prompt: The specific prompt for this commentary
            context: Game context information
            
        Returns:
            Generated commentary string
        """
        if not self.enable_commentary:
            return ""
        
        if not self.client:
            # Use fallback commentary when no API client available
            return ""
            
        try:
            # Build the full prompt with style and context
            style_instruction = self.style_prompts.get(self.commentary_style, self.style_prompts["dramatic"])
            
            full_prompt = f"""
{style_instruction}

Game Context:
- Current puzzle progress: {context.get('showing', 'Unknown')}
- Clue: {context.get('clue', 'Unknown')}
- Player winnings: {context.get('winnings', [0,0,0])}
- Current player: Player {context.get('current_player', 0)}
- Previous guesses: {context.get('previous_guesses', [])}

{prompt}

Provide a brief, engaging commentary (1-2 sentences max). Keep it appropriate for all ages.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional game show commentator."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            commentary = response.choices[0].message.content.strip()
            return commentary
            
        except Exception as e:
            print(f"Commentary generation failed: {e}")
            return ""
    
    def game_start_commentary(self, puzzle_clue: str, game_type: str) -> None:
        """Commentary for game start"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {"clue": puzzle_clue, "game_type": game_type}
        prompt = f"The game is starting! We have a {game_type} puzzle with the clue: '{puzzle_clue}'. Welcome the players and build excitement for the game ahead."
        
        commentary = self._generate_commentary(prompt, context)
        if not commentary:
            commentary = random.choice(self.fallback_commentary["game_start"])
            
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def wheel_spin_commentary(self, spin_result: int, player_num: int, winnings: List[int]) -> None:
        """Commentary for wheel spins"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {"current_player": player_num, "winnings": winnings}
        
        if spin_result == -1:  # Bankrupt
            prompt = f"Player {player_num} just hit BANKRUPT! They lost all their winnings of ${winnings[player_num]}. React with appropriate drama and sympathy."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["bankrupt"])
        elif spin_result == 0:  # Lose a turn
            prompt = f"Player {player_num} hit 'Lose a Turn'! Comment on this unfortunate spin and encourage them for next time."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["lose_turn"])
        else:  # Regular dollar amount
            prompt = f"Player {player_num} spun ${spin_result}! Comment on this spin result and build anticipation for their letter guess."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["wheel_spin"])
                
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def guess_result_commentary(self, guess: str, correct_count: int, dollar_value: int, 
                              showing: str, clue: str, previous_guesses: List[str], 
                              player_num: int, winnings: List[int]) -> None:
        """Commentary for letter guess results"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {
            "showing": showing,
            "clue": clue,
            "previous_guesses": previous_guesses,
            "current_player": player_num,
            "winnings": winnings
        }
        
        if correct_count > 0:
            earnings = dollar_value * correct_count
            prompt = f"Player {player_num} guessed '{guess}' and found {correct_count} letter(s), earning ${earnings}! The puzzle now shows: '{showing}'. Comment on this successful guess and the puzzle progress."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["correct_guess"])
        else:
            prompt = f"Player {player_num} guessed '{guess}' but it's not in the puzzle. The clue is '{clue}'. Provide encouraging commentary about this miss."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["wrong_guess"])
                
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def vowel_purchase_commentary(self, vowel: str, player_num: int, winnings: List[int]) -> None:
        """Commentary for vowel purchases"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {"current_player": player_num, "winnings": winnings}
        prompt = f"Player {player_num} bought the vowel '{vowel}' for $250. They now have ${winnings[player_num]} remaining. Comment on this strategic move."
        
        commentary = self._generate_commentary(prompt, context)
        if not commentary:
            commentary = f"💰 Smart move buying that '{vowel}'! Strategic vowel purchasing can really pay off!"
            
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def solve_attempt_commentary(self, attempt: str, correct: bool, puzzle: str, 
                                player_num: int, winnings: List[int]) -> None:
        """Commentary for solve attempts"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {"current_player": player_num, "winnings": winnings}
        
        if correct:
            prompt = f"INCREDIBLE! Player {player_num} solved the puzzle '{puzzle}' and won ${winnings[player_num]}! Celebrate this victory with enthusiasm!"
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = random.choice(self.fallback_commentary["game_end"])
        else:
            prompt = f"Player {player_num} guessed '{attempt}' but the correct answer was '{puzzle}'. Provide encouraging commentary about this close attempt."
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = "🤔 So close! Sometimes the final solve is the trickiest part!"
                
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def player_turn_commentary(self, player_num: int, player_type: str, winnings: List[int]) -> None:
        """Commentary for player turn transitions"""
        if not self.enable_commentary:
            return
            
        time.sleep(self._get_commentary_delay())
        
        context = {"current_player": player_num, "winnings": winnings}
        prompt = f"It's Player {player_num}'s turn! They are a {player_type} player with ${winnings[player_num]} in winnings. Build anticipation for their turn."
        
        commentary = self._generate_commentary(prompt, context)
        if not commentary:
            commentary = f"🎯 Player {player_num} is up! Let's see what strategy they'll use!"
            
        print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def puzzle_progress_commentary(self, showing: str, clue: str, previous_guesses: List[str]) -> None:
        """Commentary on puzzle solving progress"""
        if not self.enable_commentary:
            return
            
        # Calculate completion percentage
        total_letters = sum(1 for c in showing if c.isalpha() or c == '_')
        revealed_letters = sum(1 for c in showing if c.isalpha())
        completion_pct = (revealed_letters / total_letters * 100) if total_letters > 0 else 0
        
        if completion_pct > 75:
            time.sleep(self._get_commentary_delay())
            context = {"showing": showing, "clue": clue, "previous_guesses": previous_guesses}
            prompt = f"The puzzle is {completion_pct:.0f}% complete! Current state: '{showing}'. The clue is '{clue}'. Comment on how close we are to solving this puzzle."
            
            commentary = self._generate_commentary(prompt, context)
            if not commentary:
                commentary = f"🔥 We're getting close! The puzzle is really taking shape now!"
                
            print(f"\n🎙️ COMMENTARY: {commentary}\n")
    
    def set_commentary_style(self, style: str) -> None:
        """Change the commentary style"""
        if style in self.style_prompts:
            self.commentary_style = style
            print(f"Commentary style changed to: {style}")
        else:
            print(f"Unknown style: {style}. Available styles: {list(self.style_prompts.keys())}")
    
    def toggle_commentary(self) -> None:
        """Toggle commentary on/off"""
        self.enable_commentary = not self.enable_commentary
        status = "enabled" if self.enable_commentary else "disabled"
        print(f"Commentary {status}")


# Example usage and testing
if __name__ == "__main__":
    # Test the commentary system
    commentary = WheelOfFortuneCommentary(commentary_style="dramatic", enable_commentary=True)
    
    # Test different types of commentary
    print("Testing Commentary System...")
    
    commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
    commentary.player_turn_commentary(0, "human", [0, 0, 0])
    commentary.wheel_spin_commentary(750, 0, [0, 0, 0])
    commentary.guess_result_commentary("R", 2, 750, "_ _ R _ _ _", "FAMOUS PEOPLE", ["R"], 0, [1500, 0, 0])
    commentary.vowel_purchase_commentary("A", 0, [1250, 0, 0])
    commentary.solve_attempt_commentary("BARACK OBAMA", True, "BARACK OBAMA", 0, [1250, 0, 0])
