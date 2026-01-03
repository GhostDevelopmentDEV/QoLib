import os
import sys
import time
import random
import math
import re
from enum import Enum
from typing import List, Optional, Union, Tuple, Dict, Any
from datetime import datetime
from dataclasses import dataclass

# ============================================================================
# COLOR AND STYLE SYSTEM (no external dependencies)
# ============================================================================

class ANSIColor:
    """ANSI escape sequences for colors and styles"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'
    
    # Bright text colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_DEFAULT = '\033[49m'
    
    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    
    # 256 colors
    @staticmethod
    def fg_256(color_code: int) -> str:
        return f'\033[38;5;{color_code}m'
    
    @staticmethod
    def bg_256(color_code: int) -> str:
        return f'\033[48;5;{color_code}m'
    
    # TrueColor (RGB)
    @staticmethod
    def fg_rgb(r: int, g: int, b: int) -> str:
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        return f'\033[48;2;{r};{g};{b}m'


class Color:
    """Simplified interface for working with colors"""
    
    # Basic colors
    BLACK = ANSIColor.BLACK
    RED = ANSIColor.RED
    GREEN = ANSIColor.GREEN
    YELLOW = ANSIColor.YELLOW
    BLUE = ANSIColor.BLUE
    MAGENTA = ANSIColor.MAGENTA
    CYAN = ANSIColor.CYAN
    WHITE = ANSIColor.WHITE
    
    # Bright versions
    GRAY = ANSIColor.BRIGHT_BLACK
    LIGHT_RED = ANSIColor.BRIGHT_RED
    LIGHT_GREEN = ANSIColor.BRIGHT_GREEN
    LIGHT_YELLOW = ANSIColor.BRIGHT_YELLOW
    LIGHT_BLUE = ANSIColor.BRIGHT_BLUE
    LIGHT_MAGENTA = ANSIColor.BRIGHT_MAGENTA
    LIGHT_CYAN = ANSIColor.BRIGHT_CYAN
    LIGHT_WHITE = ANSIColor.BRIGHT_WHITE
    
    # Styles
    RESET = ANSIColor.RESET
    BOLD = ANSIColor.BOLD
    DIM = ANSIColor.DIM
    ITALIC = ANSIColor.ITALIC
    UNDERLINE = ANSIColor.UNDERLINE
    BLINK = ANSIColor.BLINK
    
    # Color palettes
    RAINBOW = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
    PASTEL = [
        ANSIColor.fg_rgb(255, 179, 186),  # pastel pink
        ANSIColor.fg_rgb(255, 223, 186),  # pastel peach
        ANSIColor.fg_rgb(255, 255, 186),  # pastel yellow
        ANSIColor.fg_rgb(186, 255, 201),  # pastel green
        ANSIColor.fg_rgb(186, 225, 255),  # pastel blue
        ANSIColor.fg_rgb(225, 186, 255),  # pastel purple
    ]
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert HEX to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c*2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def fg_hex(hex_color: str) -> str:
        """Text color from HEX"""
        r, g, b = Color.hex_to_rgb(hex_color)
        return ANSIColor.fg_rgb(r, g, b)
    
    @staticmethod
    def bg_hex(hex_color: str) -> str:
        """Background color from HEX"""
        r, g, b = Color.hex_to_rgb(hex_color)
        return ANSIColor.bg_rgb(r, g, b)
    
    @staticmethod
    def gradient(text: str, colors: List[str]) -> str:
        """Gradient text"""
        if not colors:
            return text
        
        result = []
        step = len(text) / (len(colors) - 1) if len(colors) > 1 else 1
        
        for i, char in enumerate(text):
            if char == ' ':
                result.append(char)
                continue
                
            color_idx = min(int(i / step), len(colors) - 1)
            next_idx = min(color_idx + 1, len(colors) - 1)
            
            # Interpolation between colors
            if color_idx == next_idx:
                result.append(f"{colors[color_idx]}{char}")
            else:
                pos = (i % step) / step
                result.append(f"{colors[color_idx]}{char}")
        
        return ''.join(result) + Color.RESET
    
    @staticmethod
    def strip_colors(text: str) -> str:
        """Remove all ANSI escape sequences from text"""
        return re.sub(r'\033\[[0-9;]*m', '', text)


@dataclass
class MessageStyle:
    """Style for messages"""
    prefix: str
    color: str
    style: str = ""
    icon: str = ""
    timestamp: bool = False
    indent: int = 0


class MessageType(Enum):
    """Message types"""
    INFO = "info"
    INFO2 = "info2"
    PENDING = "pending"
    SUCCESS = "success"
    SUCCESS2 = "success2"
    ERROR = "error"
    WARNING = "warning"
    QUESTION = "question"
    DEBUG = "debug"
    CUSTOM = "custom"


# ============================================================================
# MAIN LIBRARY CLASSES
# ============================================================================

class MessageService:
    """Service for outputting styled messages"""
    
    # Standard styles
    _STYLES = {
        MessageType.INFO: MessageStyle(
            prefix="[+]",
            color=Color.WHITE,
            icon="ℹ"
        ),
        MessageType.INFO2: MessageStyle(
            prefix="[#]",
            color=Color.LIGHT_BLUE,
            icon="🛈"
        ),
        MessageType.PENDING: MessageStyle(
            prefix="[...]",
            color=Color.GRAY,
            icon="⌛"
        ),
        MessageType.SUCCESS: MessageStyle(
            prefix="[✓]",
            color=Color.LIGHT_GREEN,
            icon="✅",
            style=Color.BOLD
        ),
        MessageType.SUCCESS2: MessageStyle(
            prefix="[✓]",
            color=Color.LIGHT_BLUE,
            icon="✅"
        ),
        MessageType.ERROR: MessageStyle(
            prefix="[-]",
            color=Color.LIGHT_RED,
            icon="❌",
            style=Color.BOLD
        ),
        MessageType.WARNING: MessageStyle(
            prefix="[!]",
            color=Color.LIGHT_YELLOW,
            icon="⚠",
            style=Color.BOLD
        ),
        MessageType.QUESTION: MessageStyle(
            prefix="[?]",
            color=Color.LIGHT_MAGENTA,
            icon="❓"
        ),
        MessageType.DEBUG: MessageStyle(
            prefix="[DEBUG]",
            color=Color.LIGHT_CYAN,
            icon="🐛"
        ),
    }
    
    _custom_styles: Dict[str, MessageStyle] = {}
    _show_icons: bool = True
    _show_timestamps: bool = False
    _timestamp_format: str = "%H:%M:%S"
    
    @classmethod
    def configure(cls,
                  show_icons: bool = None,
                  show_timestamps: bool = None,
                  timestamp_format: str = None) -> None:
        """Configure the message service"""
        if show_icons is not None:
            cls._show_icons = show_icons
        if show_timestamps is not None:
            cls._show_timestamps = show_timestamps
        if timestamp_format is not None:
            cls._timestamp_format = timestamp_format
    
    @classmethod
    def register_style(cls,
                      name: str,
                      prefix: str,
                      color: str,
                      style: str = "",
                      icon: str = "") -> None:
        """Register a custom style"""
        cls._custom_styles[name] = MessageStyle(
            prefix=prefix,
            color=color,
            style=style,
            icon=icon
        )
    
    @classmethod
    def print(cls,
              message_type: Union[MessageType, str],
              text: str,
              end: str = "\n",
              indent: int = 0,
              flush: bool = False) -> None:
        """Universal method for outputting messages"""
        
        # Get style
        if isinstance(message_type, MessageType):
            style = cls._STYLES.get(message_type)
        else:
            style = cls._custom_styles.get(message_type)
        
        if not style:
            style = cls._STYLES[MessageType.INFO]
        
        # Prepare prefix
        prefix_parts = []
        
        if cls._show_timestamps:
            time_str = datetime.now().strftime(cls._timestamp_format)
            prefix_parts.append(f"{Color.DIM}{time_str}{Color.RESET}")
        
        if cls._show_icons and style.icon:
            prefix_parts.append(f"{style.color}{style.style}{style.icon}{Color.RESET}")
        
        prefix_parts.append(f"{style.color}{style.style}{style.prefix}{Color.RESET}")
        
        prefix = " ".join(prefix_parts)
        
        # Form indentation
        indent_str = " " * (style.indent + indent)
        
        # Output
        full_text = f"{indent_str}{prefix} {style.color}{text}{Color.RESET}"
        print(full_text, end=end, flush=flush)
    
    # Quick methods
    @classmethod
    def info(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.INFO, text, **kwargs)
    
    @classmethod
    def info2(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.INFO2, text, **kwargs)
    
    @classmethod
    def pending(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.PENDING, text, **kwargs)
    
    @classmethod
    def success(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.SUCCESS, text, **kwargs)
    
    @classmethod
    def success2(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.SUCCESS2, text, **kwargs)
    
    @classmethod
    def error(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.ERROR, text, **kwargs)
    
    @classmethod
    def warning(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.WARNING, text, **kwargs)
    
    @classmethod
    def question(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.QUESTION, text, **kwargs)
    
    @classmethod
    def debug(cls, text: str, **kwargs) -> None:
        cls.print(MessageType.DEBUG, text, **kwargs)
    
    @classmethod
    def custom(cls, name: str, text: str, **kwargs) -> None:
        cls.print(name, text, **kwargs)


class AnimationService:
    """Service for animations and progress indicators"""
    
    @staticmethod
    def spinner(message: str = "",
                delay: float = 0.1,
                frames: List[str] = None) -> 'Spinner':
        """Create a spinner (loading indicator)"""
        return Spinner(message, delay, frames)
    
    @staticmethod
    def progress_bar(total: int,
                     description: str = "",
                     bar_length: int = 50,
                     complete_char: str = "█",
                     incomplete_char: str = "░",
                     show_percentage: bool = True,
                     show_counter: bool = True) -> 'ProgressBar':
        """Create a progress bar"""
        return ProgressBar(total, description, bar_length, complete_char,
                          incomplete_char, show_percentage, show_counter)
    
    @staticmethod
    def countdown(seconds: int,
                  message: str = "Waiting",
                  end_message: str = "Ready!") -> None:
        """Countdown timer"""
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{message}: {Color.YELLOW}{i}{Color.RESET} sec.   ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f"\r{end_message}{' ' * 20}\n")
        sys.stdout.flush()
    
    @staticmethod
    def typing_effect(text: str,
                      speed: float = 0.05,
                      color: str = Color.WHITE,
                      pause_chars: str = ".!?",
                      pause_duration: float = 0.3) -> None:
        """Typing effect with pauses on punctuation"""
        for char in text:
            sys.stdout.write(color + char + Color.RESET)
            sys.stdout.flush()
            
            if char in pause_chars:
                time.sleep(pause_duration)
            else:
                time.sleep(speed)
        
        print()


class Spinner:
    """Animated spinner"""
    
    DEFAULT_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self,
                 message: str = "",
                 delay: float = 0.1,
                 frames: List[str] = None):
        self.message = message
        self.delay = delay
        self.frames = frames or self.DEFAULT_FRAMES
        self._running = False
        self._current_frame = 0
    
    def start(self):
        """Start the spinner"""
        self._running = True
        self._current_frame = 0
        
        def spin():
            while self._running:
                frame = self.frames[self._current_frame % len(self.frames)]
                sys.stdout.write(f"\r{frame} {self.message}")
                sys.stdout.flush()
                self._current_frame += 1
                time.sleep(self.delay)
        
        import threading
        self._thread = threading.Thread(target=spin, daemon=True)
        self._thread.start()
    
    def stop(self, final_message: str = ""):
        """Stop the spinner"""
        self._running = False
        if hasattr(self, '_thread'):
            self._thread.join(timeout=0.1)
        
        # Clear the line
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        if final_message:
            print(final_message)
        sys.stdout.flush()
    
    def update_message(self, new_message: str):
        """Update spinner message"""
        self.message = new_message
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class ProgressBar:
    """Progress bar with context manager support"""
    
    def __init__(self,
                 total: int,
                 description: str = "",
                 bar_length: int = 50,
                 complete_char: str = "█",
                 incomplete_char: str = "░",
                 show_percentage: bool = True,
                 show_counter: bool = True):
        self.total = total
        self.current = 0
        self.description = description
        self.bar_length = bar_length
        self.complete_char = complete_char
        self.incomplete_char = incomplete_char
        self.show_percentage = show_percentage
        self.show_counter = show_counter
        self.start_time = time.time()
    
    def update(self, value: int = None, increment: int = 1):
        """Update progress"""
        if value is not None:
            self.current = min(value, self.total)
        else:
            self.current = min(self.current + increment, self.total)
        
        self._render()
    
    def _render(self):
        """Render the progress bar"""
        progress = self.current / self.total
        filled_length = int(self.bar_length * progress)
        
        # Bar
        bar = self.complete_char * filled_length + \
              self.incomplete_char * (self.bar_length - filled_length)
        
        # Percentage
        percentage = f"{progress * 100:.1f}%" if self.show_percentage else ""
        
        # Counter
        counter = f"{self.current}/{self.total}" if self.show_counter else ""
        
        # Time
        elapsed = time.time() - self.start_time
        if self.current > 0 and progress < 1:
            remaining = (elapsed / progress) * (1 - progress)
            time_str = f" [{elapsed:.0f}<{remaining:.0f}s]"
        elif progress >= 1:
            time_str = f" [{elapsed:.1f}s]"
        else:
            time_str = ""
        
        # Build string
        parts = []
        if self.description:
            parts.append(self.description)
        
        parts.append(f"[{bar}]")
        
        if percentage:
            parts.append(percentage)
        
        if counter:
            parts.append(counter)
        
        parts.append(time_str)
        
        line = " ".join(parts)
        
        # Output
        sys.stdout.write(f"\r{line}")
        sys.stdout.flush()
    
    def finish(self):
        """Finish the progress bar"""
        self.update(self.total)
        print()
    
    def __enter__(self):
        self.update(0)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()


class TablePrinter:
    """Print beautiful tables"""
    
    def __init__(self,
                 headers: List[str],
                 column_align: List[str] = None,
                 padding: int = 1,
                 border_style: str = "rounded",
                 header_color: str = Color.CYAN + Color.BOLD,
                 zebra_stripes: bool = False,
                 stripe_color: str = Color.DIM):
        
        self.headers = headers
        self.rows = []
        self.column_align = column_align or ["left"] * len(headers)
        self.padding = padding
        self.border_style = border_style
        self.header_color = header_color
        self.zebra_stripes = zebra_stripes
        self.stripe_color = stripe_color
        
        # Border styles
        self._border_styles = {
            "rounded": {
                "top_left": "╭",
                "top_right": "╮",
                "bottom_left": "╰",
                "bottom_right": "╯",
                "horizontal": "─",
                "vertical": "│",
                "cross": "┼",
                "top_cross": "┬",
                "bottom_cross": "┴",
                "left_cross": "├",
                "right_cross": "┤"
            },
            "double": {
                "top_left": "╔",
                "top_right": "╗",
                "bottom_left": "╚",
                "bottom_right": "╝",
                "horizontal": "═",
                "vertical": "║",
                "cross": "╬",
                "top_cross": "╦",
                "bottom_cross": "╩",
                "left_cross": "╠",
                "right_cross": "╣"
            },
            "simple": {
                "top_left": "┌",
                "top_right": "┐",
                "bottom_left": "└",
                "bottom_right": "┘",
                "horizontal": "─",
                "vertical": "│",
                "cross": "┼",
                "top_cross": "┬",
                "bottom_cross": "┴",
                "left_cross": "├",
                "right_cross": "┤"
            },
            "plain": {
                "top_left": "",
                "top_right": "",
                "bottom_left": "",
                "bottom_right": "",
                "horizontal": "",
                "vertical": " ",
                "cross": "",
                "top_cross": "",
                "bottom_cross": "",
                "left_cross": "",
                "right_cross": ""
            }
        }
    
    def add_row(self, row: List[Any]):
        """Add a row to the table"""
        self.rows.append(row)
    
    def add_rows(self, rows: List[List[Any]]):
        """Add multiple rows"""
        self.rows.extend(rows)
    
    def print(self):
        """Print the table"""
        # Determine column widths
        col_widths = []
        for i in range(len(self.headers)):
            max_width = len(str(self.headers[i]))
            for row in self.rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width + self.padding * 2)
        
        border = self._border_styles.get(self.border_style, 
                                        self._border_styles["simple"])
        
        # Top border
        if border["top_left"]:
            top_border = border["top_left"]
            for i, width in enumerate(col_widths):
                top_border += border["horizontal"] * width
                if i < len(col_widths) - 1:
                    top_border += border["top_cross"]
            top_border += border["top_right"]
            print(top_border)
        
        # Headers
        if border["vertical"]:
            header_line = border["vertical"]
        else:
            header_line = ""
            
        for i, header in enumerate(self.headers):
            width = col_widths[i] - self.padding * 2
            align = self.column_align[i]
            
            if align == "center":
                formatted = str(header).center(width)
            elif align == "right":
                formatted = str(header).rjust(width)
            else:
                formatted = str(header).ljust(width)
            
            header_line += " " * self.padding + \
                         self.header_color + formatted + Color.RESET + \
                         " " * self.padding
            
            if border["vertical"]:
                header_line += border["vertical"]
        
        print(header_line)
        
        # Separator
        if border["left_cross"]:
            separator = border["left_cross"]
            for i, width in enumerate(col_widths):
                separator += border["horizontal"] * width
                if i < len(col_widths) - 1:
                    separator += border["cross"]
            separator += border["right_cross"]
            print(separator)
        
        # Data rows
        for row_idx, row in enumerate(self.rows):
            if border["vertical"]:
                row_line = border["vertical"]
            else:
                row_line = ""
            
            # Stripe colors
            row_color = ""
            if self.zebra_stripes and row_idx % 2 == 1:
                row_color = self.stripe_color
            
            for i, cell in enumerate(row):
                width = col_widths[i] - self.padding * 2
                align = self.column_align[i]
                cell_str = str(cell) if cell is not None else ""
                
                if align == "center":
                    formatted = cell_str.center(width)
                elif align == "right":
                    formatted = cell_str.rjust(width)
                else:
                    formatted = cell_str.ljust(width)
                
                row_line += " " * self.padding + \
                          row_color + formatted + Color.RESET + \
                          " " * self.padding
                
                if border["vertical"]:
                    row_line += border["vertical"]
            
            print(row_line)
        
        # Bottom border
        if border["bottom_left"]:
            bottom_border = border["bottom_left"]
            for i, width in enumerate(col_widths):
                bottom_border += border["horizontal"] * width
                if i < len(col_widths) - 1:
                    bottom_border += border["bottom_cross"]
            bottom_border += border["bottom_right"]
            print(bottom_border)


class GraphPrinter:
    """Print graphs and charts in console"""
    
    @staticmethod
    def bar_chart(data: Dict[str, float],
                  width: int = 50,
                  max_height: int = 10,
                  show_values: bool = True,
                  color: str = Color.CYAN):
        """Bar chart"""
        
        if not data:
            return
        
        max_value = max(data.values())
        min_value = min(data.values())
        
        # Normalize data
        normalized = {}
        for key, value in data.items():
            if max_value == min_value:
                normalized[key] = max_height
            else:
                normalized[key] = int((value - min_value) / 
                                    (max_value - min_value) * max_height)
        
        # Build chart
        for key, height in normalized.items():
            bar = color + "█" * height + Color.RESET
            value_str = f" ({data[key]})" if show_values else ""
            print(f"{key.ljust(15)} {bar} {value_str}")


class ArtService:
    """Service for ASCII art and decorations"""
    
    @staticmethod
    def banner(text: str,
               font: str = "simple",
               color: str = Color.CYAN,
               width: int = None) -> str:
        """Create ASCII banner"""
        
        fonts = {
            "simple": {
                'A': " █████╗ ", 'B': "██████╗ ", 'C': " ██████╗", 'D': "██████╗ ",
                'E': "███████╗", 'F': "███████╗", 'G': " ██████╗ ", 'H': "██╗  ██╗",
                'I': "██╗", 'J': "     ██╗", 'K': "██╗  ██╗", 'L': "██╗     ",
                'M': "███╗   ███╗", 'N': "███╗   ██╗", 'O': " ██████╗ ", 'P': "██████╗ ",
                'Q': " ██████╗ ", 'R': "██████╗ ", 'S': " ███████╗", 'T': "████████╗",
                'U': "██╗   ██╗", 'V': "██╗   ██╗", 'W': "██╗    ██╗██╗", 'X': "██╗  ██╗",
                'Y': "██╗   ██╗", 'Z': "███████╗",
                ' ': "   ", '0': " ██████╗ ", '1': " ██╗", '2': "██████╗ ",
                '3': "██████╗ ", '4': "██╗  ██╗", '5': "███████╗", '6': " ██████╗ ",
                '7': "███████╗", '8': " █████╗ ", '9': " ██████╗ ",
                '!': "██╗", '?': " ██████╗", '.': "    ", ',': "    ",
                ':': "    ", ';': "    ", '-': "       ", '_': "       "
            }
        }
        
        selected_font = fonts.get(font, fonts["simple"])
        
        # Create banner
        lines = [""] * 3  # For simple font height 3 lines
        
        for char in text.upper():
            for i in range(3):
                if char in selected_font:
                    lines[i] += selected_font[char]
                else:
                    lines[i] += selected_font.get(' ', "   ")
        
        # Apply color
        result = []
        for line in lines:
            result.append(color + line + Color.RESET)
        
        return "\n".join(result)
    
    @staticmethod
    def separator(length: int = 60,
                  char: str = "═",
                  color: str = Color.GRAY) -> str:
        """Create separator line"""
        return color + char * length + Color.RESET
    
    @staticmethod
    def box(text: str,
            title: str = "",
            padding: int = 1,
            border_color: str = Color.CYAN,
            title_color: str = Color.CYAN + Color.BOLD) -> str:
        """Text in a box with optional title"""
        
        lines = text.split('\n')
        max_len = max(len(Color.strip_colors(line)) for line in lines)
        
        # Top border
        if title:
            top_border = border_color + "╭─ " + title_color + title + \
                        border_color + " " + "─" * (max_len - len(title) + padding * 2) + "╮"
        else:
            top_border = border_color + "╭" + "─" * (max_len + padding * 2 + 2) + "╮"
        
        # Text lines
        content = []
        for line in lines:
            clean_len = len(Color.strip_colors(line))
            padding_right = max_len - clean_len
            content.append(border_color + "│" + " " * padding + line + 
                         " " * (padding + padding_right) + border_color + "│")
        
        # Bottom border
        bottom_border = border_color + "╰" + "─" * (max_len + padding * 2 + 2) + "╯"
        
        return "\n".join([top_border] + content + [bottom_border]) + Color.RESET


# ============================================================================
# UTILITIES AND COMPATIBILITY
# ============================================================================

class ConsoleUtils:
    """Console utilities"""
    
    @staticmethod
    def clear():
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def wait(seconds: float):
        """Pause"""
        time.sleep(seconds)
    
    @staticmethod
    def get_size() -> Tuple[int, int]:
        """Get terminal size"""
        try:
            return os.get_terminal_size()
        except:
            return (80, 24)
    
    @staticmethod
    def hide_cursor():
        """Hide cursor"""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
    
    @staticmethod
    def show_cursor():
        """Show cursor"""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
    
    @staticmethod
    def move_cursor(x: int, y: int):
        """Move cursor"""
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()
    
    @staticmethod
    def save_position():
        """Save cursor position"""
        sys.stdout.write("\033[s")
        sys.stdout.flush()
    
    @staticmethod
    def restore_position():
        """Restore cursor position"""
        sys.stdout.write("\033[u")
        sys.stdout.flush()


class GlitchPrinterService:
    """Service for glitch effects (for backward compatibility)"""
    
    def __init__(self):
        self.glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/\\~`"
    
    def clear_line(self, length: int = 100):
        """Clear line"""
        sys.stdout.write('\r' + ' ' * length + '\r')
        sys.stdout.flush()
    
    def print_glitch_line(self, text, delay=0.03, iterations=3):
        """Glitch effect"""
        for i in range(len(text) + 1):
            for _ in range(iterations):
                line = []
                for j in range(len(text)):
                    if j < i:
                        line.append(text[j])
                    else:
                        if text[j] == ' ':
                            line.append(' ')
                        else:
                            line.append(random.choice(self.glitch_chars))
                
                sys.stdout.write('\r' + ''.join(line))
                sys.stdout.flush()
                time.sleep(delay/iterations)
        
        sys.stdout.write('\r' + text + '\n')
        sys.stdout.flush()


# Aliases for backward compatibility
OtherFuncs = ConsoleUtils


# ============================================================================
# QUICK ACCESS FUNCTIONS
# ============================================================================

# Quick color functions
def red(text: str) -> str:
    """Return text in red color"""
    return Color.RED + text + Color.RESET

def green(text: str) -> str:
    """Return text in green color"""
    return Color.GREEN + text + Color.RESET

def blue(text: str) -> str:
    """Return text in blue color"""
    return Color.BLUE + text + Color.RESET

def yellow(text: str) -> str:
    """Return text in yellow color"""
    return Color.YELLOW + text + Color.RESET

def cyan(text: str) -> str:
    """Return text in cyan color"""
    return Color.CYAN + text + Color.RESET

def magenta(text: str) -> str:
    """Return text in magenta color"""
    return Color.MAGENTA + text + Color.RESET

def bold(text: str) -> str:
    """Return text in bold style"""
    return Color.BOLD + text + Color.RESET

def underline(text: str) -> str:
    """Return text with underline"""
    return Color.UNDERLINE + text + Color.RESET

# Quick message functions
def info(text: str, **kwargs) -> None:
    """Quick info message"""
    MessageService.info(text, **kwargs)

def success(text: str, **kwargs) -> None:
    """Quick success message"""
    MessageService.success(text, **kwargs)

def warning(text: str, **kwargs) -> None:
    """Quick warning message"""
    MessageService.warning(text, **kwargs)

def error(text: str, **kwargs) -> None:
    """Quick error message"""
    MessageService.error(text, **kwargs)

# Export main classes and functions
__all__ = [
    # Color system
    'ANSIColor',
    'Color',
    'MessageStyle',
    'MessageType',
    
    # Main services
    'MessageService',
    'AnimationService',
    'Spinner',
    'ProgressBar',
    'TablePrinter',
    'GraphPrinter',
    'ArtService',
    'ConsoleUtils',
    'GlitchPrinterService',
    'OtherFuncs',
    
    # Quick functions
    'red',
    'green',
    'blue',
    'yellow',
    'cyan',
    'magenta',
    'bold',
    'underline',
    'info',
    'success',
    'warning',
    'error',
]
