import os
import sys
import time
import msvcrt

from display import (
    RED, GREEN, CYAN, BOLD, DIM, RESET,
    hide_cursor, show_cursor, clear_line, move_up,
    progress_bar, fmt_time, print_header,
)


def check_key():
    """Non-blocking key check. Returns char or None."""
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):  # special keys — consume next byte
            msvcrt.getch()
            return None
        return ch.decode('utf-8', errors='ignore').lower()
    return None


def wait_for_enter():
    """Block until Enter is pressed; return False if 'q' was pressed."""
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b'q':
                return False
            if ch == b'\r':
                return True


def run_timer(duration_min, mode, session, total_sessions):
    duration = duration_min * 60
    color = RED if mode == "work" else (GREEN if mode == "short" else CYAN)
    label = "残り時間"

    hide_cursor()
    os.system("cls")
    print_header(session, mode, total_sessions)

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
