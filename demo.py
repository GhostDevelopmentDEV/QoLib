#!/usr/bin/env python3
"""
QoLib Demo - Full library capabilities demonstration

Run: python demo.py
"""

import time
import random
from qolib import *

def demo_colors():
    """Color system demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("COLORS", color=Color.CYAN))
    print()
    
    # Basic colors
    print("Basic colors:")
    print(Color.BLACK + "Black" + Color.RESET, end=" ")
    print(Color.RED + "Red" + Color.RESET, end=" ")
    print(Color.GREEN + "Green" + Color.RESET, end=" ")
    print(Color.YELLOW + "Yellow" + Color.RESET, end=" ")
    print(Color.BLUE + "Blue" + Color.RESET, end=" ")
    print(Color.MAGENTA + "Magenta" + Color.RESET, end=" ")
    print(Color.CYAN + "Cyan" + Color.RESET, end=" ")
    print(Color.WHITE + "White" + Color.RESET)
    
    print("\nBright colors:")
    print(Color.GRAY + "Gray" + Color.RESET, end=" ")
    print(Color.LIGHT_RED + "Light Red" + Color.RESET, end=" ")
    print(Color.LIGHT_GREEN + "Light Green" + Color.RESET, end=" ")
    print(Color.LIGHT_YELLOW + "Light Yellow" + Color.RESET, end=" ")
    print(Color.LIGHT_BLUE + "Light Blue" + Color.RESET, end=" ")
    print(Color.LIGHT_MAGENTA + "Light Magenta" + Color.RESET, end=" ")
    print(Color.LIGHT_CYAN + "Light Cyan" + Color.RESET, end=" ")
    print(Color.LIGHT_WHITE + "Light White" + Color.RESET)
    
    print("\nText styles:")
    print(Color.BOLD + "Bold" + Color.RESET, end=" ")
    print(Color.DIM + "Dim" + Color.RESET, end=" ")
    print(Color.ITALIC + "Italic" + Color.RESET, end=" ")
    print(Color.UNDERLINE + "Underlined" + Color.RESET, end=" ")
    print(Color.BLINK + "Blinking" + Color.RESET, end=" ")
    print(Color.REVERSE + "Reversed" + Color.RESET)
    
    print("\nBackground colors:")
    print(Color.BG_RED + "Red background" + Color.RESET, end=" ")
    print(Color.BG_GREEN + "Green background" + Color.RESET, end=" ")
    print(Color.BG_BLUE + "Blue background" + Color.RESET, end=" ")
    print(Color.BG_YELLOW + "Yellow background" + Color.RESET)
    
    print("\nRGB colors:")
    for r, g, b, name in [
        (255, 105, 180, "Pink"),
        (255, 165, 0, "Orange"),
        (50, 205, 50, "Lime"),
        (30, 144, 255, "Light Blue"),
        (138, 43, 226, "Purple")
    ]:
        print(Color.fg_rgb(r, g, b) + name + Color.RESET, end=" ")
    
    print("\n\nHEX colors:")
    for hex_code, name in [
        ("#FF6B6B", "Coral"),
        ("#4ECDC4", "Turquoise"),
        ("#FFE66D", "Lemon"),
        ("#6A0572", "Violet"),
        ("#1A535C", "Dark Teal")
    ]:
        print(Color.fg_hex(hex_code) + name + Color.RESET, end=" ")
    
    print("\n\nGradients:")
    print(Color.gradient("Rainbow gradient", Color.RAINBOW))
    print(Color.gradient("Pastel gradient", Color.PASTEL))
    
    input("\n\nPress Enter to continue...")

def demo_messages():
    """MessageService demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("MESSAGES", color=Color.CYAN))
    print()
    
    # Configuration
    MessageService.configure(show_icons=True, show_timestamps=True)
    
    # All message types
    MessageService.info("Regular information message")
    MessageService.info2("Additional information")
    MessageService.pending("Long operation in progress...")
    MessageService.success("Operation completed successfully!")
    MessageService.success2("Success with alternative color")
    MessageService.warning("Warning: check settings")
    MessageService.error("Critical error occurred!")
    MessageService.question("Are you sure you want to continue?")
    MessageService.debug("Debug info: x=42, y=3.14")
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Custom styles
    MessageService.register_style(
        name="security",
        prefix="[SECURITY]",
        color=Color.LIGHT_RED + Color.BOLD,
        icon="🔒"
    )
    
    MessageService.register_style(
        name="celebrate",
        prefix="[HOORAY!]",
        color=Color.fg_hex("#FFD700") + Color.BOLD + Color.BLINK,
        icon="🎉"
    )
    
    MessageService.custom("security", "Unauthorized access attempt detected")
    MessageService.custom("celebrate", "Congratulations! You've reached the goal!")
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Messages with indentation
    MessageService.info("Root message", indent=0)
    MessageService.info("├── Level 1", indent=2)
    MessageService.info("│   ├── Level 2", indent=4)
    MessageService.info("│   └── Another item", indent=4)
    MessageService.info("└── Last item", indent=2)
    
    input("\n\nPress Enter to continue...")

