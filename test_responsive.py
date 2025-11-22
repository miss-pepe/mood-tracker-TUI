#!/usr/bin/env python
"""Test script to verify responsive behavior of the Mood Tracker TUI.

This script provides information about the responsive features and how to test them.
"""

import os


def print_test_guide():
    """Print a guide for testing responsive features."""
    print("=" * 80)
    print("MOOD TRACKER TUI - RESPONSIVE DESIGN TEST GUIDE")
    print("=" * 80)
    print()
    print("The Mood Tracker TUI now features full responsive design!")
    print()
    print("HOW TO TEST:")
    print("-" * 80)
    print()
    print("1. START THE APP:")
    print("   python run.py")
    print()
    print("2. RESIZE YOUR TERMINAL:")
    print("   - Make it narrower (minimum: 80 columns)")
    print("   - Make it wider (maximum optimized: 140 columns)")
    print("   - The UI should adapt in real-time!")
    print()
    print("3. TEST ALL SCREENS:")
    print("   - Main screen: Automatically visible")
    print("   - Calendar view: Press 'M'")
    print("   - Export modal: Press 'E'")
    print("   - History view: Press 'V'")
    print("   - Theme mascot: Press 'T' (cycles themes)")
    print("   - Reflection modal: Press 'Enter' or 'S' to save a mood")
    print()
    print("4. VERIFY RESPONSIVE BEHAVIOR:")
    print("   ✓ Box width adjusts smoothly")
    print("   ✓ Text remains centered and readable")
    print("   ✓ Modals scale appropriately")
    print("   ✓ No overlapping or cut-off content")
    print("   ✓ Calendar adapts to available space")
    print()
    print("SCREEN SIZE RANGES:")
    print("-" * 80)
    print()
    print("• SMALL (80-100 cols)  : Minimum viable layout")
    print("• MEDIUM (100-125 cols): Optimal experience")
    print("• LARGE (125-140+ cols): Maximum width with extra padding")
    print()
    print("RESPONSIVE FEATURES:")
    print("-" * 80)
    print()
    print("✓ Dynamic box width calculation")
    print("✓ Real-time resize event handling")
    print("✓ Flexible modal dialogs")
    print("✓ Adaptive calendar grid")
    print("✓ Responsive history table")
    print("✓ Scalable theme mascot popup")
    print("✓ Fluid mood companion widget")
    print()
    print("=" * 80)
    print()


def check_terminal_size():
    """Check and display current terminal size."""
    try:
        size = os.get_terminal_size()
        print(f"CURRENT TERMINAL SIZE: {size.columns} columns × {size.lines} lines")
        print()

        if size.columns < 80:
            print("⚠️  WARNING: Terminal is narrower than minimum (80 cols)")
            print("   Some content may not display correctly.")
        elif size.columns >= 80 and size.columns < 100:
            print("✓ Terminal size: SMALL (functional)")
        elif size.columns >= 100 and size.columns < 125:
            print("✓ Terminal size: MEDIUM (good)")
        elif size.columns >= 125 and size.columns < 140:
            print("✓ Terminal size: LARGE (optimal)")
        else:
            print("✓ Terminal size: ULTRA-WIDE (excellent)")

        print()
    except Exception as e:
        print(f"Could not detect terminal size: {e}")
        print()


if __name__ == "__main__":
    print_test_guide()
    check_terminal_size()

    print("Ready to test? Run: python run.py")
    print()
