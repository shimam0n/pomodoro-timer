import os
import sys

from config import WORK_MINUTES, SHORT_BREAK, LONG_BREAK, SESSIONS_UNTIL_LONG
from display import enable_ansi, show_cursor, BOLD, GREEN, YELLOW, CYAN, DIM, RESET
from timer import run_timer, notify, wait_for_enter


def main():
    enable_ansi()
    session = 1
    total_sessions = 0

    print(f"\n{BOLD}  ポモドーロタイマーへようこそ！{RESET}")
    print(f"  {WORK_MINUTES}分集中 → {SHORT_BREAK}分休憩 ({SESSIONS_UNTIL_LONG}回ごとに{LONG_BREAK}分の長休憩)")
    print(f"\n  {DIM}Enterキーで開始...{RESET}")
    input()

    while True:
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

        if total_sessions % SESSIONS_UNTIL_LONG == 0 and total_sessions > 0:
            break_mode = "long"
            break_min  = LONG_BREAK
            print(f"  {CYAN}お疲れ様でした！{LONG_BREAK}分の長い休憩を取りましょう。{RESET}")
        else:
            break_mode = "short"
            break_min  = SHORT_BREAK
            print(f"  {GREEN}{SHORT_BREAK}分の休憩を取りましょう。{RESET}")

        print(f"\n  {DIM}Enterキーで休憩を開始...{RESET}")
        if not wait_for_enter():
            show_cursor()
            sys.exit(0)

        result = run_timer(break_min, break_mode, session, total_sessions)
        if result == "quit":
            break

        notify(break_mode)
        session += 1

    os.system("cls")
    print(f"\n  {BOLD}お疲れ様でした！{RESET}")
    print(f"  完了したセッション: {total_sessions} 🍅")
    if total_sessions > 0:
        print(f"  集中した時間: {total_sessions * WORK_MINUTES} 分")
    print()


if __name__ == "__main__":
    main()