def demo_animations():
    """Animations demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("ANIMATIONS", color=Color.CYAN))
    print()
    
    # Typewriter effect
    print("Typewriter effect:")
    AnimationService.typing_effect(
        "Hello! I'm QoLib - a library for beautiful console output.",
        speed=0.03,
        color=Color.LIGHT_CYAN
    )
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Spinners
    print("Spinners (loading indicators):")
    
    print("\n1. Simple spinner:")
    with AnimationService.spinner("Loading data...") as spinner:
        time.sleep(2)
        spinner.update_message("Processing...")
        time.sleep(2)
    
    print("\n2. Spinner with custom icons:")
    frames = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    with AnimationService.spinner("Moon cycle...", frames=frames, delay=0.2) as spinner:
        time.sleep(3)
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Progress bars
    print("Progress bars:")
    
    print("\n1. Simple progress bar:")
    with AnimationService.progress_bar(50, "Loading files") as bar:
        for i in range(51):
            bar.update()
            time.sleep(0.05)
    
    print("\n2. Progress bar without counter:")
    with AnimationService.progress_bar(
        100, 
        "Processing",
        show_counter=False,
        complete_char="▓",
        incomplete_char="░"
    ) as bar:
        for i in range(101):
            bar.update()
            time.sleep(0.02)
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Countdown
    print("Countdown:")
    AnimationService.countdown(5, "Starting in", "Let's go!")
    
    input("\n\nPress Enter to continue...")

def demo_tables():
    """Tables demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("TABLES", color=Color.CYAN))
    print()
    
    # Table 1: Simple
    print("1. Simple table:")
    table1 = TablePrinter(
        headers=["ID", "Name", "Email", "Status"],
        border_style="simple"
    )
    
    table1.add_rows([
        [1, "Anna Ivanova", "anna@example.com", "Active"],
        [2, "Ivan Petrov", "ivan@example.com", "Inactive"],
        [3, "Maria Sidorova", "maria@example.com", "Active"],
        [4, "Alexey Smirnov", "alex@example.com", "Pending"]
    ])
    
    table1.print()
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Table 2: Styled
    print("2. Styled table:")
    table2 = TablePrinter(
        headers=["Product", "Price", "Qty", "Total"],
        column_align=["left", "right", "center", "right"],
        border_style="rounded",
        header_color=Color.LIGHT_GREEN + Color.BOLD,
        zebra_stripes=True,
        stripe_color=Color.DIM
    )
    
    table2.add_rows([
        ["Laptop", "75,000 ₽", 2, "150,000 ₽"],
        ["Mouse", "1,500 ₽", 5, "7,500 ₽"],
        ["Keyboard", "3,200 ₽", 3, "9,600 ₽"],
        ["Monitor", "32,000 ₽", 1, "32,000 ₽"],
        ["Headphones", "5,800 ₽", 4, "23,200 ₽"]
    ])
    
    table2.print()
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Table 3: Double borders
    print("3. Table with double borders:")
    table3 = TablePrinter(
        headers=["Month", "Sales", "Growth", "Target"],
        column_align=["left", "right", "center", "right"],
        border_style="double",
        header_color=Color.LIGHT_BLUE + Color.BOLD
    )
    
    table3.add_rows([
        ["January", "1,250,000 ₽", "+12%", "1,100,000 ₽"],
        ["February", "1,430,000 ₽", "+15%", "1,200,000 ₽"],
        ["March", "1,680,000 ₽", "+18%", "1,350,000 ₽"],
        ["April", "1,920,000 ₽", "+14%", "1,500,000 ₽"],
        ["May", "2,150,000 ₽", "+12%", "1,800,000 ₽"]
    ])
    
    table3.print()
    
    input("\n\nPress Enter to continue...")

