"""
Enhanced Wheel of Fortune with FREE Smart Commentary System
No API keys needed - works immediately!
"""

import sys
import random
import time
from free_commentary_system import WheelOfFortuneCommentary

# Import existing game components (assuming they exist)
try:
    from wheel_of_fortune import WheelOfFortune
    from smart_player import SmartPlayer, ConservativePlayer, AggressivePlayer
    from ascii_wheel import display_wheel
except ImportError:
    print("⚠️  Some game components not found. Using simplified versions.")
    
    # Simplified versions if imports fail
    class WheelOfFortune:
        def __init__(self):
            self.puzzles = [
                ("WHEEL OF FORTUNE", "TV SHOW"),
                ("FAMOUS PEOPLE", "BARACK OBAMA"),
                ("PLACE", "NEW YORK CITY"),
                ("FOOD AND DRINK", "PIZZA AND SODA")
            ]
            self.current_puzzle = None
            self.current_clue = None
            self.showing = ""
            self.guessed_letters = []
            self.winnings = [0, 0, 0]
            self.current_player = 0
            
        def new_game(self):
            puzzle, clue = random.choice(self.puzzles)
            self.current_puzzle = puzzle
            self.current_clue = clue
            self.showing = ''.join('_' if c.isalpha() else c for c in puzzle)
            self.guessed_letters = []
            self.winnings = [0, 0, 0]
            self.current_player = 0
            
        def spin_wheel(self):
            values = [500, 600, 700, 800, 900, 1000, -1, 0]  # -1=bankrupt, 0=lose turn
            return random.choice(values)
            
        def guess_letter(self, letter, spin_value):
            if letter in self.guessed_letters:
                return 0, "Already guessed"
                
            self.guessed_letters.append(letter)
            count = self.current_puzzle.count(letter.upper())
            
            if count > 0:
                # Update showing
                new_showing = ""
                for i, c in enumerate(self.current_puzzle):
                    if c.upper() == letter.upper():
                        new_showing += c
                    else:
                        new_showing += self.showing[i]
                self.showing = new_showing
                
                # Add winnings
                if spin_value > 0:
                    self.winnings[self.current_player] += spin_value * count
                    
            return count, "Success"
            
        def buy_vowel(self, vowel):
            if self.winnings[self.current_player] < 250:
                return False, "Not enough money"
                
            self.winnings[self.current_player] -= 250
            count = self.guess_letter(vowel, 0)[0]
            return True, f"Found {count} {vowel}'s"
            
        def solve_puzzle(self, attempt):
            return attempt.upper() == self.current_puzzle.upper()
            
        def is_solved(self):
            return '_' not in self.showing
    
    class SmartPlayer:
        def __init__(self, name="Smart"):
            self.name = name
            
        def make_move(self, game_state):
            return "spin"
            
        def choose_letter(self, game_state):
            common_letters = "RSTLNE"
            for letter in common_letters:
                if letter not in game_state.get('guessed_letters', []):
                    return letter
            return "A"
    
    class ConservativePlayer(SmartPlayer):
        def __init__(self):
            super().__init__("Conservative")
    
    class AggressivePlayer(SmartPlayer):
        def __init__(self):
            super().__init__("Aggressive")
    
    def display_wheel(spin_value):
        print(f"🎡 Wheel Result: ${spin_value}")

