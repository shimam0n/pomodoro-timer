import time
import sys
import os
import msvcrt

# ── ANSI colors (Windows 10+ supports these) ──────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ── Settings ──────────────────────────────────────────────────────────────────
WORK_MINUTES   = 25
SHORT_BREAK    = 5
LONG_BREAK     = 15
SESSIONS_UNTIL_LONG = 4
BAR_WIDTH      = 40

def enable_ansi():
    """Enable ANSI escape codes on Windows."""
    import ctypes
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

def check_key():
    """Non-blocking key check. Returns char or None."""
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):  # special keys — consume next byte
            msvcrt.getch()
            return None
        return ch.decode('utf-8', errors='ignore').lower()
    return None

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

def run_timer(duration_min, mode, session, total_sessions):
    duration = duration_min * 60
    color = RED if mode == "work" else (GREEN if mode == "short" else CYAN)
    label = "残り時間"

    hide_cursor()
    os.system("cls")
    print_header(session, mode, total_sessions)

    # Print 2 lines we'll update in-place
    print(f"  {label}: {fmt_time(duration)}")
    print(f"  {progress_bar(0, duration, color)}")
    print(f"\n  {DIM}[s] スキップ  [q] 終了{RESET}")

    start = time.time()
    try:
        while True:
            elapsed = time.time() - start
            if elapsed >= duration:
                elapsed = duration

            remaining = duration - elapsed

            # Update the 2 lines (move up, overwrite)
            move_up(3)
            clear_line()
            print(f"  {label}: {color}{BOLD}{fmt_time(remaining)}{RESET}")
            clear_line()
            print(f"  {progress_bar(elapsed, duration, color)}")
            sys.stdout.flush()

            if elapsed >= duration:
                return "done"

            key = check_key()
            if key == 'q':
                return "quit"
            if key == 's':
                return "skip"

            time.sleep(0.25)
    finally:
        show_cursor()

def notify(mode):
    """Simple bell notification."""
    for _ in range(3 if mode == "work" else 1):
        print("\a", end="", flush=True)
        time.sleep(0.2)

def main():
    enable_ansi()
    session = 1
    total_sessions = 0   # completed work sessions

    print(f"\n{BOLD}  ポモドーロタイマーへようこそ！{RESET}")
    print(f"  {WORK_MINUTES}分集中 → {SHORT_BREAK}分休憩 ({SESSIONS_UNTIL_LONG}回ごとに{LONG_BREAK}分の長休憩)")
    print(f"\n  {DIM}Enterキーで開始...{RESET}")
    input()

    while True:
        # ── Work session ──────────────────────────────────────────────────────
        result = run_timer(WORK_MINUTES, "work", session, total_sessions)
        if result == "quit":
            break
        if result == "done":
            total_sessions += 1
            notify("work")

        os.system("cls")
        if result == "skip":
            print(f"\n  {YELLOW}セッション #{session} をスキップしました。{RESET}")
        else:
            print(f"\n  {GREEN}{BOLD}セッション #{session} 完了！🍅{RESET}")

        # ── Break ─────────────────────────────────────────────────────────────
        if total_sessions % SESSIONS_UNTIL_LONG == 0 and total_sessions > 0:
            break_mode = "long"
            break_min  = LONG_BREAK
            print(f"  {CYAN}お疲れ様でした！{LONG_BREAK}分の長い休憩を取りましょう。{RESET}")
        else:
            break_mode = "short"
            break_min  = SHORT_BREAK
            print(f"  {GREEN}{SHORT_BREAK}分の休憩を取りましょう。{RESET}")

        print(f"\n  {DIM}Enterキーで休憩を開始...{RESET}")
        # Wait for Enter or 'q'
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b'q':
                    show_cursor()
                    sys.exit(0)
                if ch == b'\r':
                    break

        result = run_timer(break_min, break_mode, session, total_sessions)
        if result == "quit":
            break

        notify("break")
        session += 1

    os.system("cls")
    print(f"\n  {BOLD}お疲れ様でした！{RESET}")
    print(f"  完了したセッション: {total_sessions} 🍅")
    if total_sessions > 0:
        print(f"  集中した時間: {total_sessions * WORK_MINUTES} 分")
    print()

if __name__ == "__main__":
    main()
