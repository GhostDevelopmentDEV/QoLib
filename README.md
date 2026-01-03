# QoLib - Beautiful Console Output Library for Python

![Banner](https://img.shields.io/badge/QoLib-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

**QoLib** is a powerful yet lightweight Python library for creating beautiful console interfaces. Completely independent of external libraries, using only ANSI escape sequences.

## ✨ Features

- 🎨 **Complete Independence** - No external dependencies required
- 🚀 **Rich Color Palette** - 16 basic colors, 256 colors, RGB and HEX support
- 📊 **Multiple Widgets** - Tables, progress bars, spinners, graphs
- 🎭 **Animations & Effects** - Glitches, typewriter effect, gradients
- 📝 **Styled Messages** - Ready-made templates for logs
- 🎯 **Flexible Configuration** - Easy to customize for your needs
- 📱 **Adaptive** - Automatic terminal size detection

## 📦 Installation

Simply copy the `qolib.py` file to your project:

```python
from qolib import MessageService, Color, AnimationService
```

## 🚀 Quick Start

```python
from qolib import MessageService, Color

# Quick messages
MessageService.success("Operation completed successfully!")
MessageService.warning("Warning: check settings")
MessageService.error("An error occurred!")

# Colored text
print(Color.RED + "Red text" + Color.RESET)
print(Color.gradient("Rainbow text", Color.RAINBOW))

# Data tables
from qolib import TablePrinter
table = TablePrinter(["Name", "Age", "City"])
table.add_row(["Anna", 25, "Moscow"])
table.add_row(["Ivan", 30, "St. Petersburg"])
table.print()
```

## 📚 Documentation

### 🎨 Color System

The library provides a complete color system without dependencies:

```python
from qolib import Color

# Basic colors
print(Color.RED + "Red" + Color.RESET)
print(Color.GREEN + "Green" + Color.RESET)
print(Color.BLUE + "Blue" + Color.RESET)

# Bright colors
print(Color.LIGHT_RED + "Bright red" + Color.RESET)
print(Color.LIGHT_GREEN + "Bright green" + Color.RESET)

# RGB colors
rgb_text = Color.fg_rgb(255, 105, 180) + "Pink" + Color.RESET

# HEX colors
hex_text = Color.fg_hex("#FF5733") + "Orange" + Color.RESET

# Gradients
gradient = Color.gradient("Rainbow text", Color.RAINBOW)

# Styles
print(Color.BOLD + "Bold" + Color.RESET)
print(Color.UNDERLINE + "Underlined" + Color.RESET)
print(Color.ITALIC + "Italic" + Color.RESET)

# Palettes
print(Color.PASTEL[0] + "Pastel pink" + Color.RESET)
```

**Available colors:**
- `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`
- `GRAY`, `LIGHT_RED`, `LIGHT_GREEN`, `LIGHT_YELLOW`, `LIGHT_BLUE`, `LIGHT_MAGENTA`, `LIGHT_CYAN`, `LIGHT_WHITE`
- `RAINBOW`, `PASTEL` - color arrays for gradients

### 📝 MessageService

Service for outputting styled messages:

```python
from qolib import MessageService, MessageType

# Quick methods
MessageService.info("Information")
MessageService.success("Success!")
MessageService.warning("Warning")
MessageService.error("Error")
MessageService.pending("In progress...")
MessageService.question("Question?")
MessageService.debug("Debug")

# Universal method
MessageService.print(MessageType.SUCCESS, "Message text")

# Configuration
MessageService.configure(
    show_icons=True,          # Show icons
    show_timestamps=True,     # Show timestamps
    timestamp_format="%H:%M:%S"  # Time format
)

# Custom styles
MessageService.register_style(
    name="important",
    prefix="[IMPORTANT]",
    color=Color.LIGHT_RED + Color.BOLD,
    icon="⚡"
)
MessageService.custom("important", "Important message!")
```

### ⏳ AnimationService

Animations and progress indicators:

```python
from qolib import AnimationService

# Spinner (loading indicator)
with AnimationService.spinner("Loading...") as spinner:
    # Your code
    time.sleep(3)
    spinner.update_message("Processing...")
    time.sleep(2)

# Progress bar
with AnimationService.progress_bar(100, "Processing files") as bar:
    for i in range(100):
        bar.update()  # or bar.update(value=i)
        time.sleep(0.05)

# Countdown
AnimationService.countdown(5, "Starting in")

# Typewriter effect
AnimationService.typing_effect("Hello, world!", speed=0.05)
```

### 📊 TablePrinter

Beautiful tables with different style support:

```python
from qolib import TablePrinter

table = TablePrinter(
    headers=["Name", "Age", "City"],
    column_align=["left", "center", "left"],  # left|center|right
    border_style="rounded",  # rounded, double, simple, plain
    header_color=Color.CYAN + Color.BOLD,
    zebra_stripes=True,
    stripe_color=Color.DIM
)

table.add_row(["Anna", 25, "Moscow"])
table.add_row(["Ivan", 30, "St. Petersburg"])
table.add_row(["Maria", 22, "Kazan"])

table.print()
```

### 🎨 ArtService

Decorations and ASCII art:

```python
from qolib import ArtService

# Banner
print(ArtService.banner("My Project", font="simple", color=Color.CYAN))

# Separators
print(ArtService.separator(50, char="═", color=Color.GRAY))

# Text in box
box = ArtService.box(
    "This is an important message\nin a beautiful box",
    title="Notification",
    padding=2,
    border_color=Color.YELLOW,
    title_color=Color.LIGHT_YELLOW
)
print(box)
```

### 📈 GraphPrinter

Simple console graphs:

```python
from qolib import GraphPrinter

data = {
    "January": 150,
    "February": 220,
    "March": 180,
    "April": 300,
    "May": 270
}

GraphPrinter.bar_chart(
    data=data,
    width=40,
    max_height=10,
    show_values=True,
    color=Color.GREEN
)
```

### 🛠️ ConsoleUtils

Console utilities:

```python
from qolib import ConsoleUtils

ConsoleUtils.clear()           # Clear console
ConsoleUtils.wait(1.5)         # Pause for 1.5 seconds
width, height = ConsoleUtils.get_size()  # Terminal size
ConsoleUtils.hide_cursor()     # Hide cursor
ConsoleUtils.show_cursor()     # Show cursor
ConsoleUtils.move_cursor(10, 5)  # Move cursor
ConsoleUtils.save_position()   # Save cursor position
ConsoleUtils.restore_position()  # Restore cursor position
```

### ⚡ GlitchPrinterService (for backward compatibility)

Glitch effects:

```python
from qolib import GlitchPrinterService

printer = GlitchPrinterService()
printer.print_glitch_line("Text with glitch effect", delay=0.05, iterations=5)
```

### 🎭 Additional Features

#### Gradient text:
```python
text = Color.gradient(
    "This text has gradient coloring",
    [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA]
)
print(text)
```

#### Remove colors from text:
```python
colored = Color.RED + "Text" + Color.GREEN + " with colors" + Color.RESET
clean = Color.strip_colors(colored)  # "Text with colors"
```

#### Create progress bar manually:
```python
from qolib import ProgressBar

bar = ProgressBar(total=100, description="Loading")
for i in range(101):
    bar.update(i)
    time.sleep(0.05)
bar.finish()
```

## 🎯 Usage Examples

### Application logger:
```python
from qolib import MessageService

class AppLogger:
    def __init__(self):
        MessageService.configure(show_timestamps=True)
    
    def start(self):
        MessageService.info("Starting application...")
    
    def process(self, item):
        MessageService.pending(f"Processing: {item}")
    
    def success(self, message):
        MessageService.success(f"Done: {message}")
    
    def error(self, error):
        MessageService.error(f"Error: {error}")
```

### Download interface:
```python
from qolib import AnimationService, MessageService

def download_files(urls):
    MessageService.info(f"Starting download of {len(urls)} files")
    
    with AnimationService.progress_bar(len(urls), "Downloading") as bar:
        for i, url in enumerate(urls):
            MessageService.pending(f"Downloading: {url}")
            # Download code...
            bar.update(i + 1)
    
    MessageService.success("All files downloaded!")
```

### Report in table:
```python
from qolib import TablePrinter, Color

def generate_report(data):
    table = TablePrinter(
        ["Metric", "Value", "Status"],
        column_align=["left", "right", "center"],
        zebra_stripes=True
    )
    
    for item in data:
        status_color = Color.GREEN if item["ok"] else Color.RED
        status = status_color + ("✓" if item["ok"] else "✗") + Color.RESET
        table.add_row([item["name"], item["value"], status])
    
    table.print()
```

## 🔧 Terminal Configuration

For correct color display, ensure your terminal supports ANSI escape sequences:

- **Linux/macOS**: Supported by default
- **Windows 10+**: Supported in PowerShell and Windows Terminal
- **Older Windows**: May require ANSI support activation

## ⚠️ Limitations

1. Older Windows versions may not support all colors
2. Some effects (e.g., BLINK) may not work in all terminals
3. Correct terminal size detection requires OS support

**QoLib** - Making console applications beautiful! ✨

You can immediately use the library in your projects or show the demonstration for learning purposes!