class EnhancedWheelOfFortune:
    """Enhanced Wheel of Fortune with FREE Commentary"""
    
    def __init__(self, commentary_style="dramatic", enable_commentary=True):
        self.game = WheelOfFortune()
        self.commentary = WheelOfFortuneCommentary(
            commentary_style=commentary_style,
            enable_commentary=enable_commentary,
            delay_range=(0.5, 2)  # Shorter delays for better gameplay
        )
        self.players = []
        
    def setup_players(self, player_types):
        """Setup players based on types"""
        player_classes = {
            'human': None,  # Human player
            'smart': SmartPlayer,
            'conservative': ConservativePlayer,
            'aggressive': AggressivePlayer
        }
        
        self.players = []
        for i, player_type in enumerate(player_types):
            if player_type == 'human':
                self.players.append(('human', f"Player {i+1}"))
            else:
                player_class = player_classes.get(player_type, SmartPlayer)
                self.players.append((player_class(), f"Player {i+1}"))
    
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*50)
        print(f"Puzzle: {self.game.showing}")
        print(f"Clue: {self.game.current_clue}")
        print(f"Guessed letters: {', '.join(self.game.guessed_letters)}")
        print(f"Winnings: {self.game.winnings}")
        print(f"Current player: {self.game.current_player + 1}")
        print("="*50)
    
    def human_turn(self):
        """Handle human player turn"""
        print(f"\n🎮 Your turn! Current winnings: ${self.game.winnings[self.game.current_player]}")
        
        while True:
            action = input("Choose action: (s)pin, (b)uy vowel, s(o)lve: ").lower().strip()
            
            if action in ['s', 'spin']:
                return self.handle_spin()
            elif action in ['b', 'buy']:
                return self.handle_buy_vowel()
            elif action in ['o', 'solve']:
                return self.handle_solve()
            else:
                print("Invalid choice. Use 's' for spin, 'b' for buy vowel, 'o' for solve.")
    
    def handle_spin(self):
        """Handle wheel spin"""
        spin_result = self.game.spin_wheel()
        
        print(f"\n🎡 You spun: ", end="")
        if spin_result == -1:
            print("BANKRUPT! 💸")
        elif spin_result == 0:
            print("Lose a Turn! ⏭️")
        else:
            print(f"${spin_result}! 💰")
        
        # Commentary for spin
        self.commentary.wheel_spin_commentary(spin_result, self.game.current_player, self.game.winnings)
        
        if spin_result == -1:  # Bankrupt
            self.game.winnings[self.game.current_player] = 0
            return False  # End turn
        elif spin_result == 0:  # Lose turn
            return False  # End turn
        else:
            # Get letter guess
            while True:
                letter = input("Guess a consonant: ").upper().strip()
                if len(letter) == 1 and letter.isalpha() and letter not in 'AEIOU':
                    break
                print("Please enter a single consonant (not A, E, I, O, U)")
            
            count, message = self.game.guess_letter(letter, spin_result)
            
            # Commentary for guess
            self.commentary.guess_result_commentary(
                letter, count, spin_result, self.game.showing, 
                self.game.current_clue, self.game.guessed_letters, 
                self.game.current_player, self.game.winnings
            )
            
            if count > 0:
                print(f"✅ Found {count} {letter}'s! Earned ${spin_result * count}!")
                return True  # Continue turn
            else:
                print(f"❌ No {letter}'s in the puzzle.")
                return False  # End turn
    
    def handle_buy_vowel(self):
        """Handle vowel purchase"""
        if self.game.winnings[self.game.current_player] < 250:
            print("❌ Not enough money to buy a vowel! Need $250.")
            return True  # Continue turn
        
        while True:
            vowel = input("Buy which vowel (A, E, I, O, U): ").upper().strip()
            if vowel in 'AEIOU' and len(vowel) == 1:
                break
            print("Please enter a single vowel (A, E, I, O, U)")
        
        success, message = self.game.buy_vowel(vowel)
        
        if success:
            # Commentary for vowel purchase
            self.commentary.vowel_purchase_commentary(vowel, self.game.current_player, self.game.winnings)
            print(f"💰 Bought '{vowel}' for $250. {message}")
            return True  # Continue turn
        else:
            print(f"❌ {message}")
            return True  # Continue turn
    
    def handle_solve(self):
        """Handle puzzle solve attempt"""
        attempt = input("Enter your solution: ").strip()
        
        if self.game.solve_puzzle(attempt):
            print(f"🏆 CORRECT! You solved: {self.game.current_puzzle}")
            
            # Commentary for correct solve
            self.commentary.solve_attempt_commentary(
                attempt, True, self.game.current_puzzle, 
                self.game.current_player, self.game.winnings
            )
            
            return "solved"
        else:
            print(f"❌ Incorrect! The answer was: {self.game.current_puzzle}")
            
            # Commentary for wrong solve
            self.commentary.solve_attempt_commentary(
                attempt, False, self.game.current_puzzle, 
                self.game.current_player, self.game.winnings
            )
            
            return False  # End turn
    
    def ai_turn(self, player):
        """Handle AI player turn"""
        print(f"\n🤖 {player.name}'s turn...")
        time.sleep(1)
        
        # Simple AI logic - just spin and guess common letters
        spin_result = self.game.spin_wheel()
        
        print(f"🎡 {player.name} spun: ", end="")
        if spin_result == -1:
            print("BANKRUPT! 💸")
        elif spin_result == 0:
            print("Lose a Turn! ⏭️")
        else:
            print(f"${spin_result}! 💰")
        
        # Commentary for AI spin
        self.commentary.wheel_spin_commentary(spin_result, self.game.current_player, self.game.winnings)
        
        if spin_result <= 0:
            return False  # End turn
        
        # AI chooses letter
        letter = player.choose_letter({'guessed_letters': self.game.guessed_letters})
        print(f"🤖 {player.name} guesses: {letter}")
        
        count, message = self.game.guess_letter(letter, spin_result)
        
        # Commentary for AI guess
        self.commentary.guess_result_commentary(
            letter, count, spin_result, self.game.showing, 
            self.game.current_clue, self.game.guessed_letters, 
            self.game.current_player, self.game.winnings
        )
        
        if count > 0:
            print(f"✅ Found {count} {letter}'s! Earned ${spin_result * count}!")
            
            # AI might try to solve if puzzle is mostly complete
            if self.game.showing.count('_') <= 3:
                print(f"🤖 {player.name} attempts to solve...")
                time.sleep(1)
                if self.game.solve_puzzle(self.game.current_puzzle):
                    print(f"🏆 {player.name} solved: {self.game.current_puzzle}")
                    self.commentary.solve_attempt_commentary(
                        self.game.current_puzzle, True, self.game.current_puzzle, 
                        self.game.current_player, self.game.winnings
                    )
                    return "solved"
            
            return True  # Continue turn
        else:
            print(f"❌ No {letter}'s in the puzzle.")
            return False  # End turn
    
    def play_game(self):
        """Main game loop"""
        print("🎡 WHEEL OF FORTUNE WITH FREE COMMENTARY!")
        print("=" * 50)
        
        # Start new game
        self.game.new_game()
        
        # Game start commentary
        self.commentary.game_start_commentary(self.game.current_clue, "Puzzle Category")
        
        # Main game loop
        while not self.game.is_solved():
            self.display_game_state()
            
            # Current player's turn
            current_player_info = self.players[self.game.current_player]
            
            if current_player_info[0] == 'human':
                # Human turn
                result = self.human_turn()
            else:
                # AI turn
                result = self.ai_turn(current_player_info[0])
            
            # Check if game was solved
            if result == "solved":
                break
            
            # Check if puzzle is complete
            if self.game.is_solved():
                break
            
            # Move to next player if turn ended
            if not result:
                self.game.current_player = (self.game.current_player + 1) % len(self.players)
        
        # Game end
        self.display_game_state()
        winner = self.game.current_player
        print(f"\n🏆 Game Over! Player {winner + 1} wins with ${self.game.winnings[winner]}!")
        print(f"🎊 The puzzle was: {self.game.current_puzzle}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python wheel_of_fortune_with_free_commentary.py <player1> [player2] [player3] [options]")
        print("Player types: human, smart, conservative, aggressive")
        print("Options: --style [dramatic|humorous|professional|casual], --no-commentary")
        print("\nExample: python wheel_of_fortune_with_free_commentary.py human smart conservative --style humorous")
        return
    
    # Parse arguments
    args = sys.argv[1:]
    player_types = []
    commentary_style = "dramatic"
    enable_commentary = True
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--style" and i + 1 < len(args):
            commentary_style = args[i + 1]
            i += 2
        elif arg == "--no-commentary":
            enable_commentary = False
            i += 1
        elif arg in ['human', 'smart', 'conservative', 'aggressive']:
            player_types.append(arg)
            i += 1
        else:
            i += 1
    
    # Default to 3 players if not enough specified
    while len(player_types) < 3:
        player_types.append('smart')
    
    # Limit to 3 players
    player_types = player_types[:3]
    
    print(f"🎮 Players: {', '.join(player_types)}")
    print(f"🎭 Commentary style: {commentary_style}")
    print(f"🎙️ Commentary: {'Enabled' if enable_commentary else 'Disabled'}")
    
    # Create and start game
    game = EnhancedWheelOfFortune(commentary_style=commentary_style, enable_commentary=enable_commentary)
    game.setup_players(player_types)
    game.play_game()