def demo_art_and_graphs():
    """Art and graphs demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("ART & GRAPHS", color=Color.CYAN))
    print()
    
    # Banners
    print("ASCII banners:")
    print(ArtService.banner("QoLib", color=Color.RAINBOW[0]))
    print(ArtService.banner("SHOWCASE", color=Color.RAINBOW[3]))
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Text in boxes
    print("Text in boxes:")
    
    box1 = ArtService.box(
        "This is an important notification for the user.\n"
        "Here can be any important information\n"
        "that needs to be highlighted visually.",
        title="ATTENTION",
        padding=2,
        border_color=Color.YELLOW,
        title_color=Color.LIGHT_YELLOW + Color.BOLD
    )
    print(box1)
    
    print()
    
    box2 = ArtService.box(
        "Operation completed successfully!\n"
        "All data saved in the system.",
        title="SUCCESS",
        padding=1,
        border_color=Color.GREEN,
        title_color=Color.LIGHT_GREEN + Color.BOLD
    )
    print(box2)
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Graphs
    print("Bar charts:")
    
    sales_data = {
        "January": random.randint(100, 200),
        "February": random.randint(150, 250),
        "March": random.randint(200, 300),
        "April": random.randint(180, 280),
        "May": random.randint(220, 320),
        "June": random.randint(250, 350),
        "July": random.randint(230, 330),
        "August": random.randint(270, 370)
    }
    
    GraphPrinter.bar_chart(
        data=sales_data,
        width=50,
        max_height=12,
        show_values=True,
        color=Color.GREEN
    )
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Separators
    print("Different separators:")
    print(ArtService.separator(50, "=", Color.RED))
    print(ArtService.separator(50, "-", Color.GREEN))
    print(ArtService.separator(50, "~", Color.BLUE))
    print(ArtService.separator(50, "*", Color.MAGENTA))
    print(ArtService.separator(50, "#", Color.CYAN))
    
    input("\n\nPress Enter to continue...")

def demo_utilities():
    """Utilities demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("UTILITIES", color=Color.CYAN))
    print()
    
    # Terminal size
    width, height = ConsoleUtils.get_size()
    MessageService.info(f"Terminal size: {width}x{height}")
    
    # Cursor control
    print("\nCursor control:")
    print("Text 1")
    print("Text 2")
    
    ConsoleUtils.save_position()
    ConsoleUtils.move_cursor(0, ConsoleUtils.get_size()[1] - 3)
    print("This text appeared at the bottom of the screen")
    ConsoleUtils.restore_position()
    print("And we returned to the old position")
    
    # Hide/show cursor
    print("\nCursor will be hidden for 2 seconds...")
    ConsoleUtils.hide_cursor()
    time.sleep(2)
    ConsoleUtils.show_cursor()
    print("Cursor is visible again!")
    
    print("\n" + ArtService.separator(60))
    print()
    
    # Glitch effect (backward compatibility)
    print("Glitch effect:")
    printer = GlitchPrinterService()
    printer.print_glitch_line("QoLib - cool library!", delay=0.05, iterations=5)
    
    input("\n\nPress Enter to continue...")

