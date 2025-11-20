"""
Setup Script for FREE Commentary System
Interactive configuration and testing
"""

import os
import sys
from free_commentary_system import WheelOfFortuneCommentary

def print_banner():
    """Print welcome banner"""
    print("🎡" + "=" * 58 + "🎡")
    print("🎙️  WHEEL OF FORTUNE FREE COMMENTARY SETUP  🎙️")
    print("🎡" + "=" * 58 + "🎡")
    print("🆓 100% FREE - No API keys needed!")
    print("🎭 Smart commentary that feels like real AI!")
    print("⚡ Works immediately - no configuration required!")
    print("🎡" + "=" * 58 + "🎡")

def test_commentary_system():
    """Test the commentary system"""
    print("\n🧪 TESTING COMMENTARY SYSTEM")
    print("=" * 40)
    
    try:
        # Test basic functionality
        print("📝 Testing basic functionality...")
        commentary = WheelOfFortuneCommentary(commentary_style="dramatic", delay_range=(0.5, 1))
        
        print("✅ Commentary system initialized successfully!")
        
        # Test different events
        print("\n🎮 Testing game events...")
        commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
        commentary.wheel_spin_commentary(750, 0, [0, 0, 0])
        commentary.guess_result_commentary("R", 2, 750, "_ _ R _ _ _", "FAMOUS PEOPLE", ["R"], 0, [1500, 0, 0])
        
        print("✅ All commentary events working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing commentary system: {e}")
        return False

def test_all_styles():
    """Test all commentary styles"""
    print("\n🎭 TESTING ALL COMMENTARY STYLES")
    print("=" * 40)
    
    styles = {
        "dramatic": "Exciting game show host style",
        "humorous": "Witty jokes and puns",
        "professional": "Sports commentator approach", 
        "casual": "Friendly conversational tone"
    }
    
    for style, description in styles.items():
        print(f"\n🎨 Testing {style.upper()} style ({description}):")
        try:
            commentary = WheelOfFortuneCommentary(commentary_style=style, delay_range=(0.3, 0.8))
            commentary.wheel_spin_commentary(850, 0, [0, 0, 0])
            print(f"✅ {style.upper()} style working perfectly!")
        except Exception as e:
            print(f"❌ Error with {style} style: {e}")

def interactive_style_demo():
    """Interactive demo of commentary styles"""
    print("\n🎪 INTERACTIVE STYLE DEMO")
    print("=" * 40)
    
    styles = ["dramatic", "humorous", "professional", "casual"]
    
    print("Choose a commentary style to demo:")
    for i, style in enumerate(styles, 1):
        print(f"{i}. {style.title()}")
    
    while True:
        try:
            choice = input("\nEnter 1-4 (or 'all' for all styles): ").strip().lower()
            
            if choice == 'all':
                for style in styles:
                    print(f"\n🎨 {style.upper()} Style Demo:")
                    commentary = WheelOfFortuneCommentary(commentary_style=style, delay_range=(0.5, 1))
                    commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
                    commentary.wheel_spin_commentary(750, 0, [0, 0, 0])
                    commentary.guess_result_commentary("R", 1, 750, "R _ _ _ _ _", "FAMOUS PEOPLE", ["R"], 0, [750, 0, 0])
                    print("-" * 30)
                break
            
            elif choice in ['1', '2', '3', '4']:
                style = styles[int(choice) - 1]
                print(f"\n🎨 {style.upper()} Style Demo:")
                commentary = WheelOfFortuneCommentary(commentary_style=style, delay_range=(0.5, 1))
                
                print("🎮 Sample game events with commentary:")
                commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
                commentary.wheel_spin_commentary(850, 0, [0, 0, 0])
                commentary.guess_result_commentary("R", 2, 850, "R _ R _ _ _", "FAMOUS PEOPLE", ["R"], 0, [1700, 0, 0])
                commentary.vowel_purchase_commentary("A", 0, [1450, 0, 0])
                commentary.solve_attempt_commentary("ROBERT DOWNEY JR", True, "ROBERT DOWNEY JR", 0, [1450, 0, 0])
                break
            
            else:
                print("Please enter 1-4 or 'all'")
                
        except (ValueError, IndexError):
            print("Please enter a valid choice (1-4 or 'all')")