if __name__ == "__main__":
    main()import random
import re
import sys
import time
import ascii_wheel
from smart_player import computer_turn_smart, computer_turn_smart_conservative, computer_turn_smart_aggressive
from chatgpt_commentary import WheelOfFortuneCommentary

# Global commentary system instance
commentary_system = None

def computer_turn(showing, winnings, previous_guesses, turn):
  # Guess in the order of the alphabet
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        if commentary_system:
          commentary_system.vowel_purchase_commentary(character, turn % 3, winnings)
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_morse(showing, winnings, previous_guesses, turn):
  # Guess in the order that Samuel Morse identified for his code
  alphabet = "ETAINOSHRDLUCMFWYGPBVKQJXZ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        if commentary_system:
          commentary_system.vowel_purchase_commentary(character, turn % 3, winnings)
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_oxford(showing, winnings, previous_guesses, turn):
  # From dictionary ... that's game optimized word not occurance of words
  # Concise Oxford Dictionary (9th edition, 1995) 
  # https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html

  alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
  dollar = 0
  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        if commentary_system:
          commentary_system.vowel_purchase_commentary(character, turn % 3, winnings)
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn):

  allow_vowels = False
  if winnings[(turn % 3)] >= 250:
    allow_vowels = True

  candidate_trigrams = [] 
  showing_words = showing.split(' ')
  for word in showing_words:
    index = 0
    while index < (len(word) - 2):
      trigram = word[index:index+3]
      #print(trigram)
      if trigram[2] == "_" and "_" != trigram[0] and "_" != trigram[1]:
        candidate_trigrams.append(trigram)
      index = index + 1

  candidate_bigrams = [] 
  for word in showing_words:
    index = 0
    while index < (len(word) - 1):
      bigram = word[index:index+2]
      #print(bigram)
      if "_" != bigram[0] and bigram[1] == "_":
        candidate_bigrams.append(bigram)
      index = index + 1

  #print(candidate_trigrams)
  #print(candidate_bigrams)

  dollar = 0
  guess = "_"

  # Frewquencies from: http://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/#:~:text=Most%20common%20bigrams%20(in%20order,%2C%20sa%2C%20em%2C%20ro.

  #Most common trigrams (in order)
  trigrams = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR", "NDE", "HAS", "NCE", "EDT", "TIS", "OFT", "STH", "MEN"]
  for trigram in trigrams:
    to_match = trigram[0:2] + "_"
    #print("TOMatch", to_match)
    if to_match in candidate_trigrams:
      candidate = trigram[2]
      #print("CANDIDATE", candidate)
      if is_vowel(candidate) and allow_vowels == False:
        #print("can't vowel")
        continue
      elif candidate in previous_guesses:
        #print("already guessed")
        continue
      else:
        guess = candidate
        #print("Actual CANDIDATE", candidate)
        break
  if guess != "_":
    if is_vowel(guess):
      print("Computer bought:", guess)
      winnings[(turn % 3)] = winnings[(turn % 3)] - 250
      if commentary_system:
        commentary_system.vowel_purchase_commentary(guess, turn % 3, winnings)
      return guess, dollar # Should be a vowel and 0 since we've already subtraced
    else:
      dollar = spin_wheel()
      if dollar == 0:
        print("Computer lost a turn")
        guess = "_"
      elif dollar == -1:
        print("Computer went backrupt")
        winnings[(turn % 3)] = 0
        guess = "_"
      else:
        print("Computer guessed:", guess)
      return guess, dollar

  #print("No trigrams ... backing off to bigrams")

  #Most common bigrams (in order)
  #frequent bigrams from a file ... http://practicalcryptography.com/media/cryptanalysis/files/english_bigrams_1.txt Only want first 128
  #bigrams = ["TH", "HE", "IN", "EN", "NT", "RE", "ER", "AN", "TI", "ES", "ON", "AT", "SE", "ND", "OR", "AR", "AL", "TE", "CO", "DE", "TO", "RA", "ET", "ED", "IT", "SA", "EM", "RO"]
  bigrams = []
  try:
    with open("bigrams.txt") as g:
      for line in g:
        line = line.rstrip('\n')
        bigram = line.split(' ')[0].upper()
        bigrams.append(bigram)
        if len(bigrams) == 128:
          break # Arbitrary threshold to use
  except FileNotFoundError:
    # Fallback bigrams if file not found
    bigrams = ["TH", "HE", "IN", "EN", "NT", "RE", "ER", "AN", "TI", "ES", "ON", "AT", "SE", "ND", "OR", "AR", "AL", "TE", "CO", "DE", "TO", "RA", "ET", "ED", "IT", "SA", "EM", "RO"]
  
  #print(bigrams)
  for bigram in bigrams:
    to_match = bigram[0] + "_"
    #print(to_match)
    if to_match in candidate_bigrams:
      candidate = bigram[1]
      #print("CANDIDATE", candidate)
      if is_vowel(candidate) and allow_vowels == False:
        #print("can't vowel")
        continue
      elif candidate in previous_guesses:
        #print("already guessed")
        continue
      else:
        guess = candidate
        #print("Actual CANDIDATE", candidate)
        break
  if guess != "_":
    if is_vowel(guess):
      print("Computer bought:", guess)
      winnings[(turn % 3)] = winnings[(turn % 3)] - 250
      if commentary_system:
        commentary_system.vowel_purchase_commentary(guess, turn % 3, winnings)
      return guess, dollar # Should be a vowel and 0 since we've already subtraced
    else:
      dollar = spin_wheel()
      if dollar == 0:
        print("Computer lost a turn")
        guess = "_"
      elif dollar == -1:
        print("Computer went backrupt")
        winnings[(turn % 3)] = 0
        guess = "_"
      else:
        print("Computer guessed:", guess)
      return guess, dollar

  #print("No bigrams ... backing off to unigrams")

  # Unigrams are from the oxford strategy above
  alphabet = "EARIOTNSLCUDPMHGBFYWKVXZJQ"


  for character in alphabet:
    if character in previous_guesses:
      continue
    if is_vowel(character):
      if winnings[(turn % 3)] < 250:
        continue
      else:
        print("Computer bought:", character)
        winnings[(turn % 3)] = winnings[(turn % 3)] - 250
        if commentary_system:
          commentary_system.vowel_purchase_commentary(character, turn % 3, winnings)
        break
    # Want to choose a consonant ... so spins wheel
    dollar = spin_wheel()
    if dollar == 0:
      print("Computer lost a turn")
      character = "_"
      break
    elif dollar == -1:
      print("Computer went backrupt")
      winnings[(turn % 3)] = 0
      character = "_"
      break
    else:
      print("Computer guessed:", character)
      break
  return character, dollar

