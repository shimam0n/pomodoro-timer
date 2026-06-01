import sys
import ctypes

from config import BAR_WIDTH

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def enable_ansi():
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def clear_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()


def move_up(n):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def progress_bar(elapsed, total, color):
    filled = int(BAR_WIDTH * elapsed / total)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    pct = int(100 * elapsed / total)
    return f"{color}│{bar}│ {pct:3d}%{RESET}"


def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def print_header(session, mode, total_sessions):
    tomatoes = "🍅" * total_sessions
    label = {
        "work":  f"{RED}{BOLD}  集中タイム  {RESET}",
        "short": f"{GREEN}{BOLD} 短い休憩 ☕ {RESET}",
        "long":  f"{CYAN}{BOLD} 長い休憩 🌿 {RESET}",
    }[mode]
    print(f"\n  ポモドーロタイマー  {DIM}v1.0{RESET}")
    print(f"  セッション #{session}  {label}")
    print(f"  完了: {tomatoes if tomatoes else DIM+'(まだなし)'+RESET}")
    print()
