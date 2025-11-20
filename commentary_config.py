"""
Configuration settings for Wheel of Fortune ChatGPT Commentary
"""

import os
from typing import Dict, Any

class CommentaryConfig:
    """Configuration class for the commentary system"""
    
    def __init__(self):
        self.settings = {
            # API Settings
            'api_key': os.getenv('OPENAI_API_KEY', ''),
            'model': 'gpt-3.5-turbo',
            'max_tokens': 100,
            'temperature': 0.8,
            
            # Commentary Settings
            'enable_commentary': True,
            'commentary_style': 'dramatic',  # dramatic, humorous, professional, casual
            'delay_range': (1, 3),  # seconds
            
            # Feature Toggles
            'game_start_commentary': True,
            'wheel_spin_commentary': True,
            'guess_result_commentary': True,
            'vowel_purchase_commentary': True,
            'solve_attempt_commentary': True,
            'player_turn_commentary': True,
            'puzzle_progress_commentary': True,
            
            # Commentary Frequency
            'progress_commentary_threshold': 75,  # Only comment when puzzle is X% complete
            'max_commentary_per_turn': 2,  # Limit commentary to avoid spam
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self.settings[key] = value
    
    def update(self, new_settings: Dict[str, Any]) -> None:
        """Update multiple configuration values"""
        self.settings.update(new_settings)
    
    def load_from_file(self, filepath: str) -> None:
        """Load configuration from a JSON file"""
        try:
            import json
            with open(filepath, 'r') as f:
                file_settings = json.load(f)
                self.update(file_settings)
        except FileNotFoundError:
            print(f"Configuration file {filepath} not found. Using defaults.")
        except json.JSONDecodeError:
            print(f"Invalid JSON in {filepath}. Using defaults.")
    
    def save_to_file(self, filepath: str) -> None:
        """Save current configuration to a JSON file"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get_style_description(self, style: str) -> str:
        """Get description of a commentary style"""
        descriptions = {
            'dramatic': 'Enthusiastic game show host style with excitement and suspense',
            'humorous': 'Witty and funny commentary with clever jokes and puns',
            'professional': 'Analytical sports commentator style with strategic insights',
            'casual': 'Friendly, conversational commentary like watching with friends'
        }
        return descriptions.get(style, 'Unknown style')
    
    def validate_settings(self) -> list:
        """Validate current settings and return list of issues"""
        issues = []
        
        # Check API key
        if self.get('enable_commentary') and not self.get('api_key'):
            issues.append("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or use --api-key option.")
        
        # Check style
        valid_styles = ['dramatic', 'humorous', 'professional', 'casual']
        if self.get('commentary_style') not in valid_styles:
            issues.append(f"Invalid commentary style. Must be one of: {', '.join(valid_styles)}")
        
        # Check delay range
        delay_range = self.get('delay_range')
        if not isinstance(delay_range, tuple) or len(delay_range) != 2:
            issues.append("delay_range must be a tuple of (min, max) seconds")
        elif delay_range[0] < 0 or delay_range[1] < delay_range[0]:
            issues.append("Invalid delay_range values")
        
        return issues

# Global configuration instance
config = CommentaryConfig()

# Load configuration from file if it exists
config.load_from_file('commentary_settings.json')