def get_random_puzzle():
  random_int = random.randint(0,900) # Roughly size of num puzzles in valid
  number = 0
  try:
    with open("../../data/puzzles/valid.csv") as f:
      for line in f:
        line = line.rstrip('\n')
        puzzle, clue, date, game_type = line.split(',')
        if number == random_int:
          #print(line)
          clue = clue.replace("&amp;", "&") # HTML Code
          puzzle = puzzle.replace("&amp;", "&") # HTML Code
          return(puzzle, clue, date, game_type)
        number = number + 1
  except FileNotFoundError:
    # Fallback puzzles if file not found
    fallback_puzzles = [
      ("WHEEL OF FORTUNE", "TV SHOW", "2024-01-01", "SHOW BIZ"),
      ("ARTIFICIAL INTELLIGENCE", "TECHNOLOGY", "2024-01-01", "TECH"),
      ("PYTHON PROGRAMMING", "COMPUTER SCIENCE", "2024-01-01", "TECH"),
      ("CHATGPT COMMENTARY", "AI FEATURE", "2024-01-01", "TECH"),
      ("GAME SHOW HOST", "ENTERTAINMENT", "2024-01-01", "SHOW BIZ")
    ]
    return random.choice(fallback_puzzles)

def human_turn(showing, winnings, previous_guesses, turn, puzzle):

  # Make sure human chooses a valid action
  deciding = False
  while not deciding:
    decision = input("1: Spin, 2: Buy Vowel, 3: Solve ....  ")
    if decision == "1" or decision == "2" or decision == "3":
      deciding = True
      if decision == "2" and winnings[(turn % 3)] < 250: # Minimum cost of a vowel
        print("Sorry .... you don't have enough money. Select 1 or 3")
        deciding = False
    else:
      print("Please choose 1, 2, or 3")

  # Player decisions
  if decision == "3":
    deciding = True
    solve = input("Your guess to solve: ...... ").upper() # TODO: clean
    if solve == puzzle:
      print("YOU WIN!")
      print("Player", turn % 3, "won!")
      print("Winnings:", winnings)
      if commentary_system:
        commentary_system.solve_attempt_commentary(solve, True, puzzle, turn % 3, winnings)
      is_solved = True
      exit()
      #break #TODO: not just exit here
    else:
      print("Wrong ... next player")
      if commentary_system:
        commentary_system.solve_attempt_commentary(solve, False, puzzle, turn % 3, winnings)
      #turn = turn + 1
      #print("The clue is:", clue)
      #print_board(showing)
      #continue
      guess = "_"
      dollar = 0
  elif decision == "2":
    winnings[(turn % 3)] = winnings[(turn % 3)] - 250
    is_one_vowel = False
    while is_one_vowel != True:
      vowel = input("Guess a vowel: ").upper()
      if len(vowel) != 1:
        print("Guess only one letter")
      else:
        is_one_vowel = is_vowel(vowel)

      if not is_one_vowel:
        print("Not a vowel")
    guess = vowel
    dollar = 0
    if commentary_system:
      commentary_system.vowel_purchase_commentary(vowel, turn % 3, winnings)
  elif decision == "1":
    # Spin wheel
    dollar = spin_wheel()
    guess = ""
    if dollar == 0:
      print("Sorry! Lose a turn. Next player")
      #turn = turn + 1
      #continue
      guess = "_"
    elif dollar == -1:
      print("Oh No! Bankrupt!")
      winnings[(turn % 3)] = 0
      #turn = turn + 1
      #continue
      guess = "_"
    is_one_consonant = False
    if guess == "_":
      is_one_consonant = True # Hacky way
    while is_one_consonant != True:
      guess = input("Name a consonant .... ").upper()
      if len(guess) != 1: 
        print("Guess only one letter")
      else:
        is_one_consonant = is_consonant(guess)

      if not is_one_consonant:
        print("Not a consonant")
  return guess, dollar