def create_config_file():
    """Create a simple configuration file"""
    print("\n⚙️ CREATING CONFIGURATION FILE")
    print("=" * 40)
    
    print("Choose your preferred settings:")
    
    # Commentary style
    styles = ["dramatic", "humorous", "professional", "casual"]
    print("\nCommentary styles:")
    for i, style in enumerate(styles, 1):
        print(f"{i}. {style.title()}")
    
    while True:
        try:
            choice = input("Choose default style (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                default_style = styles[int(choice) - 1]
                break
            else:
                print("Please enter 1-4")
        except ValueError:
            print("Please enter a valid number")
    
    # Commentary timing
    print("\nCommentary timing:")
    print("1. Fast (0.5-1 seconds)")
    print("2. Normal (1-2 seconds)")
    print("3. Slow (2-3 seconds)")
    
    while True:
        try:
            choice = input("Choose timing (1-3): ").strip()
            if choice == '1':
                delay_range = (0.5, 1)
                break
            elif choice == '2':
                delay_range = (1, 2)
                break
            elif choice == '3':
                delay_range = (2, 3)
                break
            else:
                print("Please enter 1-3")
        except ValueError:
            print("Please enter a valid number")
    
    # Create config file
    config_content = f"""# FREE Commentary System Configuration
# Generated by setup script

DEFAULT_STYLE = "{default_style}"
DELAY_RANGE = {delay_range}
ENABLE_COMMENTARY = True

# Available styles: dramatic, humorous, professional, casual
# Delay range: (min_seconds, max_seconds)
"""
    
    try:
        with open("commentary_config.py", "w") as f:
            f.write(config_content)
        
        print(f"✅ Configuration saved to 'commentary_config.py'")
        print(f"📝 Default style: {default_style}")
        print(f"⏱️ Timing: {delay_range[0]}-{delay_range[1]} seconds")
        
    except Exception as e:
        print(f"❌ Error creating config file: {e}")

def check_system_requirements():
    """Check system requirements"""
    print("\n🔍 CHECKING SYSTEM REQUIREMENTS")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 7):
        print("✅ Python version is compatible!")
    else:
        print("⚠️  Python 3.7+ recommended for best compatibility")
    
    # Check required modules
    required_modules = ['random', 'time', 'typing']
    
    print("\n📦 Checking required modules:")
    all_good = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Missing")
            all_good = False
    
    if all_good:
        print("\n🎉 All requirements satisfied!")
        print("🚀 Your system is ready for FREE commentary!")
    else:
        print("\n⚠️  Some modules are missing, but the system should still work")
    
    return all_good

def show_usage_examples():
    """Show usage examples"""
    print("\n📖 USAGE EXAMPLES")
    print("=" * 40)
    
    examples = [
        {
            "title": "Basic Usage",
            "code": """from free_commentary_system import WheelOfFortuneCommentary

# Initialize commentary
commentary = WheelOfFortuneCommentary(commentary_style="dramatic")

# Use in your game
commentary.game_start_commentary("FAMOUS PEOPLE", "Celebrity Names")
commentary.wheel_spin_commentary(750, 0, [0, 0, 0])"""
        },
        {
            "title": "Change Style During Game",
            "code": """# Start with dramatic
commentary = WheelOfFortuneCommentary(commentary_style="dramatic")

# Change to humorous
commentary.set_commentary_style("humorous")

# Toggle on/off
commentary.toggle_commentary()"""
        },
        {
            "title": "Custom Timing",
            "code": """# Faster commentary
commentary = WheelOfFortuneCommentary(
    commentary_style="professional",
    delay_range=(0.5, 1)  # 0.5-1 second delays
)"""
        }
    ]
    
    for example in examples:
        print(f"\n🔹 {example['title']}:")
        print(example['code'])

def main_menu():
    """Main setup menu"""
    while True:
        print("\n🎯 SETUP MENU")
        print("=" * 30)
        print("1. Test commentary system")
        print("2. Test all commentary styles")
        print("3. Interactive style demo")
        print("4. Create configuration file")
        print("5. Check system requirements")
        print("6. Show usage examples")
        print("7. Exit setup")
        
        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == '1':
            test_commentary_system()
        elif choice == '2':
            test_all_styles()
        elif choice == '3':
            interactive_style_demo()
        elif choice == '4':
            create_config_file()
        elif choice == '5':
            check_system_requirements()
        elif choice == '6':
            show_usage_examples()
        elif choice == '7':
            print("\n🎊 Setup complete! Enjoy your FREE commentary system!")
            break
        else:
            print("Please enter a valid choice (1-7)")

def main():
    """Main function"""
    print_banner()
    
    # Quick system check
    print("\n🔍 Quick system check...")
    if check_system_requirements():
        print("✅ System ready!")
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    if test_commentary_system():
        print("✅ Commentary system working perfectly!")
        
        # Show main menu
        main_menu()
    else:
        print("❌ There seems to be an issue with the commentary system.")
        print("Please check that 'free_commentary_system.py' is in the same directory.")

if __name__ == "__main__":
    main()
