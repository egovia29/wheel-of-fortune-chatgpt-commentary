#!/usr/bin/env python3
"""
Setup script for Wheel of Fortune ChatGPT Commentary
"""

import os
import sys
import json
from commentary_config import CommentaryConfig

def setup_api_key():
    """Interactive setup for OpenAI API key"""
    print("🔑 OpenAI API Key Setup")
    print("=" * 30)
    
    current_key = os.getenv('OPENAI_API_KEY', '')
    if current_key:
        print(f"✅ Found existing API key: {current_key[:8]}...")
        use_existing = input("Use existing key? (y/n): ").lower().strip()
        if use_existing == 'y':
            return current_key
    
    print("\nTo use ChatGPT commentary, you need an OpenAI API key.")
    print("Get one at: https://platform.openai.com/api-keys")
    print("\nOptions:")
    print("1. Enter API key now (will be saved to config file)")
    print("2. Set OPENAI_API_KEY environment variable")
    print("3. Skip (commentary will be disabled)")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == '1':
        api_key = input("Enter your OpenAI API key: ").strip()
        if api_key:
            return api_key
        else:
            print("No key entered.")
            return None
    elif choice == '2':
        print("\nSet the environment variable like this:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("Then restart your terminal and run the game.")
        return None
    else:
        print("Skipping API key setup. Commentary will be disabled.")
        return None

def setup_commentary_style():
    """Interactive setup for commentary style"""
    print("\n🎭 Commentary Style Setup")
    print("=" * 30)
    
    styles = {
        '1': ('dramatic', 'Enthusiastic game show host (like Pat Sajak)'),
        '2': ('humorous', 'Witty and funny with clever jokes'),
        '3': ('professional', 'Analytical sports commentator style'),
        '4': ('casual', 'Friendly, conversational tone')
    }
    
    print("Choose your commentary style:")
    for key, (style, description) in styles.items():
        print(f"{key}. {style.title()}: {description}")
    
    choice = input("\nChoose style (1-4): ").strip()
    
    if choice in styles:
        return styles[choice][0]
    else:
        print("Invalid choice. Using dramatic style.")
        return 'dramatic'

def create_sample_config():
    """Create a sample configuration file"""
    config = CommentaryConfig()
    
    # Get user preferences
    api_key = setup_api_key()
    style = setup_commentary_style()
    
    # Update configuration
    if api_key:
        config.set('api_key', api_key)
        config.set('enable_commentary', True)
    else:
        config.set('enable_commentary', False)
    
    config.set('commentary_style', style)
    
    # Save configuration
    config.save_to_file('commentary_settings.json')
    
    print(f"\n✅ Configuration saved to commentary_settings.json")
    print(f"Commentary enabled: {config.get('enable_commentary')}")
    print(f"Style: {config.get('commentary_style')}")
    
    return config

def test_commentary():
    """Test the commentary system"""
    print("\n🧪 Testing Commentary System")
    print("=" * 30)
    
    try:
        from chatgpt_commentary import WheelOfFortuneCommentary
        
        # Load configuration
        config = CommentaryConfig()
        config.load_from_file('commentary_settings.json')
        
        # Test commentary system
        commentary = WheelOfFortuneCommentary(
            api_key=config.get('api_key'),
            commentary_style=config.get('commentary_style'),
            enable_commentary=config.get('enable_commentary')
        )
        
        if commentary.enable_commentary:
            print("🎙️ Testing commentary generation...")
            commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
            print("✅ Commentary system working!")
        else:
            print("ℹ️ Commentary is disabled (no API key or disabled in config)")
            
    except Exception as e:
        print(f"❌ Error testing commentary: {e}")
        print("You can still play without commentary.")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing Dependencies")
    print("=" * 30)
    
    try:
        import subprocess
        import sys
        
        # Install openai package
        print("Installing OpenAI package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
        print("✅ OpenAI package installed")
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please run: pip install openai")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main setup function"""
    print("🎡 Wheel of Fortune ChatGPT Commentary Setup")
    print("=" * 50)
    
    # Check if setup has been run before
    if os.path.exists('commentary_settings.json'):
        print("Found existing configuration.")
        reconfigure = input("Reconfigure? (y/n): ").lower().strip()
        if reconfigure != 'y':
            print("Using existing configuration.")
            test_commentary()
            return
    
    # Install dependencies
    try:
        import openai
        print("✅ OpenAI package already installed")
    except ImportError:
        install_dependencies()
    
    # Create configuration
    config = create_sample_config()
    
    # Test the system
    test_commentary()
    
    print("\n🎮 Ready to Play!")
    print("=" * 20)
    print("Run the game with:")
    print("python wheel_of_fortune_with_commentary.py human smart conservative")
    print("\nOr use the original game without commentary:")
    print("python wheel_of_fortune.py human smart conservative")
    print("\nFor more options:")
    print("python wheel_of_fortune_with_commentary.py --help")

if __name__ == "__main__":
    main()