def is_consonant(guess):
  consonants = "BCDFGHJKLMNPQRSTVWXYZ"
  if guess in consonants:
    return True
  else:
    return False

def is_vowel(guess):
  vowels = "AEIOU"
  if guess in vowels:
    return True
  else:
    return False

def print_board(showing):
  words = showing.split(" ")
  to_print = ""
  for word in words:
    for character in word:
      to_print = to_print + character + " "
    to_print = to_print + "\n"
  print(to_print)

def spin_wheel():
  wheel_values = [0,-1,500,550,600,650,700,750,800,850,900,-1,500,550,600,650,700,750,800,850,900,500,550,600]
  # Note that the wheel changes over time ... free play now an 850. Different rounds, etc.
  print("Wheel is spinning ....")
  print("It landed on ....")
  time.sleep(2) # Drama!
  try:
    ascii_wheel.draw_ascii_wheel(wheel_values, radius=18, label_style="long")
  except:
    print("🎡 [Wheel spinning animation would appear here]")
  dollar = random.choice(wheel_values)
  print("....", dollar, "dollars")
  
  # Add commentary for wheel spin results
  if commentary_system:
    # We'll add the player info when this is called from the main game loop
    pass
    
  return dollar


def play_random_game(type_of_players, enable_commentary=True, commentary_style="dramatic", api_key=None):
  global commentary_system
  
  # Initialize commentary system
  if enable_commentary:
    commentary_system = WheelOfFortuneCommentary(
      api_key=api_key,
      commentary_style=commentary_style,
      enable_commentary=True
    )
  else:
    commentary_system = None

  # Play the game
  puzzle, clue, date, game_type = get_random_puzzle()
  print("Welcome to Wheel of Fortune")
  print("You are playing a game of type:", game_type)
  print("The clue is:", clue)
  
  # Game start commentary
  if commentary_system:
    commentary_system.game_start_commentary(clue, game_type)

  # Mask out word
  showing = puzzle
  showing = re.sub(r"[A-Z]","_",showing)
  print_board(showing)

  # Play the game
  guess = ""
  previous_guesses = []
  turn = 0

  winnings = [0,0,0]
  dollar = 0
  is_solved = False

  while showing != puzzle:
    time.sleep(2) # Let humans see what is going on
    # Ends wierd if last letter is guessed and not solved.# TODO
    print("It is player", turn % 3, "'s turn")

    # Type of player
    type_of_player = type_of_players[turn % 3]
    print("This player is:", type_of_player)
    
    # Player turn commentary
    if commentary_system:
      commentary_system.player_turn_commentary(turn % 3, type_of_player, winnings)

    if type_of_player == "human":
      guess, dollar = human_turn(showing, winnings, previous_guesses, turn, puzzle)
    elif type_of_player == "morse":
      guess, dollar = computer_turn_morse(showing, winnings, previous_guesses, turn)
    elif type_of_player == "oxford":
      guess, dollar = computer_turn_oxford(showing, winnings, previous_guesses, turn)
    elif type_of_player == "trigram":
      guess, dollar = computer_turn_trigrams_bigrams(showing, winnings, previous_guesses, turn)
    elif type_of_player == "smart":
      guess, dollar = computer_turn_smart(showing, winnings, previous_guesses, turn)
    elif type_of_player == "conservative":
      guess, dollar = computer_turn_smart_conservative(showing, winnings, previous_guesses, turn)
    elif type_of_player == "aggressive":
      guess, dollar = computer_turn_smart_aggressive(showing, winnings, previous_guesses, turn)

    # Add wheel spin commentary for computer players (human commentary is handled in human_turn)
    if type_of_player != "human" and commentary_system and dollar != 0:
      commentary_system.wheel_spin_commentary(dollar, turn % 3, winnings)

    # Double check that guess has not already been said (I've seen it on TV before)
    if guess in previous_guesses and guess != "_":
      print("Sorry, that's already been guessed .... next player")
      turn = turn + 1
    else:
      # Update board
      previous_guesses.append(guess)
      correct_places = []
      for pos,char in enumerate(puzzle):
        if(char == guess):
            correct_places.append(pos)
      #print(correct_places)
      if guess == "_": # Hacky way to say the comp got it wrong or bankrupt, etc.
        turn = turn + 1
      elif len(correct_places) < 1:
        print("Sorry, not in the puzzle ... next player")
        turn = turn + 1
        
      # Add guess result commentary
      if commentary_system and guess != "_":
        commentary_system.guess_result_commentary(
          guess, len(correct_places), dollar, showing, clue, 
          previous_guesses, turn % 3, winnings
        )
        
    winnings[(turn % 3)] = winnings[(turn % 3)] + (dollar * len(correct_places))
    for correct_letter in correct_places:
      showing = showing[:correct_letter] + guess + showing[correct_letter + 1:]
    print("Winnings:", winnings)
    print("Previous guesses:", previous_guesses)
    print("The clue is:", clue)
    print_board(showing)
    
    # Add puzzle progress commentary
    if commentary_system:
      commentary_system.puzzle_progress_commentary(showing, clue, previous_guesses)

  while not is_solved:
    print("Player", turn % 3, "has a chance to solve")
    type_of_player = type_of_players[turn % 3] # wouldn't have hit this above
    # If human, let them guess, otheerwise let computer guess
    if type_of_player == "human":
      solve = input("Your guess to solve: ...... ").upper() # TODO: clean
    else:
      solve = showing
  
    if solve == puzzle:
      print("Player", turn % 3, "won!")
      print("Winnings:", winnings)
      if commentary_system:
        commentary_system.solve_attempt_commentary(solve, True, puzzle, turn % 3, winnings)
      is_solved = True
    else:
      print("Wrong ... next player")
      if commentary_system:
        commentary_system.solve_attempt_commentary(solve, False, puzzle, turn % 3, winnings)
      turn = turn + 1
      print("The clue is:", clue)
      print_board(showing)