def demo_integration():
    """Integrated demonstration"""
    ConsoleUtils.clear()
    print(ArtService.banner("INTEGRATION", color=Color.CYAN))
    print()
    
    MessageService.info("Starting integration demonstration...")
    
    # Simulate installation process
    print("\n" + ArtService.box(
        "Simulating software installation process\n"
        "using all QoLib capabilities",
        title="DEMO",
        padding=1,
        border_color=Color.CYAN
    ))
    
    print()
    
    # Step 1: System check
    MessageService.info("Step 1: System check")
    with AnimationService.spinner("Checking dependencies...") as spinner:
        time.sleep(1.5)
        spinner.update_message("Checking disk space...")
        time.sleep(1.5)
        spinner.update_message("Checking permissions...")
        time.sleep(1)
    
    # Check results table
    print("\nCheck results:")
    check_table = TablePrinter(
        ["Component", "Status", "Details"],
        column_align=["left", "center", "left"],
        border_style="simple"
    )
    
    check_table.add_rows([
        ["Python 3.7+", "✓", "3.9.0 detected"],
        ["Disk space", "✓", "15.2 GB free"],
        ["Permissions", "✓", "Access granted"],
        ["Network", "✓", "Internet available"],
        ["External dependencies", "⚠", "Update required"]
    ])
    
    check_table.print()
    
    print()
    
    # Step 2: File download
    MessageService.info("Step 2: Downloading files")
    
    files_to_download = [
        "Main components",
        "Database",
        "Documentation",
        "Code examples",
        "Test data"
    ]
    
    with AnimationService.progress_bar(
        len(files_to_download),
        "Downloading",
        bar_length=40,
        complete_char="█",
        incomplete_char="░"
    ) as bar:
        for i, file in enumerate(files_to_download):
            MessageService.pending(f"Downloading: {file}")
            # Simulate download
            time.sleep(random.uniform(0.5, 1.5))
            bar.update(i + 1)
    
    MessageService.success("All files downloaded successfully!")
    
    print()
    
    # Step 3: Installation
    MessageService.info("Step 3: Installation and configuration")
    
    AnimationService.countdown(3, "Starting installation in")
    
    steps = [
        ("Extracting files", 0.8),
        ("System configuration", 1.2),
        ("Installing components", 1.5),
        ("Creating database", 0.9),
        ("Final setup", 0.7)
    ]
    
    for step_name, duration in steps:
        MessageService.pending(step_name)
        time.sleep(duration)
    
    print()
    
    # Step 4: Results
    MessageService.info("Step 4: Installation summary")
    
    # Resource usage graph
    print("\nResource usage:")
    resource_data = {
        "CPU": 42,
        "Memory": 68,
        "Disk": 23,
        "Network": 15
    }
    
    GraphPrinter.bar_chart(
        data=resource_data,
        width=35,
        max_height=10,
        show_values=True,
        color=Color.LIGHT_BLUE
    )
    
    print()
    
    # Final message
    success_box = ArtService.box(
        "Installation completed successfully!\n\n"
        "All components were installed correctly.\n"
        "System is ready for use.",
        title="SUCCESS",
        padding=2,
        border_color=Color.GREEN,
        title_color=Color.LIGHT_GREEN + Color.BOLD + Color.BLINK
    )
    
    print(success_box)
    
    print()
    MessageService.custom("celebrate", "Demonstration completed successfully!")

def main():
    """Main demonstration function"""
    ConsoleUtils.clear()
    
    # Main banner
    print(Color.gradient("╔══════════════════════════════════════════════════╗", Color.RAINBOW))
    print(Color.gradient("║               QoLib DEMONSTRATION                ║", Color.RAINBOW))
    print(Color.gradient("║               Complete Guide v1.0                ║", Color.RAINBOW))
    print(Color.gradient("╚══════════════════════════════════════════════════╝", Color.RAINBOW))
    print()
    
    MessageService.configure(show_icons=True, show_timestamps=False)
    
    # Demo selection menu
    demos = {
        "1": ("🎨 Color System", demo_colors),
        "2": ("📝 Messages", demo_messages),
        "3": ("⏳ Animations", demo_animations),
        "4": ("📊 Tables", demo_tables),
        "5": ("🎭 Art & Graphs", demo_art_and_graphs),
        "6": ("🛠️ Utilities", demo_utilities),
        "7": ("🚀 Full Integration", demo_integration),
        "0": ("🚪 Exit", exit)
    }
    
    while True:
        print("\n" + ArtService.separator(60, "═", Color.CYAN))
        print("\nSelect demonstration:\n")
        
        for key, (name, _) in demos.items():
            print(f"  {Color.CYAN}{key}.{Color.RESET} {name}")
        
        print("\n" + ArtService.separator(60, "─", Color.GRAY))
        
        choice = input(f"\n{Color.LIGHT_CYAN}Your choice (1-7, 0 to exit): {Color.RESET}").strip()
        
        if choice in demos:
            if choice == "0":
                ConsoleUtils.clear()
                print(Color.gradient("\nThank you for using QoLib!", Color.RAINBOW))
                print(ArtService.banner("Goodbye!", color=Color.CYAN))
                break
            
            name, func = demos[choice]
            print(f"\n{Color.YELLOW}Launching: {name}{Color.RESET}")
            ConsoleUtils.wait(1)
            func()
        else:
            MessageService.error("Invalid choice. Please choose a number from 0 to 7.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Demonstration interrupted by user.{Color.RESET}")
    except Exception as e:
        MessageService.error(f"An error occurred: {e}")
