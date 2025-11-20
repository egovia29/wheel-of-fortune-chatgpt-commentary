"""
ASCII Wheel drawing for Wheel of Fortune
Mock implementation for testing
"""

def draw_ascii_wheel(wheel_values, radius=18, label_style="long"):
    """
    Draw an ASCII representation of the wheel
    This is a simplified mock implementation
    """
    print("    🎡 WHEEL OF FORTUNE 🎡")
    print("         ╭─────────╮")
    print("       ╭─┴─────────┴─╮")
    print("     ╭─┴─────────────┴─╮")
    print("   ╭─┴─────────────────┴─╮")
    print("  ╱                       ╲")
    print(" ╱         SPINNING        ╲")
    print("╱                           ╲")
    print("│            🎯             │")
    print("╲                           ╱")
    print(" ╲         WHEEL           ╱")
    print("  ╲                       ╱")
    print("   ╰─┬─────────────────┬─╯")
    print("     ╰─┬─────────────┬─╯")
    print("       ╰─┬─────────┬─╯")
    print("         ╰─────────╯")
    print()
    
    # Show some sample values
    print("Wheel contains values like:")
    sample_values = [v for v in wheel_values if v > 0][:8]
    for i, val in enumerate(sample_values):
        if i % 4 == 0:
            print()
        print(f"${val:>4}", end="  ")
    print("\n...plus BANKRUPT and LOSE A TURN")
    print()