def print_usage():
  print("\nWheel of Fortune with ChatGPT Commentary")
  print("=" * 50)
  print("Usage: python wheel_of_fortune_with_commentary.py [player1] [player2] [player3] [options]")
  print("\nPlayer Types:")
  print("  human       - Human player")
  print("  morse       - Computer using Morse code frequency")
  print("  oxford      - Computer using Oxford dictionary frequency")
  print("  trigram     - Computer using trigram/bigram analysis")
  print("  smart       - Smart AI player")
  print("  conservative- Conservative AI player")
  print("  aggressive  - Aggressive AI player")
  print("\nCommentary Options:")
  print("  --no-commentary     Disable ChatGPT commentary")
  print("  --style=STYLE       Commentary style: dramatic, humorous, professional, casual")
  print("  --api-key=KEY       OpenAI API key (or set OPENAI_API_KEY environment variable)")
  print("\nExamples:")
  print("  python wheel_of_fortune_with_commentary.py human smart conservative")
  print("  python wheel_of_fortune_with_commentary.py human morse oxford --style=humorous")
  print("  python wheel_of_fortune_with_commentary.py smart smart smart --no-commentary")
  print()

if __name__ == '__main__':
  # Parse command line arguments
  args = sys.argv[1:]
  
  # Default settings
  type_of_players = []
  enable_commentary = True
  commentary_style = "dramatic"
  api_key = None
  
  # Parse arguments
  for arg in args:
    if arg.startswith('--'):
      if arg == '--no-commentary':
        enable_commentary = False
      elif arg.startswith('--style='):
        commentary_style = arg.split('=')[1]
      elif arg.startswith('--api-key='):
        api_key = arg.split('=')[1]
      elif arg == '--help':
        print_usage()
        exit()
    else:
      type_of_players.append(arg)
  
  print("Players:", type_of_players)
  print("Commentary enabled:", enable_commentary)
  if enable_commentary:
    print("Commentary style:", commentary_style)
  
  if len(type_of_players) != 3:
    print("There should be 3 players ... creating a default game with smart AI players")
    print("Available player types: human, morse, oxford, trigram, smart, conservative, aggressive")
    print("Use --help for more options")
    type_of_players = ["human", "smart", "conservative"] # Updated default with smart players
    time.sleep(3)

  play_random_game(type_of_players, enable_commentary, commentary_style, api_key)
